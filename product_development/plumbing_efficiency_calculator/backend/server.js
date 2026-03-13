const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Email service imports
const BrevoService = require('./services/brevoService');
const GmailService = require('./services/gmailService');

// Initialize email services
const brevoService = new BrevoService();
const gmailService = new GmailService();

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy',
        timestamp: new Date().toISOString(),
        services: {
            brevo: 'configured',
            gmail: 'configured'
        }
    });
});

// Submit email endpoint
app.post('/api/submit-email', async (req, res) => {
    try {
        const { email, businessName, efficiencyScore, insights } = req.body;
        
        // Validate input
        if (!email || !validateEmail(email)) {
            return res.status(400).json({ 
                success: false, 
                error: 'Valid email address is required' 
            });
        }
        
        // Create lead record
        const leadData = {
            email,
            businessName: businessName || 'Plumbing Business',
            efficiencyScore: efficiencyScore || 0,
            insights: insights || [],
            timestamp: new Date().toISOString(),
            ipAddress: req.ip,
            userAgent: req.get('User-Agent')
        };
        
        console.log('New lead submission:', leadData);
        
        // Try Brevo first
        let emailSent = false;
        let emailService = 'none';
        let emailError = null;
        
        try {
            console.log('Attempting to send email via Brevo...');
            await brevoService.sendEfficiencyReport(email, businessName, efficiencyScore, insights);
            emailSent = true;
            emailService = 'brevo';
            console.log('Brevo email sent successfully');
        } catch (brevoError) {
            console.error('Brevo failed:', brevoError.message);
            emailError = brevoError.message;
            
            // Fallback to Gmail SMTP
            try {
                console.log('Falling back to Gmail SMTP...');
                await gmailService.sendEfficiencyReport(email, businessName, efficiencyScore, insights);
                emailSent = true;
                emailService = 'gmail';
                console.log('Gmail email sent successfully');
            } catch (gmailError) {
                console.error('Gmail also failed:', gmailError.message);
                emailError = gmailError.message;
            }
        }
        
        // Prepare response
        const response = {
            success: emailSent,
            message: emailSent 
                ? 'Efficiency report sent successfully!' 
                : 'Failed to send email. Please try again later.',
            data: {
                email,
                businessName,
                efficiencyScore,
                emailService,
                timestamp: new Date().toISOString()
            }
        };
        
        if (!emailSent) {
            response.error = emailError;
        }
        
        // Log the submission (in production, save to database)
        logSubmission(leadData, emailSent, emailService, emailError);
        
        res.json(response);
        
    } catch (error) {
        console.error('Error in submit-email endpoint:', error);
        res.status(500).json({ 
            success: false, 
            error: 'Internal server error',
            message: error.message 
        });
    }
});

// Get statistics endpoint
app.get('/api/stats', (req, res) => {
    // In production, this would query a database
    const stats = {
        totalSubmissions: 12500,
        averageScore: 67,
        conversionRate: '32%',
        businessesHelped: '12,500+',
        timestamp: new Date().toISOString()
    };
    
    res.json({ success: true, data: stats });
});

// Validate email function
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Log submission function
function logSubmission(leadData, emailSent, emailService, error) {
    const logEntry = {
        ...leadData,
        emailSent,
        emailService,
        error: error || null,
        logTimestamp: new Date().toISOString()
    };
    
    // In production, save to database
    console.log('Lead logged:', JSON.stringify(logEntry, null, 2));
    
    // Also log to file in development
    if (process.env.NODE_ENV !== 'production') {
        const fs = require('fs');
        const logFile = 'leads.log';
        fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
    }
}

// Start server
app.listen(PORT, () => {
    console.log(`Plumbing Efficiency Calculator backend running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`Brevo API Key: ${process.env.BREVO_API_KEY ? 'Configured' : 'Missing'}`);
    console.log(`Gmail configured: ${process.env.GMAIL_USER ? 'Yes' : 'No'}`);
});