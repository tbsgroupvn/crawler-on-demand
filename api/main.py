from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
import uuid
import json
import os
from datetime import datetime
import redis
from celery import Celery
import databases
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime, Text

# Database setup  
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
database = databases.Database(DATABASE_URL)
metadata = MetaData()

# Tasks table
tasks_table = Table(
    "tasks",
    metadata,
    Column("id", String, primary_key=True),
    Column("url", String, nullable=False),
    Column("status", String, nullable=False, default="pending"),
    Column("result", Text, nullable=True),
    Column("error", Text, nullable=True),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("completed_at", DateTime, nullable=True),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

# Redis setup
redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

# Celery setup
celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

# FastAPI app
app = FastAPI(
    title="Crawler On Demand API",
    description="A simple web crawler API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class CrawlRequest(BaseModel):
    url: HttpUrl
    depth: Optional[int] = 1
    max_pages: Optional[int] = 10

class TaskResponse(BaseModel):
    id: str
    url: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

# Database connection events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# API endpoints
@app.get("/")
async def root():
    return {
        "message": "Crawler On Demand API",
        "status": "running", 
        "version": "1.0.0"
    }

@app.post("/crawl")
async def create_crawl_task(request: CrawlRequest):
    task_id = str(uuid.uuid4())
    
    # Save task to database
    query = tasks_table.insert().values(
        id=task_id,
        url=str(request.url),
        status="pending",
        created_at=datetime.utcnow()
    )
    await database.execute(query)
    
    # Send task to Celery worker
    celery_app.send_task(
        "worker.crawl_url",
        args=[task_id, str(request.url), request.depth, request.max_pages]
    )
    
    return {
        "task_id": task_id,
        "status": "pending",
        "message": "Crawl task created successfully"
    }

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    query = tasks_table.select().where(tasks_table.c.id == task_id)
    task = await database.fetch_one(query)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    result = None
    if task.result:
        try:
            result = json.loads(task.result)
        except:
            result = {"raw": task.result}
    
    return {
        "id": task.id,
        "url": task.url,
        "status": task.status,
        "result": result,
        "error": task.error,
        "created_at": task.created_at,
        "completed_at": task.completed_at
    }

@app.get("/tasks")
async def list_tasks(limit: int = 20, offset: int = 0):
    # Get total count
    count_query = "SELECT COUNT(*) FROM tasks"
    total = await database.fetch_val(count_query)
    
    # Get tasks
    query = tasks_table.select().order_by(tasks_table.c.created_at.desc()).limit(limit).offset(offset)
    tasks = await database.fetch_all(query)
    
    task_responses = []
    for task in tasks:
        result = None
        if task.result:
            try:
                result = json.loads(task.result)
            except:
                result = {"raw": task.result}
        
        task_responses.append({
            "id": task.id,
            "url": task.url,
            "status": task.status,
            "result": result,
            "error": task.error,
            "created_at": task.created_at,
            "completed_at": task.completed_at
        })
    
    return {"tasks": task_responses, "total": total}

@app.get("/health")
async def health_check():
    try:
        await database.fetch_val("SELECT 1")
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    try:
        redis_client.ping()
        redis_status = "healthy"
    except:
        redis_status = "unhealthy"
    
    return {
        "status": "running",
        "database": db_status,
        "redis": redis_status,
        "celery": "configured"
    }

# New features added!

@app.get("/export/csv/{task_id}")
async def export_task_csv(task_id: str):
    from fastapi.responses import StreamingResponse
    import csv
    import io
    
    query = tasks_table.select().where(tasks_table.c.id == task_id)
    task = await database.fetch_one(query)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not task.result:
        raise HTTPException(status_code=400, detail="Task has no results to export")
    
    try:
        result = json.loads(task.result)
    except:
        raise HTTPException(status_code=400, detail="Invalid task result format")
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['URL', 'Title', 'Description', 'Headings', 'Paragraph_Count', 'Link_Count', 'Image_Count'])
    
    # Data rows
    for page in result.get('pages', []):
        writer.writerow([
            page.get('url', ''),
            page.get('title', ''),
            page.get('description', '')[:100] + '...' if len(page.get('description', '')) > 100 else page.get('description', ''),
            '; '.join(page.get('headings', []))[:200],
            len(page.get('paragraphs', [])),
            len(page.get('links', [])),
            len(page.get('images', []))
        ])
    
    output.seek(0)
    
    def iter_csv():
        yield output.getvalue()
    
    return StreamingResponse(
        iter_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=crawl_results_{task_id}.csv"}
    )

@app.get("/export/excel/{task_id}")
async def export_task_excel(task_id: str):
    from fastapi.responses import StreamingResponse
    import io
    import json
    from datetime import datetime
    
    query = tasks_table.select().where(tasks_table.c.id == task_id)
    task = await database.fetch_one(query)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not task.result:
        raise HTTPException(status_code=400, detail="Task has no results to export")
    
    try:
        result = json.loads(task.result)
    except:
        raise HTTPException(status_code=400, detail="Invalid task result format")
    
    # Create Excel content using openpyxl
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill
        from openpyxl.utils import get_column_letter
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Crawl Results"
        
        # Headers with styling
        headers = ['URL', 'Title', 'Description', 'Headings', 'Paragraphs', 'Links', 'Images', 'Content Size', 'Crawled At']
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
        
        # Data rows
        for row, page in enumerate(result.get('pages', []), 2):
            ws.cell(row=row, column=1, value=page.get('url', ''))
            ws.cell(row=row, column=2, value=page.get('title', ''))
            ws.cell(row=row, column=3, value=page.get('description', '')[:200] + '...' if len(page.get('description', '')) > 200 else page.get('description', ''))
            ws.cell(row=row, column=4, value='; '.join(page.get('headings', []))[:300])
            ws.cell(row=row, column=5, value=len(page.get('paragraphs', [])))
            ws.cell(row=row, column=6, value=len(page.get('links', [])))
            ws.cell(row=row, column=7, value=len(page.get('images', [])))
            ws.cell(row=row, column=8, value=page.get('content_length', 0))
            ws.cell(row=row, column=9, value=page.get('scraped_at', ''))
        
        # Auto-adjust column widths
        for col in range(1, len(headers) + 1):
            column_letter = get_column_letter(col)
            max_length = 0
            for row in ws[column_letter]:
                try:
                    if len(str(row.value)) > max_length:
                        max_length = len(str(row.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Save to BytesIO
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        
        def iter_excel():
            yield excel_buffer.getvalue()
        
        return StreamingResponse(
            iter_excel(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=crawl_results_{task_id}.xlsx"}
        )
        
    except ImportError:
        # Fallback to CSV if openpyxl not available
        raise HTTPException(status_code=501, detail="Excel export requires openpyxl. Use CSV export instead.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel export failed: {str(e)}")

@app.get("/tasks/filter/{status}")
async def filter_tasks_by_status(status: str, limit: int = 20):
    """Filter tasks by status: pending, running, completed, failed"""
    valid_statuses = ['pending', 'running', 'completed', 'failed']
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Use: {', '.join(valid_statuses)}")
    
    query = tasks_table.select().where(tasks_table.c.status == status).order_by(tasks_table.c.created_at.desc()).limit(limit)
    tasks = await database.fetch_all(query)
    
    task_responses = []
    for task in tasks:
        result = None
        if task.result:
            try:
                result = json.loads(task.result)
                # Add summary stats
                if 'pages' in result:
                    result['summary'] = {
                        'total_pages': len(result['pages']),
                        'total_links': sum(len(page.get('links', [])) for page in result['pages']),
                        'total_images': sum(len(page.get('images', [])) for page in result['pages'])
                    }
            except:
                result = {"raw": task.result}
        
        task_responses.append({
            "id": task.id,
            "url": task.url,
            "status": task.status,
            "result": result,
            "error": task.error,
            "created_at": task.created_at,
            "completed_at": task.completed_at
        })
    
    return {"tasks": task_responses, "status_filter": status, "count": len(task_responses)}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a specific task"""
    query = tasks_table.select().where(tasks_table.c.id == task_id)
    task = await database.fetch_one(query)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    delete_query = tasks_table.delete().where(tasks_table.c.id == task_id)
    await database.execute(delete_query)
    
    return {"message": f"Task {task_id} deleted successfully"}

@app.post("/batch/crawl")
async def batch_crawl(urls: List[str], depth: Optional[int] = 1, max_pages: Optional[int] = 5):
    """Create multiple crawl tasks at once"""
    if len(urls) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 URLs per batch")
    
    tasks = []
    for url in urls:
        task_id = str(uuid.uuid4())
        
        # Save task to database
        query = tasks_table.insert().values(
            id=task_id,
            url=url,
            status="pending",
            created_at=datetime.utcnow()
        )
        await database.execute(query)
        
        # Send task to Celery worker
        celery_app.send_task(
            "worker.crawl_url",
            args=[task_id, url, depth, max_pages]
        )
        
        tasks.append({
            "task_id": task_id,
            "url": url,
            "status": "pending"
        })
    
    return {
        "message": f"Created {len(tasks)} crawl tasks",
        "tasks": tasks
    }

@app.get("/stats")
async def get_system_stats():
    """Get system statistics"""
    # Count tasks by status
    stats = {}
    for status in ['pending', 'running', 'completed', 'failed']:
        count_query = f"SELECT COUNT(*) FROM tasks WHERE status = '{status}'"
        count = await database.fetch_val(count_query)
        stats[f"{status}_tasks"] = count
    
    # Total tasks
    total_query = "SELECT COUNT(*) FROM tasks"
    stats['total_tasks'] = await database.fetch_val(total_query)
    
    # Recent activity (last 24 hours)
    recent_query = "SELECT COUNT(*) FROM tasks WHERE created_at > datetime('now', '-1 day')"
    try:
        stats['tasks_last_24h'] = await database.fetch_val(recent_query)
    except:
        stats['tasks_last_24h'] = 0
    
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 