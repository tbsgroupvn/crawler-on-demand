# ��️ Crawler On Demand - Enhanced AI-Powered Web Scraping Platform

**Professional web scraping solution with advanced analytics, SEO analysis, content intelligence, and real-time processing capabilities**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Celery](https://img.shields.io/badge/Celery-5.3+-red.svg)](https://celeryproject.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 **New Enhanced Features (v2.0)**

### **🧠 AI-Powered Content Analysis**
- **SEO Analysis**: Title length, meta descriptions, headings structure, Open Graph tags, Schema markup
- **Content Quality Metrics**: Word count, readability scores, language detection, content freshness
- **Social Media Detection**: Automatic discovery of Facebook, Twitter, Instagram, LinkedIn, YouTube, TikTok links
- **Contact Information Extraction**: Emails, phone numbers, addresses with Vietnamese format support
- **Structured Data Extraction**: Breadcrumbs, navigation menus, forms, tables, footer links

### **📊 Advanced Analytics & Insights**
- **Content Analytics API**: `/analytics/{task_id}` - Deep content analysis with keyword extraction
- **Website Comparison**: `/compare` - Compare multiple websites side-by-side
- **Smart Search**: `/search` - Search across all crawled content with filters
- **Advanced Dashboard**: Real-time statistics, domain analysis, time-series data
- **Enhanced Export**: JSON with analytics, professional Excel reports, comprehensive CSV

### **⚡ Performance & Reliability**
- **Parallel Processing**: Multi-worker support with Redis clustering
- **Smart Progress Tracking**: Real-time progress updates with detailed messaging
- **Enhanced Error Handling**: Automatic retries, graceful degradation
- **Respectful Crawling**: Configurable delays, robots.txt respect
- **Health Monitoring**: Container health checks, service monitoring

## 📋 **Complete API Endpoints**

| Method | Endpoint | Description | Enhanced Features |
|--------|----------|-------------|-------------------|
| `GET` | `/` | API status and info | ✅ System health |
| `POST` | `/crawl` | Start single URL crawl | ✅ Enhanced extraction |
| `POST` | `/batch/crawl` | Batch URL processing | ✅ Parallel execution |
| `GET` | `/tasks` | List all tasks | ✅ Advanced filtering |
| `GET` | `/tasks/{task_id}` | Get task details | ✅ Rich metadata |
| `GET` | `/analytics/{task_id}` | **NEW** Content analytics | 🔥 AI-powered analysis |
| `GET` | `/compare` | **NEW** Website comparison | 🔥 Multi-site analysis |
| `POST` | `/search` | **NEW** Content search | 🔥 Advanced search |
| `GET` | `/export/csv/{task_id}` | Export to CSV | ✅ Enhanced data |
| `GET` | `/export/excel/{task_id}` | Export to Excel | ✅ Professional formatting |
| `GET` | `/export/json/{task_id}` | **NEW** Export JSON | 🔥 With analytics |
| `GET` | `/dashboard/advanced` | **NEW** Advanced stats | 🔥 Real-time insights |
| `DELETE` | `/tasks/{task_id}` | Delete task | ✅ Clean removal |
| `GET` | `/tasks/filter/{status}` | Filter by status | ✅ Smart filtering |
| `GET` | `/stats` | System statistics | ✅ Enhanced metrics |
| `GET` | `/health` | Health check | ✅ Service monitoring |

## 🛠️ **Technology Stack**

### **Backend Services**
- **FastAPI** 0.104+ - High-performance async API framework
- **Celery** 5.3+ - Distributed task queue with Redis broker
- **SQLAlchemy** 2.0+ - Modern ORM with async support
- **Redis** 7+ - In-memory data structure store
- **SQLite** - Embedded database for development
- **Docker** - Containerization with health checks

### **Web Scraping Engine**
- **BeautifulSoup4** 4.12+ - HTML/XML parsing
- **Requests** 2.31+ - HTTP library with session management
- **lxml** 4.9+ - Fast XML/HTML processing
- **cssselect** 1.2+ - CSS selector support

### **Data Processing & Analytics**
- **OpenPyXL** 3.1+ - Excel file generation
- **python-dateutil** - Advanced date parsing
- **Collections.Counter** - Frequency analysis
- **Regular Expressions** - Pattern matching

### **Frontend Demo**
- **Vanilla JavaScript** - No framework dependencies
- **Tailwind CSS** - Utility-first CSS framework
- **Responsive Design** - Mobile-first approach

## 🚦 **Quick Start**

### **1. Clone Repository**
```bash
git clone https://github.com/tbsgroupvn/crawler-on-demand.git
cd crawler-on-demand
```

### **2. Start with Docker (Recommended)**
```bash
# Start all services
docker compose up -d

# Check service health
docker compose ps
docker compose logs api
```

### **3. Access Services**
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Redis**: localhost:6379
- **Demo Interface**: Open `netlify-deploy/index.html`

### **4. Test Enhanced Features**
```bash
# Test basic crawl
curl -X POST "http://localhost:8000/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "max_depth": 2, "max_pages": 5}'

# Get analytics
curl "http://localhost:8000/analytics/{task_id}"

# Search content
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "technology", "type": "all"}'

# Compare websites
curl "http://localhost:8000/compare?urls=https://site1.com,https://site2.com"
```

## 📈 **Enhanced Data Structure**

### **Crawled Page Data (Enhanced)**
```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "description": "Meta description",
  "content_size": 45678,
  "status_code": 200,
  "crawled_at": "2024-01-15T10:30:00",
  
  "seo_analysis": {
    "title_length": 65,
    "meta_description_length": 155,
    "h1_count": 1,
    "h2_count": 5,
    "og_tags": {"og:title": "...", "og:description": "..."},
    "schema_markup": [{"@type": "Organization", "name": "..."}],
    "canonical_url": "https://example.com/",
    "robots_meta": "index,follow",
    "lang": "en"
  },
  
  "content_quality": {
    "word_count": 1250,
    "paragraph_count": 12,
    "image_count": 8,
    "video_count": 2,
    "link_count": 25,
    "readability_score": 12.5,
    "language_detected": "english"
  },
  
  "social_media": {
    "facebook": ["https://facebook.com/company"],
    "twitter": ["https://twitter.com/company"],
    "linkedin": ["https://linkedin.com/company/company"]
  },
  
  "contact_info": {
    "emails": ["contact@example.com", "info@example.com"],
    "phones": ["+1-555-123-4567", "(555) 987-6543"],
    "addresses": []
  },
  
  "structured_data": {
    "breadcrumbs": ["Home", "Products", "Category"],
    "navigation_menu": [
      {"text": "Home", "href": "/"},
      {"text": "About", "href": "/about"}
    ],
    "forms": [
      {
        "action": "/contact",
        "method": "post",
        "inputs": [
          {"type": "email", "name": "email", "required": true},
          {"type": "text", "name": "message", "required": true}
        ]
      }
    ],
    "tables": [
      {"headers": ["Product", "Price", "Stock"], "rows": 10}
    ]
  }
}
```

## 🔧 **Configuration Options**

### **Environment Variables**
```bash
# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Database Configuration
DATABASE_URL=sqlite:///app/app.db

# Crawler Settings
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
CRAWL_DELAY=1

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
```

### **Docker Compose Override**
Create `docker-compose.override.yml` for custom settings:
```yaml
services:
  api:
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    ports:
      - "8001:8000"  # Custom port
  
  worker:
    deploy:
      replicas: 4  # Scale workers
```

## 🎯 **Advanced Usage Examples**

### **1. Content Analytics**
```python
import requests

# Start crawl
response = requests.post("http://localhost:8000/crawl", json={
    "url": "https://techcrunch.com",
    "max_depth": 2,
    "max_pages": 10
})
task_id = response.json()["task_id"]

# Get detailed analytics
analytics = requests.get(f"http://localhost:8000/analytics/{task_id}")
print(f"SEO Score: {analytics.json()['analytics']['seo_score']}")
print(f"Top Keywords: {analytics.json()['analytics']['top_keywords']}")
```

### **2. Batch Processing**
```python
# Process multiple URLs
batch_response = requests.post("http://localhost:8000/batch/crawl", json={
    "urls": [
        "https://example1.com",
        "https://example2.com",
        "https://example3.com"
    ],
    "max_depth": 1,
    "max_pages": 5
})
```

### **3. Advanced Search**
```python
# Search across all crawled content
search_response = requests.post("http://localhost:8000/search", json={
    "keyword": "artificial intelligence",
    "type": "content"
})

for result in search_response.json()["results"]:
    print(f"Found in: {result['url']}")
    for match in result["matches"]:
        print(f"  {match['type']}: {match['content'][:100]}...")
```

### **4. Website Comparison**
```python
# Compare multiple websites
comparison = requests.get("http://localhost:8000/compare", params={
    "urls": "https://site1.com,https://site2.com,https://site3.com"
})

summary = comparison.json()["summary"]
print(f"Best content volume: {summary['metrics']['word_count']['highest']}")
print(f"Average page count: {summary['metrics']['total_pages']['average']}")
```

## 📊 **Performance Metrics**

### **Benchmark Results**
- **Processing Speed**: 5-10 pages/second (depending on content)
- **Memory Usage**: ~100MB base + ~10MB per concurrent request
- **Storage**: ~1KB per page crawled (compressed)
- **Response Time**: <100ms for API calls, <5s for analytics

### **Scalability**
- **Horizontal Scaling**: Add more worker containers
- **Redis Clustering**: Support for Redis clusters
- **Database Scaling**: PostgreSQL support for production
- **Load Balancing**: Multiple API instances

## 🔒 **Security Features**

- **Rate Limiting**: Configurable request limits
- **Input Validation**: Pydantic models for all inputs
- **URL Filtering**: Whitelist/blacklist support
- **CORS Protection**: Configurable CORS policies
- **Health Checks**: Container and service monitoring
- **Error Handling**: Graceful failure modes

## 🌐 **Deployment Options**

### **1. Local Development**
```bash
docker compose up -d
```

### **2. Production with Docker Swarm**
```bash
docker stack deploy -c docker-compose.yml crawler-stack
```

### **3. Kubernetes Deployment**
```yaml
# See k8s/ directory for full configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crawler-api
spec:
  replicas: 3
  # ... full k8s config available
```

### **4. Cloud Deployment**
- **AWS ECS**: Elastic Container Service
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Managed containers
- **DigitalOcean Apps**: Platform-as-a-Service

## 🧪 **Testing**

### **Unit Tests**
```bash
cd api && python -m pytest tests/ -v
cd worker && python -m pytest tests/ -v
```

### **Integration Tests**
```bash
docker compose -f docker-compose.test.yml up --abort-on-container-exit
```

### **Load Testing**
```bash
# Install artillery
npm install -g artillery

# Run load test
artillery run tests/load-test.yml
```

## 📝 **Contributing**

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### **Development Setup**
```bash
# Clone and setup
git clone https://github.com/tbsgroupvn/crawler-on-demand.git
cd crawler-on-demand

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r api/requirements.txt
pip install -r worker/requirements.txt

# Run tests
pytest
```

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **FastAPI** team for the excellent framework
- **Celery** project for distributed task processing
- **BeautifulSoup** for HTML parsing capabilities
- **Docker** for containerization support
- **Redis** for reliable message brokering
- **Tailwind CSS** for beautiful UI components

## 📞 **Support & Contact**

- **GitHub Issues**: [Report bugs and feature requests](https://github.com/tbsgroupvn/crawler-on-demand/issues)
- **Documentation**: [Full API documentation](http://localhost:8000/docs)
- **Demo**: [Live demo interface](https://your-netlify-site.netlify.app)

---

**Built with ❤️ by TBS Group Vietnam**  
*Professional web scraping solutions for modern businesses* 