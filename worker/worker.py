from celery import Celery
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime
import sqlite3

# Celery app configuration
app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

def get_db_connection():
    """Get database connection"""
    # Share database file with API via volume
    db_path = "/app/app.db"
    return sqlite3.connect(db_path)

def update_task_status(task_id, status, result=None, error=None):
    """Update task status in database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status == "completed":
            cursor.execute(
                "UPDATE tasks SET status = ?, result = ?, completed_at = ? WHERE id = ?",
                (status, result, datetime.utcnow().isoformat(), task_id)
            )
        elif status == "failed":
            cursor.execute(
                "UPDATE tasks SET status = ?, error = ?, completed_at = ? WHERE id = ?",
                (status, error, datetime.utcnow().isoformat(), task_id)
            )
        else:
            cursor.execute(
                "UPDATE tasks SET status = ? WHERE id = ?",
                (status, task_id)
            )
        
        conn.commit()
        conn.close()
        print(f"Updated task {task_id} status to {status}")
    except Exception as e:
        print(f"Error updating task status: {e}")

def extract_content(url):
    """Extract content from a single URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic info
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title"
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ''
        
        # Extract headings
        headings = []
        for i in range(1, 4):  # h1 to h3 only
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    'level': i,
                    'text': heading.get_text().strip()
                })
                if len(headings) >= 10:  # Limit headings
                    break
        
        # Extract some paragraphs
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 20:  # Only meaningful paragraphs
                paragraphs.append(text)
                if len(paragraphs) >= 5:  # Limit paragraphs
                    break
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text().strip()
            if href and text:
                full_url = urljoin(url, href)
                parsed = urlparse(full_url)
                if parsed.scheme in ['http', 'https']:
                    links.append({
                        'url': full_url,
                        'text': text[:100],  # Limit text length
                        'internal': parsed.netloc == urlparse(url).netloc
                    })
                    if len(links) >= 20:  # Limit links
                        break
        
        return {
            'url': url,
            'status_code': response.status_code,
            'title': title_text,
            'description': description,
            'headings': headings,
            'paragraphs': paragraphs,
            'links': links,
            'content_length': len(response.content),
            'scraped_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return {
            'url': url,
            'error': str(e),
            'scraped_at': datetime.utcnow().isoformat()
        }

@app.task(bind=True)
def crawl_url(self, task_id, url, depth=1, max_pages=10):
    """Main crawling task"""
    try:
        print(f"Starting crawl task {task_id} for URL: {url}")
        update_task_status(task_id, "running")
        
        crawled_urls = set()
        to_crawl = [url]
        results = []
        current_depth = 0
        
        while to_crawl and len(results) < max_pages and current_depth < depth:
            current_batch = to_crawl.copy()
            to_crawl = []
            
            for current_url in current_batch:
                if current_url in crawled_urls or len(results) >= max_pages:
                    continue
                
                print(f"Crawling: {current_url}")
                content = extract_content(current_url)
                results.append(content)
                crawled_urls.add(current_url)
                
                # Collect internal links for next level
                if current_depth < depth - 1 and 'links' in content and not content.get('error'):
                    for link in content['links']:
                        if (link.get('internal') and 
                            link['url'] not in crawled_urls and 
                            link['url'] not in to_crawl):
                            to_crawl.append(link['url'])
                
                # Be respectful - small delay
                time.sleep(1)
            
            current_depth += 1
        
        # Prepare final result
        final_result = {
            'task_id': task_id,
            'total_pages': len(results),
            'crawled_urls': list(crawled_urls),
            'pages': results,
            'depth_reached': current_depth,
            'completed_at': datetime.utcnow().isoformat()
        }
        
        # Update task as completed
        result_json = json.dumps(final_result)
        update_task_status(task_id, "completed", result_json)
        
        print(f"Crawl task {task_id} completed successfully. Crawled {len(results)} pages.")
        return final_result
        
    except Exception as e:
        error_msg = f"Crawl task failed: {str(e)}"
        print(f"Error in task {task_id}: {error_msg}")
        update_task_status(task_id, "failed", error=error_msg)
        raise

@app.task
def health_check():
    """Simple health check task"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "worker": "operational"
    }

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

if __name__ == "__main__":
    app.start() 