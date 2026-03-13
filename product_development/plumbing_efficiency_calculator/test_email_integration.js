#!/usr/bin/env node
/**
 * Test script for Plumbing Efficiency Calculator email integration
 * Tests Brevo + Gmail email services
 */

require('dotenv').config({ path: './backend/.env' });

const BrevoService = require('./backend/services/brevoService');
const GmailService = require('./backend/services/gmailService');

async function testEmailIntegration() {
    console.log('🔧 TESTING EMAIL INTEGRATION');
    console.log('============================\n');
    
    // Test Brevo service
    console.log('1. Testing Brevo Service...');
    const brevoService = new BrevoService();
    
    try {
        const brevoTest = await brevoService.testConnection();
        if (brevoTest.success) {
            console.log('✅ Brevo connection successful');
            console.log(`   Plan: ${brevoTest.plan}`);
            console.log(`   Credits: ${brevoTest.credits}`);
            console.log(`   Email: ${brevoTest.email}`);
        } else {
            console.log('❌ Brevo connection failed:', brevoTest.error);
        }
    } catch (error) {
        console.log('❌ Brevo test error:', error.message);
    }
    
    console.log('\n2. Testing Gmail Service...');
    const gmailService = new GmailService();
    
    try {
        const gmailTest = await gmailService.testConnection();
        if (gmailTest.success) {
            console.log('✅ Gmail connection successful');
            console.log(`   Service: ${gmailTest.service}`);
            console.log(`   User: ${gmailTest.user}`);
        } else {
            console.log('❌ Gmail connection failed:', gmailTest.error);
        }
    } catch (error) {
        console.log('❌ Gmail test error:', error.message);
    }
    
    console.log('\n3. Testing Email Sending...');
    console.log('   Sending test email to sam@cubiczan.com');
    
    const testEmail = 'sam@cubiczan.com';
    const testBusiness = 'Test Plumbing Business';
    const testScore = 75;
    const testInsights = [
        'Test insight 1: Digital scheduling recommended',
        'Test insight 2: Automated invoicing available',
        'Test insight 3: Customer portal would help'
    ];
    
    // Try Brevo first
    let emailSent = false;
    let serviceUsed = 'none';
    
    try {
        console.log('   Trying Brevo...');
        await brevoService.sendEfficiencyReport(testEmail, testBusiness, testScore, testInsights);
        emailSent = true;
        serviceUsed = 'brevo';
        console.log('   ✅ Brevo email sent successfully');
    } catch (brevoError) {
        console.log('   ❌ Brevo failed:', brevoError.message);
        
        // Fallback to Gmail
        try {
            console.log('   Trying Gmail fallback...');
            await gmailService.sendEfficiencyReport(testEmail, testBusiness, testScore, testInsights);
            emailSent = true;
            serviceUsed = 'gmail';
            console.log('   ✅ Gmail email sent successfully');
        } catch (gmailError) {
            console.log('   ❌ Gmail also failed:', gmailError.message);
        }
    }
    
    console.log('\n📊 TEST RESULTS');
    console.log('==============');
    console.log(`Email sending: ${emailSent ? '✅ SUCCESS' : '❌ FAILED'}`);
    console.log(`Service used: ${serviceUsed}`);
    console.log(`Test email: ${testEmail}`);
    console.log(`Business: ${testBusiness}`);
    console.log(`Score: ${testScore}`);
    
    if (emailSent) {
        console.log('\n🎉 Email integration test PASSED!');
        console.log('The Plumbing Efficiency Calculator is ready to send emails.');
    } else {
        console.log('\n⚠️  Email integration test FAILED!');
        console.log('Please check your configuration:');
        console.log('1. Verify Brevo API key in .env file');
        console.log('2. Check Gmail credentials');
        console.log('3. Ensure internet connectivity');
        process.exit(1);
    }
}

// Run test
testEmailIntegration().catch(error => {
    console.error('Test failed with error:', error);
    process.exit(1);
});