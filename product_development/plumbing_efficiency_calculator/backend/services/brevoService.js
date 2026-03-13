const SibApiV3Sdk = require('sib-api-v3-sdk');
require('dotenv').config();

class BrevoService {
    constructor() {
        // Configure API key
        const defaultClient = SibApiV3Sdk.ApiClient.instance;
        const apiKey = defaultClient.authentications['api-key'];
        apiKey.apiKey = process.env.BREVO_API_KEY;
        
        this.apiInstance = new SibApiV3Sdk.TransactionalEmailsApi();
        this.contactsApi = new SibApiV3Sdk.ContactsApi();
        
        // Sender information
        this.sender = {
            name: 'Plumbing Efficiency Calculator',
            email: 'noreply@cubiczan.com'
        };
        
        // Template IDs (configure in Brevo dashboard)
        this.templateIds = {
            efficiencyReport: parseInt(process.env.BREVO_TEMPLATE_ID) || 1
        };
    }
    
    async sendEfficiencyReport(email, businessName, efficiencyScore, insights = []) {
        try {
            // First, add contact to Brevo list
            await this.addContact(email, businessName, efficiencyScore);
            
            // Prepare email parameters
            const params = {
                BUSINESS_NAME: businessName || 'Plumbing Business',
                EFFICIENCY_SCORE: efficiencyScore || 0,
                SCORE_LABEL: this.getScoreLabel(efficiencyScore),
                INSIGHT_1: insights[0] || 'Consider digital scheduling to reduce admin time',
                INSIGHT_2: insights[1] || 'Automated invoicing could speed up payments',
                INSIGHT_3: insights[2] || 'Customer communication tools reduce no-shows',
                REPORT_LINK: `https://www.cubiczan.com/reports/${this.generateReportId(email)}`,
                CALCULATOR_LINK: 'https://www.cubiczan.com/plumbing-efficiency',
                UNSUBSCRIBE_LINK: `https://www.cubiczan.com/unsubscribe/${this.generateUnsubscribeId(email)}`,
                CURRENT_YEAR: new Date().getFullYear()
            };
            
            // Send transactional email
            const sendSmtpEmail = {
                to: [{
                    email: email,
                    name: businessName || 'Plumbing Business Owner'
                }],
                sender: this.sender,
                replyTo: {
                    email: 'sam@cubiczan.com',
                    name: 'Sam Desigan'
                },
                templateId: this.templateIds.efficiencyReport,
                params: params,
                headers: {
                    'X-Mailin-custom': 'plumbing-efficiency-calculator',
                    'charset': 'iso-8859-1'
                }
            };
            
            console.log('Sending Brevo email to:', email);
            const result = await this.apiInstance.sendTransacEmail(sendSmtpEmail);
            
            console.log('Brevo email sent successfully:', result.messageId);
            return result;
            
        } catch (error) {
            console.error('Brevo email sending failed:', error);
            throw new Error(`Brevo failed: ${error.message}`);
        }
    }
    
    async addContact(email, businessName, efficiencyScore) {
        try {
            const createContact = new SibApiV3Sdk.CreateContact();
            
            createContact.email = email;
            createContact.attributes = {
                FIRSTNAME: businessName ? businessName.split(' ')[0] : 'Business',
                LASTNAME: businessName ? businessName.split(' ').slice(1).join(' ') : 'Owner',
                BUSINESS: businessName || 'Plumbing Business',
                EFFICIENCY_SCORE: efficiencyScore || 0,
                SOURCE: 'Plumbing Efficiency Calculator',
                OPT_IN: true,
                OPT_IN_DATE: new Date().toISOString()
            };
            
            createContact.listIds = [parseInt(process.env.BREVO_LIST_ID) || 2];
            createContact.updateEnabled = true;
            
            console.log('Adding contact to Brevo:', email);
            await this.contactsApi.createContact(createContact);
            console.log('Contact added successfully');
            
        } catch (error) {
            // Contact might already exist, that's okay
            if (error.response && error.response.text && error.response.text.includes('already exists')) {
                console.log('Contact already exists in Brevo, updating...');
                await this.updateContact(email, businessName, efficiencyScore);
            } else {
                console.warn('Failed to add/update Brevo contact:', error.message);
                // Don't throw - email sending might still work
            }
        }
    }
    
    async updateContact(email, businessName, efficiencyScore) {
        try {
            const updateContact = new SibApiV3Sdk.UpdateContact();
            
            updateContact.attributes = {
                BUSINESS: businessName || 'Plumbing Business',
                EFFICIENCY_SCORE: efficiencyScore || 0,
                LAST_CALCULATED: new Date().toISOString()
            };
            
            await this.contactsApi.updateContact(email, updateContact);
            console.log('Contact updated successfully');
            
        } catch (error) {
            console.warn('Failed to update Brevo contact:', error.message);
        }
    }
    
    getScoreLabel(score) {
        if (score >= 80) return 'Excellent Efficiency';
        if (score >= 60) return 'Good Efficiency';
        if (score >= 40) return 'Average Efficiency';
        return 'Needs Improvement';
    }
    
    generateReportId(email) {
        // Generate a unique report ID
        const timestamp = Date.now();
        const hash = require('crypto')
            .createHash('md5')
            .update(email + timestamp)
            .digest('hex')
            .substring(0, 8);
        return `${hash}-${timestamp}`;
    }
    
    generateUnsubscribeId(email) {
        // Generate unsubscribe ID
        return require('crypto')
            .createHash('sha256')
            .update(email + process.env.UNSUBSCRIBE_SECRET || 'secret')
            .digest('hex')
            .substring(0, 16);
    }
    
    // Test connection
    async testConnection() {
        try {
            const account = new SibApiV3Sdk.AccountApi();
            const result = await account.getAccount();
            return {
                success: true,
                plan: result.plan[0].type,
                credits: result.plan[0].credits,
                email: result.email
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
}

module.exports = BrevoService;