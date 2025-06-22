# 🚀 Netlify Deployment Guide - Crawler On Demand

This directory contains the **optimized static deployment files** for the **Crawler On Demand** demo interface with enhanced configuration.

## 🌐 Live Demo

**Demo URL**: [https://crawlall.netlify.app](https://crawlall.netlify.app)  
**GitHub**: [tbsgroupvn/crawler-on-demand](https://github.com/tbsgroupvn/crawler-on-demand)

## 📁 Enhanced Files Structure

### **Core Files**
- `index.html` - Main demo interface with advanced features
- `debug.html` - API debugging and simulation page
- `hello.html` - Simple test page
- `simple.html` - Minimal crawler demo
- `test.html` - Feature testing page

### **🔧 Configuration Files** (NEW!)
- `netlify.toml` - **Enhanced Netlify configuration** with security, caching, and performance optimizations
- `_redirects` - **Advanced URL routing** with API simulation and clean URLs
- `package.json` - Dependency management and build scripts
- `deployment.config.js` - **Comprehensive deployment configuration** with environment management
- `TROUBLESHOOTING.md` - Deployment troubleshooting guide

## ⚡ Enhanced Features

### **🛡️ Security Enhancements**
- **HSTS** (HTTP Strict Transport Security)
- **CSP** (Content Security Policy)
- **XSS Protection** with mode=block
- **Frame Options** protection (DENY)
- **Content-Type** sniffing protection
- **Referrer Policy** configuration

### **📊 Performance Optimizations**
- **Caching Strategy**:
  - HTML: 1 hour cache with revalidation
  - Static assets: 1 year cache (immutable)
  - API responses: 5 minutes cache
- **Compression**: Gzip/Brotli for all assets
- **Minification**: CSS, JS, and HTML optimization
- **Image Optimization**: Automatic compression

### **🌐 Advanced Routing**
- **API Demo Routes**: `/api/*` → Debug interface
- **Clean URLs**: `/crawler`, `/demo`, `/dashboard` → Main interface
- **External Links**: `/github`, `/docs`, `/deploy` → GitHub repository
- **Legacy Support**: Old URLs redirected to new structure
- **Version Support**: `/v1/*`, `/v2/*`, `/beta/*` handling

## 🚀 Deployment Methods

### **Method 1: Netlify Dashboard**
1. Connect your GitHub repository to Netlify
2. Set **Build settings**:
   - **Build command**: `npm run build`
   - **Publish directory**: `netlify-deploy`
   - **Node version**: `18.x`
3. Add **Environment variables** (optional):
   ```
   NODE_ENV=production
   CRAWLER_VERSION=2.0.0
   DEMO_MODE=true
   ```
4. Deploy! 🎉

### **Method 2: Netlify CLI**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from netlify-deploy directory
cd netlify-deploy
netlify deploy

# Production deployment
netlify deploy --prod
```

### **Method 3: Git Integration**
```bash
# Push to your connected GitHub repository
git add .
git commit -m "Enhanced deployment configuration"
git push origin main

# Netlify will auto-deploy from the main branch
```

## 🖥️ Local Development

### **Standard Development Server**
```bash
cd netlify-deploy

# Python HTTP server
python -m http.server 8888

# OR Node.js server (if you have package.json)
npm install
npm run dev
```

### **Netlify Dev (Recommended)**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Run local Netlify environment
cd netlify-deploy
netlify dev

# This simulates the actual Netlify environment locally
```

Visit: http://localhost:8888

## 🔄 Demo vs Full System

| Feature | Demo | Full System |
|---------|------|-------------|
| **UI Interface** | ✅ Complete | ✅ Complete |
| **Form Interaction** | ✅ Demo Mode | ✅ Real API calls |
| **Data Processing** | ❌ UI Only | ✅ Full crawling |
| **Excel Export** | ❌ Demo | ✅ Real exports |
| **Real-time Stats** | ❌ Static | ✅ Live updates |
| **Security Headers** | ✅ Production-ready | ✅ Production-ready |
| **Performance** | ✅ Optimized | ✅ Optimized |

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
# Interface: http://localhost:3000 (Next.js)
```

## 📈 Performance Metrics

### **Optimized Caching**
- **HTML files**: 1 hour (3600s) with revalidation
- **CSS/JS files**: 1 year (31536000s) immutable cache
- **Images**: 1 year (31536000s) immutable cache
- **Fonts**: 1 year with CORS headers

### **Security Score**
- **A+ SSL Labs rating** with HSTS
- **CSP protection** against XSS attacks
- **Frame protection** against clickjacking
- **Content-type protection** against MIME sniffing

## 🔍 Testing Deployment

### **Pre-deployment Checks**
```bash
# Validate configuration
npm run validate

# Test build process
npm run build

# Run deployment tests
npm run test
```

### **Post-deployment Verification**
1. **Main page loads**: https://your-site.netlify.app
2. **API simulation works**: https://your-site.netlify.app/api/health
3. **Redirects function**: https://your-site.netlify.app/github
4. **Clean URLs work**: https://your-site.netlify.app/crawler
5. **Security headers**: Check with tools like securityheaders.com

## 🛠️ Customization

### **Update Site Information**
Edit `deployment.config.js`:
```javascript
netlify: {
  siteName: 'your-site-name',
  siteUrl: 'https://your-site.netlify.app'
}
```

### **Modify API Endpoints**
Edit `_redirects` for custom API simulation:
```
/api/your-endpoint    /debug.html?endpoint=your-endpoint    200
```

### **Custom Headers**
Add to `netlify.toml`:
```toml
[[headers]]
  for = "/your-path/*"
  [headers.values]
    Custom-Header = "your-value"
```

## 🔗 Links

- **GitHub Repository**: [tbsgroupvn/crawler-on-demand](https://github.com/tbsgroupvn/crawler-on-demand)
- **Deployment Guide**: [Quick Start](https://github.com/tbsgroupvn/crawler-on-demand#-quick-start)
- **API Documentation**: [API Endpoints](https://github.com/tbsgroupvn/crawler-on-demand#-api-endpoints)
- **Docker Guide**: [Docker Deployment](https://github.com/tbsgroupvn/crawler-on-demand#docker-deployment)

## 🛠️ Technical Stack

- **Frontend**: Vanilla JavaScript + Tailwind CSS
- **Backend**: FastAPI + Celery + Redis (not included in demo)
- **Export**: OpenPyXL for Excel, CSV standard
- **Deployment**: Docker + Docker Compose
- **CDN**: Netlify Edge Network
- **Security**: HTTPS, HSTS, CSP, XSS Protection

## 📊 Full System Features

When deployed locally, you get:

- ✅ **15+ API Endpoints** for complete functionality
- ✅ **Real Web Crawling** with depth control and multi-threading
- ✅ **Excel & CSV Export** with professional formatting
- ✅ **Batch Processing** for multiple URLs simultaneously
- ✅ **Real-time Dashboard** with live updates via WebSocket
- ✅ **Task Management** with status tracking and history
- ✅ **Multi-language Support** for international sites
- ✅ **Advanced Analytics** with content analysis
- ✅ **Search & Filter** across crawled data
- ✅ **Website Comparison** tools

## 🆘 Troubleshooting

Common issues and solutions are documented in [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md).

Quick fixes:
- **Build fails**: Check Node.js version (requires 16+)
- **Redirects not working**: Verify `_redirects` file format
- **Assets not loading**: Check `netlify.toml` publish directory
- **Security warnings**: Review CSP configuration

## 🎯 Next Steps

After successful deployment:
1. **Set up custom domain** (optional)
2. **Configure form handling** (if needed)
3. **Add analytics** (Google Analytics, etc.)
4. **Set up monitoring** (Netlify Analytics)
5. **Enable branch deploys** for testing

---

**Ready to deploy the full system?** [View the deployment guide →](https://github.com/tbsgroupvn/crawler-on-demand#-quick-start)

**✨ Built with ❤️ by TBS Group Vietnam**  
*Professional web scraping solutions for modern businesses* 