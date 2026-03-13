/**
 * Gmail Backup Service for BuilderBase Construction Profit Analyzer
 * Fallback email service when Brevo fails
 */

const nodemailer = require('nodemailer');

class GmailService {
  constructor() {
    // Create transporter with primary Gmail account
    this.transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.GMAIL_USER || 'sam@cubiczan.com',
        pass: process.env.GMAIL_APP_PASSWORD
      }
    });

    // Backup transporter (optional)
    if (process.env.GMAIL_BACKUP_USER && process.env.GMAIL_BACKUP_PASSWORD) {
      this.backupTransporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
          user: process.env.GMAIL_BACKUP_USER,
          pass: process.env.GMAIL_BACKUP_PASSWORD
        }
      });
    }
  }

  /**
   * Test Gmail connection
   */
  async testConnection() {
    try {
      await this.transporter.verify();
      return {
        success: true,
        service: 'Gmail SMTP',
        user: process.env.GMAIL_USER || 'sam@cubiczan.com'
      };
    } catch (error) {
      console.error('❌ Gmail connection test failed:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Send construction efficiency report email via Gmail
   */
  async sendEfficiencyReport(email, businessName, efficiencyScore, insights) {
    try {
      // Try primary Gmail account first
      return await this.sendWithTransporter(
        this.transporter,
        email,
        businessName,
        efficiencyScore,
        insights,
        'primary'
      );
    } catch (primaryError) {
      console.log(`❌ Primary Gmail failed: ${primaryError.message}`);
      
      // Try backup Gmail if available
      if (this.backupTransporter) {
        try {
          return await this.sendWithTransporter(
            this.backupTransporter,
            email,
            businessName,
            efficiencyScore,
            insights,
            'backup'
          );
        } catch (backupError) {
          console.log(`❌ Backup Gmail also failed: ${backupError.message}`);
          throw new Error(`Both Gmail accounts failed: ${primaryError.message} | ${backupError.message}`);
        }
      } else {
        throw primaryError;
      }
    }
  }

  /**
   * Send email using specific transporter
   */
  async sendWithTransporter(transporter, email, businessName, efficiencyScore, insights, accountType) {
    const scoreLabel = this.getScoreLabel(efficiencyScore);
    
    const mailOptions = {
      from: `"BuilderBase Team" <${accountType === 'primary' ? process.env.GMAIL_USER : process.env.GMAIL_BACKUP_USER}>`,
      to: email,
      subject: `Your Construction Profit Analysis: ${efficiencyScore}/100`,
      text: this.generateEmailText(businessName, efficiencyScore, insights),
      html: this.generateEmailHtml(businessName, efficiencyScore, insights)
    };

    const result = await transporter.sendMail(mailOptions);
    console.log(`✅ Gmail (${accountType}) email sent to ${email}, message ID: ${result.messageId}`);
    return result;
  }

  /**
   * Generate HTML email content
   */
  generateEmailHtml(businessName, efficiencyScore, insights) {
    const scoreLabel = this.getScoreLabel(efficiencyScore);
    
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>Your Construction Profit Analysis</title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
          .content { background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }
          .score { font-size: 48px; font-weight: bold; color: #2c3e50; text-align: center; margin: 20px 0; }
          .score-label { font-size: 18px; color: #666; text-align: center; margin-bottom: 30px; }
          .insight { background: white; padding: 15px; margin: 15px 0; border-left: 4px solid #4ca1af; border-radius: 5px; }
          .cta-button { display: inline-block; background: linear-gradient(135deg, #4ca1af 0%, #2c3e50 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }
          .footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px; }
          .note { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 15px 0; font-size: 14px; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>BuilderBase Construction Profit Analysis</h1>
          <p>Personalized insights for ${businessName}</p>
        </div>
        
        <div class="content">
          <div class="note">
            <strong>Note:</strong> This email was sent via Gmail backup service. Our primary email system experienced a temporary issue.
          </div>
          
          <h2>Your Construction Efficiency Score</h2>
          <div class="score">${efficiencyScore}/100</div>
          <div class="score-label">${scoreLabel}</div>
          
          <h3>Key Insights for Improvement:</h3>
          ${insights.map(insight => `<div class="insight">${insight}</div>`).join('')}
          
          <p>Based on your current processes, we estimate you could increase profitability by <strong>15-25%</strong> with better project management tools.</p>
          
          <p><strong>BuilderBase can help you:</strong></p>
          <ul>
            <li>Track projects in real-time</li>
            <li>Automate client communication</li>
            <li>Manage change orders digitally</li>
            <li>Reduce administrative time by 10+ hours/week</li>
            <li>Increase profit margins by 5-15%</li>
          </ul>
          
          <center>
            <a href="${process.env.FRONTEND_URL || 'https://www.cubiczan.com/construction-profit'}" class="cta-button">
              Explore BuilderBase Solutions
            </a>
          </center>
          
          <div class="footer">
            <p>This analysis was generated by BuilderBase Construction Profit Analyzer.</p>
            <p>© ${new Date().getFullYear()} BuilderBase. All rights reserved.</p>
            <p><a href="${process.env.FRONTEND_URL || 'https://www.cubiczan.com/construction-profit'}/unsubscribe">Unsubscribe</a></p>
          </div>
        </div>
      </body>
      </html>
    `;
  }

  /**
   * Generate plain text email content
   */
  generateEmailText(businessName, efficiencyScore, insights) {
    const scoreLabel = this.getScoreLabel(efficiencyScore);
    
    return `
BUILDERBASE CONSTRUCTION PROFIT ANALYSIS
========================================

Note: This email was sent via Gmail backup service. Our primary email system experienced a temporary issue.

Business: ${businessName}
Efficiency Score: ${efficiencyScore}/100
Rating: ${scoreLabel}

KEY INSIGHTS:
${insights.map((insight, i) => `${i + 1}. ${insight}`).join('\n')}

Based on your current processes, we estimate you could increase profitability by 15-25% with better project management tools.

BuilderBase can help you:
- Track projects in real-time
- Automate client communication
- Manage change orders digitally
- Reduce administrative time by 10+ hours/week
- Increase profit margins by 5-15%

Explore BuilderBase Solutions:
${process.env.FRONTEND_URL || 'https://www.cubiczan.com/construction-profit'}

---
This analysis was generated by BuilderBase Construction Profit Analyzer.
© ${new Date().getFullYear()} BuilderBase. All rights reserved.
To unsubscribe: ${process.env.FRONTEND_URL || 'https://www.cubiczan.com/construction-profit'}/unsubscribe
    `;
  }

  /**
   * Get label for efficiency score
   */
  getScoreLabel(score) {
    if (score >= 80) return 'Excellent - Well optimized!';
    if (score >= 60) return 'Good - Room for improvement';
    if (score >= 40) return 'Average - Significant opportunities';
    return 'Needs improvement - High potential for growth';
  }
}

module.exports = GmailService;