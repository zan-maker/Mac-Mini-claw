/**
 * Brevo Service for BuilderBase Construction Profit Analyzer
 * Handles email sending and contact management via Brevo API
 */

const SibApiV3Sdk = require('sib-api-v3-sdk');

class BrevoService {
  constructor() {
    // Configure Brevo API
    const defaultClient = SibApiV3Sdk.ApiClient.instance;
    const apiKey = defaultClient.authentications['api-key'];
    apiKey.apiKey = process.env.BREVO_API_KEY;
    
    this.apiInstance = new SibApiV3Sdk.TransactionalEmailsApi();
    this.contactsApi = new SibApiV3Sdk.ContactsApi();
  }

  /**
   * Test Brevo connection
   */
  async testConnection() {
    try {
      const defaultClient = SibApiV3Sdk.ApiClient.instance;
      const apiKey = defaultClient.authentications['api-key'];
      apiKey.apiKey = process.env.BREVO_API_KEY;
      
      const accountApi = new SibApiV3Sdk.AccountApi();
      const account = await accountApi.getAccount();
      
      return {
        success: true,
        email: account.email,
        plan: account.plan[0].type,
        credits: account.plan[0].credits
      };
    } catch (error) {
      console.error('❌ Brevo connection test failed:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Send construction efficiency report email
   */
  async sendEfficiencyReport(email, businessName, efficiencyScore, insights) {
    try {
      // Create or update contact in Brevo
      await this.createOrUpdateContact(email, businessName, efficiencyScore);
      
      // Prepare email data
      const sendSmtpEmail = new SibApiV3Sdk.SendSmtpEmail();
      
      sendSmtpEmail.to = [{
        email: email,
        name: businessName
      }];
      
      sendSmtpEmail.sender = {
        email: process.env.BREVO_SENDER_EMAIL || 'sam@cubiczan.com',
        name: process.env.BREVO_SENDER_NAME || 'BuilderBase Team'
      };
      
      sendSmtpEmail.subject = `Your Construction Profit Analysis: ${efficiencyScore}/100`;
      
      // Use template if available, otherwise send plain email
      if (process.env.BREVO_TEMPLATE_ID) {
        sendSmtpEmail.templateId = parseInt(process.env.BREVO_TEMPLATE_ID);
        sendSmtpEmail.params = {
          BUSINESS_NAME: businessName,
          EFFICIENCY_SCORE: efficiencyScore,
          SCORE_LABEL: this.getScoreLabel(efficiencyScore),
          INSIGHT_1: insights[0] || 'Digital project tracking could save 10+ hours/week',
          INSIGHT_2: insights[1] || 'Automated client communication reduces misunderstandings',
          INSIGHT_3: insights[2] || 'Integrated change order system prevents budget overruns',
          REPORT_LINK: `${process.env.FRONTEND_URL || 'https://www.cubiczan.com/construction-profit'}/report`,
          CALCULATOR_LINK: process.env.FRONTEND_URL || 'https://www.cubiczan.com/construction-profit',
          UNSUBSCRIBE_LINK: `${process.env.FRONTEND_URL || 'https://www.cubiczan.com/construction-profit'}/unsubscribe`,
          CURRENT_YEAR: new Date().getFullYear()
        };
      } else {
        // Fallback to HTML email
        sendSmtpEmail.htmlContent = this.generateEmailHtml(businessName, efficiencyScore, insights);
        sendSmtpEmail.textContent = this.generateEmailText(businessName, efficiencyScore, insights);
      }
      
      // Send email
      const result = await this.apiInstance.sendTransacEmail(sendSmtpEmail);
      
      console.log(`✅ Brevo email sent to ${email}, message ID: ${result.messageId}`);
      return result;
      
    } catch (error) {
      console.error(`❌ Brevo email failed for ${email}:`, error.message);
      throw new Error(`Brevo email failed: ${error.message}`);
    }
  }

  /**
   * Create or update contact in Brevo
   */
  async createOrUpdateContact(email, businessName, efficiencyScore) {
    try {
      const createContact = new SibApiV3Sdk.CreateContact();
      
      createContact.email = email;
      createContact.attributes = {
        FIRSTNAME: businessName.split(' ')[0] || businessName,
        LASTNAME: businessName.split(' ').slice(1).join(' ') || 'Construction',
        COMPANY: businessName,
        EFFICIENCY_SCORE: efficiencyScore.toString(),
        INDUSTRY: 'Construction',
        SOURCE: 'BuilderBase Profit Analyzer',
        SIGNUP_DATE: new Date().toISOString()
      };
      
      // Add to list if list ID is configured
      if (process.env.BREVO_LIST_ID) {
        createContact.listIds = [parseInt(process.env.BREVO_LIST_ID)];
      }
      
      await this.contactsApi.createContact(createContact);
      console.log(`✅ Brevo contact created/updated: ${email}`);
      
    } catch (error) {
      // Contact might already exist, that's okay
      if (error.response && error.response.text && error.response.text.includes('Contact already exist')) {
        console.log(`ℹ️ Brevo contact already exists: ${email}`);
      } else {
        console.error(`❌ Brevo contact creation failed for ${email}:`, error.message);
        // Don't throw - email sending can still proceed
      }
    }
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
        </style>
      </head>
      <body>
        <div class="header">
          <h1>BuilderBase Construction Profit Analysis</h1>
          <p>Personalized insights for ${businessName}</p>
        </div>
        
        <div class="content">
          <h2>Your Construction Efficiency Score</h2>
          <div class="score">${efficiencyScore}/100</div>
          <div class="score-label">${scoreLabel}</div>
          
          <h3>Key Insights for Improvement:</h3>
          ${insights.map(insight => `<div class="insight">${insight}</div>`).join('')}
          
          <p>Based on your current processes, we estimate you could increase profitability by <strong>15-25%</strong> with better project management tools.</p>
          
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

Business: ${businessName}
Efficiency Score: ${efficiencyScore}/100
Rating: ${scoreLabel}

KEY INSIGHTS:
${insights.map((insight, i) => `${i + 1}. ${insight}`).join('\n')}

Based on your current processes, we estimate you could increase profitability by 15-25% with better project management tools.

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

module.exports = BrevoService;