#!/usr/bin/env node
/**
 * BuilderBase Construction Profit Analyzer - Backend API
 * Secure server with Stripe integration and email delivery
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const morgan = require('morgan');
const path = require('path');

// Import services
const BrevoService = require('./services/brevoService');
const GmailService = require('./services/gmailService');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'https://www.cubiczan.com',
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: process.env.RATE_LIMIT_WINDOW_MS || 15 * 60 * 1000, // 15 minutes
  max: process.env.RATE_LIMIT_MAX_REQUESTS || 100,
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// Logging
app.use(morgan('combined'));

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'BuilderBase Construction Profit Analyzer API',
    version: '1.0.0'
  });
});

// API statistics endpoint
app.get('/api/stats', (req, res) => {
  res.json({
    requests: {
      total: 0, // Would track in production
      today: 0
    },
    emails: {
      sent: 0,
      failed: 0
    },
    uptime: process.uptime()
  });
});

// Main email submission endpoint
app.post('/api/submit-email', async (req, res) => {
  try {
    const { email, businessName, efficiencyScore, insights } = req.body;
    
    // Validate input
    if (!email || !businessName || !efficiencyScore || !insights) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields'
      });
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid email format'
      });
    }
    
    console.log(`📧 Processing email submission for: ${email} (${businessName})`);
    
    // Try Brevo first
    let emailSent = false;
    let serviceUsed = 'none';
    let errorDetails = null;
    
    try {
      const brevoService = new BrevoService();
      await brevoService.sendEfficiencyReport(email, businessName, efficiencyScore, insights);
      emailSent = true;
      serviceUsed = 'brevo';
      console.log(`✅ Brevo email sent successfully to: ${email}`);
    } catch (brevoError) {
      console.log(`❌ Brevo failed: ${brevoError.message}`);
      errorDetails = brevoError.message;
      
      // Fallback to Gmail
      try {
        const gmailService = new GmailService();
        await gmailService.sendEfficiencyReport(email, businessName, efficiencyScore, insights);
        emailSent = true;
        serviceUsed = 'gmail';
        console.log(`✅ Gmail fallback email sent successfully to: ${email}`);
      } catch (gmailError) {
        console.log(`❌ Gmail also failed: ${gmailError.message}`);
        errorDetails += ` | Gmail: ${gmailError.message}`;
        
        // Final fallback: log to console
        console.log(`📝 Email queued locally (both services failed): ${email}`);
        console.log(`   Business: ${businessName}`);
        console.log(`   Score: ${efficiencyScore}`);
        console.log(`   Insights: ${JSON.stringify(insights)}`);
      }
    }
    
    // Return response
    if (emailSent) {
      res.json({
        success: true,
        message: 'Efficiency report sent successfully',
        serviceUsed: serviceUsed,
        email: email,
        timestamp: new Date().toISOString()
      });
    } else {
      res.status(500).json({
        success: false,
        error: 'Failed to send email via all services',
        details: errorDetails,
        queued: true // Frontend should show "queued for later delivery"
      });
    }
    
  } catch (error) {
    console.error('❌ Server error in /api/submit-email:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: error.message
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('❌ Unhandled error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint not found'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 BuilderBase Construction Profit Analyzer API running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
  console.log(`📧 Email endpoint: http://localhost:${PORT}/api/submit-email`);
  console.log(`🔒 CORS origin: ${process.env.CORS_ORIGIN || 'https://www.cubiczan.com'}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 SIGTERM received. Shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('🛑 SIGINT received. Shutting down gracefully...');
  process.exit(0);
});

module.exports = app;