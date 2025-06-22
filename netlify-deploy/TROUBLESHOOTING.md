# 🔧 Netlify Deployment Troubleshooting Guide

## Quick Fix Checklist

### ✅ Immediate Actions
1. **Clear browser cache** (Ctrl+F5 or Cmd+Shift+R)
2. **Try incognito/private browsing** mode
3. **Test different browsers** (Chrome, Firefox, Safari)
4. **Wait 5-10 minutes** after deployment (DNS propagation)

### 🔍 Debug URLs to Test
- Main site: `https://yoursite.netlify.app/`
- Simple test: `https://yoursite.netlify.app/simple`
- Hello test: `https://yoursite.netlify.app/hello`
- Debug helper: `https://yoursite.netlify.app/debug`

## Common Issues & Solutions

### 1. 🚨 404 Error on Root Path (`/`)

**Symptoms:**
- Site URL loads but shows "Page Not Found"
- Works on localhost but not on Netlify
- Other pages like `/simple` work fine

**Solutions:**
```bash
# Check _redirects file contains:
/                 /index.html     200

# Verify index.html exists in root of netlify-deploy folder
# File structure should be:
netlify-deploy/
├── index.html
├── _redirects
└── netlify.toml
```

**Fix Steps:**
1. Go to Netlify dashboard → Site → Deploys
2. Check if `index.html` is listed in deployed files
3. If missing, re-drag the entire netlify-deploy folder
4. Ensure you're uploading the folder contents, not the folder itself

### 2. 📁 Files Not Found (404 on specific pages)

**Symptoms:**
- Main page loads but `/simple` or `/test` shows 404
- Direct file URLs don't work

**Solutions:**
```bash
# Verify file names match exactly (case-sensitive):
/simple.html  # Not /Simple.html or /simple.HTML
/test.html    # Not /Test.html
/hello.html   # Not /hello.htm

# Check _redirects contains:
/simple           /simple.html    200
/test             /test.html      200
/hello            /hello.html     200
```

### 3. 🏗️ Deployment Failed

**Symptoms:**
- Netlify shows "Deploy failed" 
- Build process errors
- Site doesn't update after new deployment

**Solutions:**
1. **Check Deploy Logs:**
   - Go to Netlify Dashboard → Site → Deploys
   - Click on failed deploy → View function logs
   - Look for specific error messages

2. **Common Build Issues:**
   ```bash
   # If netlify.toml has errors:
   [build]
     publish = "."
     command = "echo 'Static deployment ready'"
   
   # Ensure no invalid JSON or YAML syntax
   ```

3. **Manual Deployment:**
   - Try drag & drop instead of Git integration
   - Upload only the netlify-deploy folder contents
   - Remove problematic files temporarily

### 4. 🌐 Site Loads but Content is Wrong

**Symptoms:**
- Old version of site is showing
- Changes don't appear after deployment
- Cached content

**Solutions:**
1. **Force Deploy:**
   ```bash
   # In Netlify dashboard:
   1. Go to Deploys tab
   2. Click "Trigger deploy" → "Clear cache and deploy site"
   ```

2. **Hard Refresh:**
   - Chrome/Firefox: `Ctrl + F5`
   - Safari: `Cmd + Shift + R`
   - Or use incognito mode

3. **Check CDN Cache:**
   - Wait 15-30 minutes for global CDN update
   - Try accessing from different locations/devices

### 5. ⚙️ Configuration Issues

**Symptoms:**
- Redirects not working
- Headers not applied
- Security warnings

**Check netlify.toml:**
```toml
[build]
  publish = "."
  command = "echo 'Static deployment ready'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
```

**Check _redirects:**
```
# Root redirect (most important)
/                 /index.html     200

# Test pages
/simple           /simple.html    200
/test             /test.html      200
/hello            /hello.html     200
/debug            /debug.html     200

# SPA behavior
/*                /index.html     200
```

## Step-by-Step Debugging

### Phase 1: Local Testing
```bash
# Test files locally first:
cd netlify-deploy
python -m http.server 3000

# Open browser to:
http://localhost:3000
http://localhost:3000/simple.html
http://localhost:3000/test.html
```

### Phase 2: File Verification
```bash
# Check file structure:
netlify-deploy/
├── index.html      (83KB - main demo)
├── simple.html     (2.3KB - simple test)  
├── test.html       (1.7KB - test page)
├── hello.html      (minimal test)
├── debug.html      (debug helper)
├── _redirects      (routing rules)
├── netlify.toml    (config)
└── README.md       (documentation)

# Verify file sizes match expected values
```

### Phase 3: Deployment Check
1. **Netlify Dashboard:**
   - Login to https://app.netlify.com
   - Find your site
   - Check deploy status: ✅ Published vs ❌ Failed

2. **Deploy Logs:**
   - Click on latest deploy
   - Review "Deploy log" for errors
   - Check "Functions log" if applicable

3. **File List:**
   - Verify all files are listed in deployed files
   - Check file sizes match local versions

### Phase 4: Live Testing
```bash
# Test these URLs in order:
1. https://yoursite.netlify.app/debug     # Debug helper
2. https://yoursite.netlify.app/hello     # Minimal test
3. https://yoursite.netlify.app/simple    # Simple test  
4. https://yoursite.netlify.app/test      # Test page
5. https://yoursite.netlify.app/          # Main site
```

## Emergency Recovery

### Quick Redeploy
1. Download working files from GitHub:
   ```bash
   git clone https://github.com/tbsgroupvn/crawler-on-demand.git
   cd crawler-on-demand/netlify-deploy
   ```

2. Manual Upload:
   - Go to Netlify dashboard
   - Drag the entire `netlify-deploy` folder to deploy area
   - Wait for deployment to complete

### Minimal Test Site
If main site fails, deploy just these files:
```
minimal-test/
├── index.html      (simple "Hello World")
├── _redirects      (basic routing)
└── netlify.toml    (minimal config)
```

Create `minimal-test/index.html`:
```html
<!DOCTYPE html>
<html>
<head><title>Test Site</title></head>
<body>
  <h1>✅ Site Working!</h1>
  <p>Time: <span id="time"></span></p>
  <script>
    document.getElementById('time').textContent = new Date().toLocaleString();
  </script>
</body>
</html>
```

## Support Resources

### 🔗 Useful Links
- **Netlify Status:** https://www.netlifystatus.com/
- **Netlify Docs:** https://docs.netlify.com/
- **GitHub Repo:** https://github.com/tbsgroupvn/crawler-on-demand
- **Debug Helper:** /debug.html (on deployed site)

### 📞 Getting Help
1. **Check GitHub Issues:** Look for similar problems
2. **Netlify Community:** https://community.netlify.com/
3. **Discord/Forums:** Search for Netlify deployment issues
4. **Debug Helper:** Use `/debug` page on your deployed site

### 🐛 Reporting Issues
When asking for help, include:
- Site URL
- Error messages (exact text)
- Browser and version
- Steps to reproduce
- Screenshot of error
- Deploy log (if available)

---

**Last Updated:** Deploy v2.0 with enhanced debugging tools
**Test Pages:** `/debug`, `/simple`, `/hello`, `/test` 