// Crawler On Demand - Netlify Deployment Configuration
// This file contains deployment-specific settings and configurations

const deploymentConfig = {
  // Application Information
  app: {
    name: 'crawler-on-demand',
    version: '2.0.0',
    environment: process.env.NODE_ENV || 'production',
    demoMode: true
  },

  // Netlify Configuration
  netlify: {
    siteName: 'crawlall',
    siteUrl: 'https://crawlall.netlify.app',
    deployUrl: process.env.DEPLOY_URL || '',
    branch: process.env.HEAD || 'main',
    context: process.env.CONTEXT || 'production'
  },

  // GitHub Integration
  github: {
    repository: 'tbsgroupvn/crawler-on-demand',
    branch: 'main',
    issuesUrl: 'https://github.com/tbsgroupvn/crawler-on-demand/issues',
    documentationUrl: 'https://github.com/tbsgroupvn/crawler-on-demand#readme'
  },

  // API Configuration (Demo Mode)
  api: {
    baseUrl: process.env.DEMO_API_BASE_URL || '/api',
    timeout: parseInt(process.env.DEMO_TIMEOUT) || 5000,
    mockEnabled: true,
    mockDelay: 1000,
    endpoints: {
      health: '/api/health',
      crawl: '/api/crawl',
      tasks: '/api/tasks',
      export: '/api/export',
      search: '/api/search',
      analytics: '/api/analytics',
      compare: '/api/compare',
      stats: '/api/stats'
    }
  },

  // Performance Settings
  performance: {
    caching: {
      html: 3600,        // 1 hour
      static: 31536000,  // 1 year
      api: 300           // 5 minutes
    },
    compression: true,
    minification: true,
    imageOptimization: true
  },

  // Security Configuration
  security: {
    headers: {
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block',
      'X-Content-Type-Options': 'nosniff',
      'Referrer-Policy': 'strict-origin-when-cross-origin',
      'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
      'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    },
    contentSecurityPolicy: "default-src 'self' https: 'unsafe-inline' 'unsafe-eval'; img-src 'self' https: data:; font-src 'self' https: data:",
    cors: {
      origin: true,
      credentials: true
    }
  },

  // Feature Flags
  features: {
    advancedAnalytics: true,
    exportFeatures: true,
    searchFeatures: true,
    comparisonFeatures: true,
    realTimeUpdates: false,
    userAuthentication: false
  },

  // Demo Configuration
  demo: {
    enabled: true,
    sampleUrls: [
      'https://example.com',
      'https://github.com',
      'https://stackoverflow.com'
    ],
    maxDepth: 3,
    maxPages: 20,
    defaultTimeout: 30000
  },

  // Monitoring and Analytics
  monitoring: {
    enabled: true,
    errorTracking: true,
    performanceMonitoring: true,
    userAnalytics: false
  },

  // Contact Information
  contact: {
    supportEmail: 'support@tbsgroup.vn',
    companyName: 'TBS Group Vietnam',
    website: 'https://github.com/tbsgroupvn'
  },

  // Build Configuration
  build: {
    command: 'echo "Static deployment ready - Optimized for production"',
    publish: '.',
    functions: 'functions',
    environment: {
      NODE_ENV: 'production',
      CRAWLER_VERSION: '2.0.0'
    }
  },

  // Redirect Rules
  redirects: [
    { from: '/crawler', to: '/index.html', status: 200 },
    { from: '/demo', to: '/index.html', status: 200 },
    { from: '/github', to: 'https://github.com/tbsgroupvn/crawler-on-demand', status: 302 },
    { from: '/api/*', to: '/debug.html', status: 200 }
  ]
};

// Environment-specific overrides
if (deploymentConfig.netlify.context === 'deploy-preview') {
  deploymentConfig.app.environment = 'staging';
  deploymentConfig.demo.enabled = true;
  deploymentConfig.monitoring.userAnalytics = false;
}

if (deploymentConfig.netlify.context === 'branch-deploy') {
  deploymentConfig.app.environment = 'development';
  deploymentConfig.performance.caching.html = 0;
  deploymentConfig.security.headers['Cache-Control'] = 'no-cache';
}

// Export for Node.js and browser environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = deploymentConfig;
} else if (typeof window !== 'undefined') {
  window.deploymentConfig = deploymentConfig;
}

// Utility functions for deployment
const deploymentUtils = {
  // Get current environment
  getEnvironment: () => deploymentConfig.app.environment,
  
  // Check if demo mode is enabled
  isDemoMode: () => deploymentConfig.demo.enabled,
  
  // Get API base URL
  getApiBaseUrl: () => deploymentConfig.api.baseUrl,
  
  // Get site URL
  getSiteUrl: () => deploymentConfig.netlify.siteUrl,
  
  // Check if feature is enabled
  isFeatureEnabled: (feature) => deploymentConfig.features[feature] || false,
  
  // Get cache duration for resource type
  getCacheDuration: (type) => deploymentConfig.performance.caching[type] || 3600,
  
  // Get security headers
  getSecurityHeaders: () => deploymentConfig.security.headers,
  
  // Get demo configuration
  getDemoConfig: () => deploymentConfig.demo,
  
  // Generate meta tags for SEO
  generateMetaTags: () => ({
    title: 'Crawler On Demand - Professional Web Scraping Solution',
    description: 'Professional web scraping solution with FastAPI, Celery, Redis & Excel export',
    keywords: 'web scraping, crawler, fastapi, celery, redis, docker',
    author: deploymentConfig.contact.companyName,
    url: deploymentConfig.netlify.siteUrl
  })
};

// Export utilities as well
if (typeof module !== 'undefined' && module.exports) {
  module.exports.utils = deploymentUtils;
} else if (typeof window !== 'undefined') {
  window.deploymentUtils = deploymentUtils;
} 