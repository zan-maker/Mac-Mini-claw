/**
 * AI Marketing Pro - Backend Server
 * Main application entry point
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// Import services and controllers
const AIContentService = require('./services/AIContentService');
const ContentController = require('./controllers/ContentController');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3001;

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// Initialize services
const aiContentService = new AIContentService();
const contentController = new ContentController(aiContentService);

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'AI Marketing Pro Backend',
    version: '1.0.0'
  });
});

// API Routes
app.post('/api/v1/content/generate', (req, res) => contentController.generateContent(req, res));
app.post('/api/v1/content/batch', (req, res) => contentController.batchGenerate(req, res));
app.get('/api/v1/content/templates', (req, res) => contentController.getTemplates(req, res));
app.get('/api/v1/content/history', (req, res) => contentController.getHistory(req, res));
app.post('/api/v1/competitor/analyze', (req, res) => contentController.analyzeCompetitor(req, res));

// Campaign management endpoints (placeholder)
app.post('/api/v1/campaigns', (req, res) => {
  res.status(201).json({
    success: true,
    message: 'Campaign created successfully',
    campaignId: `campaign_${Date.now()}`,
    data: req.body
  });
});

app.get('/api/v1/campaigns', (req, res) => {
  res.status(200).json({
    success: true,
    campaigns: []
  });
});

// Analytics endpoints (placeholder)
app.get('/api/v1/analytics/overview', (req, res) => {
  res.status(200).json({
    success: true,
    analytics: {
      totalContentGenerated: 0,
      averageEngagementScore: 0,
      topContentTypes: [],
      recentActivity: []
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  
  res.status(err.status || 500).json({
    success: false,
    error: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint not found',
    path: req.originalUrl
  });
});

// Start server
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`🚀 AI Marketing Pro Backend running on port ${PORT}`);
    console.log(`📡 Health check: http://localhost:${PORT}/health`);
    console.log(`🔌 API Base URL: http://localhost:${PORT}/api/v1`);
    console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
  });
}

module.exports = app; // For testing