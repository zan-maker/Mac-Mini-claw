const nodemailer = require('nodemailer');
require('dotenv').config();

class GmailService {
    constructor() {
        // Configure Gmail transporter
        this.transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.GMAIL_USER || 'sam@cubiczan.com',
                pass: process.env.GMAIL_PASSWORD || process.env.GMAIL_APP_PASSWORD
            },
            tls: {
                rejectUnauthorized: false
            }
        });
        
        // Sender information
        this.sender = {
            name: 'Plumbing Efficiency Calculator',
            email: process.env.GMAIL_USER || 'sam@cubiczan.com'
        };
    }
    
    async sendEfficiencyReport(email, businessName, efficiencyScore, insights = []) {
        try {
            // Generate report content
            const reportContent = this.generateReportContent(businessName, efficiencyScore, insights);
            
            // Prepare email
            const mailOptions = {
                from: this.sender,
                to: email,
                replyTo: 'sam@cubiczan.com',
                subject: `Your Plumbing Business Efficiency Report - Score: ${efficiencyScore}/100`,
                html: reportContent.html,
                text: reportContent.text,
                headers: {
                    'X-Mailer': 'Plumbing Efficiency Calculator',
                    'X-Priority': '1',
                    'Importance': 'high'
                }
            };
            
            console.log('Sending Gmail email to:', email);
            const result = await this.transporter.sendMail(mailOptions);
            
            console.log('Gmail email sent successfully:', result.messageId);
            return result;
            
        } catch (error) {
            console.error('Gmail email sending failed:', error);
            throw new Error(`Gmail failed: ${error.message}`);
        }
    }
    
    generateReportContent(businessName, efficiencyScore, insights) {
        const scoreLabel = this.getScoreLabel(efficiencyScore);
        const currentDate = new Date().toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        // HTML content
        const html = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Plumbing Business Efficiency Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: #f8fafc;
        }
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            border-radius: 10px 10px 0 0;
            text-align: center;
        }
        .content {
            background: white;
            padding: 30px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .score {
            font-size: 48px;
            font-weight: 900;
            text-align: center;
            margin: 20px 0;
            color: ${this.getScoreColor(efficiencyScore)};
        }
        .insight {
            background: #f1f5f9;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
        }
        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            margin: 20px 0;
            text-align: center;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            color: #718096;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Your Plumbing Business Efficiency Report</h1>
        <p>Generated on ${currentDate}</p>
    </div>
    
    <div class="content">
        <h2>Hello ${businessName || 'Plumbing Business Owner'},</h2>
        
        <p>Thank you for using our Plumbing Business Efficiency Calculator. Here's your personalized analysis:</p>
        
        <div class="score">${efficiencyScore}/100</div>
        <h3 style="text-align: center; color: ${this.getScoreColor(efficiencyScore)};">${scoreLabel}</h3>
        
        <h3>Key Insights:</h3>
        ${insights.map(insight => `<div class="insight">${insight}</div>`).join('')}
        
        ${insights.length === 0 ? `
        <div class="insight">Consider implementing digital scheduling to reduce administrative time by 40-60%.</div>
        <div class="insight">Automated invoicing could speed up payments from 30+ days to 7-14 days.</div>
        <div class="insight">Customer communication tools can reduce no-shows by up to 60%.</div>
        ` : ''}
        
        <h3>Next Steps:</h3>
        <ol>
            <li>Review your efficiency score against industry benchmarks</li>
            <li>Implement the top 1-2 recommendations from your insights</li>
            <li>Track improvements over the next 30 days</li>
            <li>Consider specialized tools for plumbing businesses</li>
        </ol>
        
        <div style="text-align: center;">
            <a href="https://www.cubiczan.com/plumbing-efficiency" class="cta-button">
                View Detailed Recommendations →
            </a>
        </div>
        
        <div class="footer">
            <p><strong>www.cubiczan.com</strong><br>
            Helping plumbing businesses thrive through technology and efficiency.</p>
            
            <p>This report was generated by the Plumbing Business Efficiency Calculator.<br>
            If you no longer wish to receive these reports, please <a href="https://www.cubiczan.com/unsubscribe">unsubscribe here</a>.</p>
            
            <p>© ${new Date().getFullYear()} www.cubiczan.com. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
        `;
        
        // Plain text content
        const text = `
YOUR PLUMBING BUSINESS EFFICIENCY REPORT
=========================================

Generated on: ${currentDate}

Hello ${businessName || 'Plumbing Business Owner'},

Thank you for using our Plumbing Business Efficiency Calculator. Here's your personalized analysis:

Efficiency Score: ${efficiencyScore}/100
Score Rating: ${scoreLabel}

KEY INSIGHTS:
${insights.map((insight, i) => `${i + 1}. ${insight}`).join('\n')}

${insights.length === 0 ? `
1. Consider implementing digital scheduling to reduce administrative time by 40-60%.
2. Automated invoicing could speed up payments from 30+ days to 7-14 days.
3. Customer communication tools can reduce no-shows by up to 60%.
` : ''}

NEXT STEPS:
1. Review your efficiency score against industry benchmarks
2. Implement the top 1-2 recommendations from your insights
3. Track improvements over the next 30 days
4. Consider specialized tools for plumbing businesses

View detailed recommendations: https://www.cubiczan.com/plumbing-efficiency

--
www.cubiczan.com
Helping plumbing businesses thrive through technology and efficiency.

This report was generated by the Plumbing Business Efficiency Calculator.
If you no longer wish to receive these reports, please unsubscribe: https://www.cubiczan.com/unsubscribe

© ${new Date().getFullYear()} www.cubiczan.com. All rights reserved.
        `;
        
        return { html, text };
    }
    
    getScoreLabel(score) {
        if (score >= 80) return 'Excellent Efficiency';
        if (score >= 60) return 'Good Efficiency';
        if (score >= 40) return 'Average Efficiency';
        return 'Needs Improvement';
    }
    
    getScoreColor(score) {
        if (score >= 80) return '#10b981';
        if (score >= 60) return '#3b82f6';
        if (score >= 40) return '#f59e0b';
        return '#ef4444';
    }
    
    // Test connection
    async testConnection() {
        try {
            await this.transporter.verify();
            return {
                success: true,
                service: 'gmail',
                user: process.env.GMAIL_USER || 'sam@cubiczan.com'
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
}

module.exports = GmailService;