# 🕷️ Crawler On Demand

A professional web scraping solution built with FastAPI, Celery, Redis, and modern web technologies.

## ✨ Features

- **🔗 Single URL Crawling**: Deep crawl individual websites with configurable depth and page limits
- **📦 Batch Processing**: Crawl multiple websites simultaneously  
- **📊 Excel Export**: Professional .xlsx export with styling and formatting
- **📄 CSV Export**: Standard CSV format for data analysis
- **🔄 Real-time Monitoring**: Live dashboard with task status and statistics
- **⚡ Async Processing**: High-performance asynchronous crawling with Celery workers
- **🎯 Smart Extraction**: Automatically extracts titles, descriptions, headings, paragraphs, links, and images
- **📈 Analytics Dashboard**: Comprehensive statistics and task management
- **🌐 Multi-language Support**: Optimized for Vietnamese and international websites

## 🏗️ Architecture

```
├── api/          # FastAPI backend server
├── worker/       # Celery worker for crawling tasks  
├── web/          # Next.js frontend (development)
├── crawler_complete.html  # Production-ready HTML interface
└── docker-compose.yml     # Full stack deployment
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Python 3.9+ (for local development)
- Node.js 18+ (for frontend development)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crawler-on-demand.git
cd crawler-on-demand
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
- **API**: http://localhost:8000
- **Web Interface**: Open `crawler_complete.html` in your browser
- **API Documentation**: http://localhost:8000/docs

### Local Development

1. Start Redis:
```bash
docker run -d -p 6379:6379 redis:alpine
```

2. Install API dependencies:
```bash
cd api
pip install -r requirements.txt
python main.py
```

3. Install Worker dependencies:
```bash
cd worker
pip install -r requirements.txt
celery -A worker worker --loglevel=info
```

## 📚 API Endpoints

### Core Endpoints
- `POST /crawl` - Create single URL crawl task
- `POST /batch/crawl` - Create batch crawl tasks
- `GET /tasks` - List all tasks
- `GET /tasks/{id}` - Get specific task details
- `DELETE /tasks/{id}` - Delete task

### Export Endpoints
- `GET /export/csv/{id}` - Export task data as CSV
- `GET /export/excel/{id}` - Export task data as Excel

### Management Endpoints
- `GET /stats` - System statistics
- `GET /tasks/filter/{status}` - Filter tasks by status
- `GET /health` - Health check

## 💻 Usage Examples

### Single URL Crawl
```bash
curl -X POST "http://localhost:8000/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "depth": 2,
    "max_pages": 10
  }'
```

### Batch Crawl
```bash
curl -X POST "http://localhost:8000/batch/crawl" \
  -H "Content-Type: application/json" \
  -d '["https://site1.com", "https://site2.com", "https://site3.com"]'
```

### Export Data
```bash
# Download CSV
curl "http://localhost:8000/export/csv/{task_id}" -o data.csv

# Download Excel
curl "http://localhost:8000/export/excel/{task_id}" -o data.xlsx
```

## 🎯 Crawling Capabilities

### Extracted Data Points
- **Title**: Page title
- **Description**: Meta description
- **Headings**: H1, H2, H3 tags content
- **Paragraphs**: All paragraph text
- **Links**: Internal and external links
- **Images**: Image URLs and alt text
- **Content Size**: Total content size in bytes
- **Metadata**: Crawl timestamp and processing info

### Crawling Features
- **Respectful Crawling**: Built-in delays and rate limiting
- **Multi-level Depth**: Configurable crawling depth (1-3 levels)
- **Page Limits**: Control maximum pages per domain
- **Error Handling**: Robust error handling and retry logic
- **Content Filtering**: Smart content extraction and cleaning

## 🌟 Web Interface Features

### Dashboard
- Real-time statistics (Pending, Running, Completed, Failed tasks)
- Auto-refresh every 5 seconds
- Beautiful gradient design with Tailwind CSS

### Forms
- **Single Crawl**: URL input with depth and page limit controls
- **Batch Crawl**: Multi-line URL input with sample URL sets
- **Quick Test**: One-click testing with popular websites

### Task Management
- Task list with status indicators
- Export buttons for CSV and Excel
- Delete individual tasks or bulk clear
- Task filtering and search

### Sample URL Sets
- 🇻🇳 Vietnamese news sites (VnExpress, Dân Trí, etc.)
- 💻 Tech websites (GitHub, Stack Overflow, etc.)
- 🛒 E-commerce sites (Shopee, Tiki, etc.)
- 🧪 Test & demo sites for development

## 📊 Data Export

### CSV Export
- Standard comma-separated format
- Compatible with Excel, Google Sheets
- Headers: URL, Title, Description, Headings, Paragraphs, Links, Images, Content Size, Crawled At

### Excel Export (.xlsx)
- Professional formatting with styled headers
- Auto-adjusting column widths
- Blue header with white text
- Ready for business reporting

## 🔧 Configuration

### Environment Variables
```bash
# Redis connection
REDIS_URL=redis://localhost:6379/0

# Celery configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# API configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### Docker Compose Services
- **redis**: Redis server for task queue
- **api**: FastAPI application server
- **worker**: Celery worker processes
- **web**: Next.js frontend (development mode)

## 🧪 Tested Websites

Successfully tested with:
- ✅ Vietnamese news sites (VnExpress, Dân Trí, Thanh Niên, Genk.vn)
- ✅ International tech sites (GitHub, Stack Overflow, Medium)
- ✅ E-commerce platforms (Shopee, Tiki, Lazada)
- ✅ Development/test sites (HTTPBin, Quotes to Scrape)

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **Celery**: Distributed task queue
- **Redis**: Message broker and cache
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP client
- **OpenPyXL**: Excel file generation

### Frontend
- **Vanilla JavaScript**: Pure JS for maximum compatibility
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-friendly interface

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Git**: Version control

## 📈 Performance

- **Concurrent Processing**: Multiple Celery workers
- **Asynchronous I/O**: Non-blocking HTTP requests
- **Memory Efficient**: Streaming data processing
- **Scalable Architecture**: Horizontal scaling with additional workers

### Benchmarks
- Genk.vn: 5 pages crawled in ~6 seconds (377KB content)
- VnExpress: 300KB+ content extraction
- Batch processing: 4 websites simultaneously

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/crawler-on-demand/issues)
- **Documentation**: See `/docs` folder
- **API Docs**: http://localhost:8000/docs (when running)

## 🚀 Roadmap

- [ ] Database persistence options (PostgreSQL, MongoDB)
- [ ] User authentication and multi-tenancy
- [ ] Scheduled crawling jobs
- [ ] Advanced filtering and content analysis
- [ ] Machine learning-based content classification
- [ ] Webhook notifications
- [ ] API rate limiting and quotas
- [ ] Advanced export formats (JSON, XML)

---

Built with ❤️ using modern web technologies. Perfect for data scientists, researchers, and businesses needing reliable web scraping solutions. 