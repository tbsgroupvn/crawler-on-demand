# 🕷️ Crawler On Demand - Netlify Demo

This is a **live demo** of the Crawler On Demand web interface, optimized for Netlify deployment.

## 🌐 Live Demo

**Demo URL**: [https://crawler-on-demand.netlify.app](https://crawler-on-demand.netlify.app)

## ⚡ What This Demo Shows

- **Beautiful Interface**: Modern UI with Tailwind CSS
- **Interactive Forms**: Try the crawling interface (demo mode)
- **Feature Overview**: See what the full system can do
- **GitHub Integration**: Links to source code and deployment guide

## 🔄 Demo vs Full System

| Feature | Demo | Full System |
|---------|------|-------------|
| **UI Interface** | ✅ Complete | ✅ Complete |
| **Form Interaction** | ✅ Demo Mode | ✅ Real API calls |
| **Data Processing** | ❌ UI Only | ✅ Full crawling |
| **Excel Export** | ❌ Demo | ✅ Real exports |
| **Real-time Stats** | ❌ Static | ✅ Live updates |

## 🚀 Deploy Full System

To get the complete functionality:

```bash
# Clone the repository
git clone https://github.com/tbsgroupvn/crawler-on-demand.git
cd crawler-on-demand

# Start with Docker
docker-compose up -d

# Access locally
# API: http://localhost:8000
# Interface: Open crawler_complete.html
```

## 📁 Files in This Demo

- `index.html` - Main demo interface
- `_redirects` - Netlify routing rules
- `netlify.toml` - Deployment configuration
- `README.md` - This file

## 🔗 Links

- **GitHub Repository**: [tbsgroupvn/crawler-on-demand](https://github.com/tbsgroupvn/crawler-on-demand)
- **Deployment Guide**: [Quick Start](https://github.com/tbsgroupvn/crawler-on-demand#-quick-start)
- **API Documentation**: Available when running locally at `/docs`

## 🛠️ Technical Stack

- **Frontend**: Vanilla JavaScript + Tailwind CSS
- **Backend**: FastAPI + Celery + Redis (not included in demo)
- **Export**: OpenPyXL for Excel, CSV standard
- **Deployment**: Docker + Docker Compose

## 📊 Full System Features

When deployed locally, you get:

- ✅ **10+ API Endpoints** for complete functionality
- ✅ **Real Web Crawling** with depth control
- ✅ **Excel & CSV Export** with professional formatting
- ✅ **Batch Processing** for multiple URLs
- ✅ **Real-time Dashboard** with live updates
- ✅ **Task Management** with status tracking
- ✅ **Multi-language Support** for international sites

---

**Ready to deploy the full system?** [View the deployment guide →](https://github.com/tbsgroupvn/crawler-on-demand#-quick-start) 