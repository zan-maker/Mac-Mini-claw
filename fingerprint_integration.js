#!/usr/bin/env node
/**
 * Browser Fingerprinting Integration
 * Using Apify Fingerprint Suite with Playwright/Puppeteer
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { newInjectedContext } = require('fingerprint-injector');

class FingerprintIntegration {
    constructor(configPath) {
        this.configPath = configPath;
        this.config = this.loadConfig();
        this.resultsDir = path.join(__dirname, 'results/fingerprinting');
        
        // Ensure results directory exists
        if (!fs.existsSync(this.resultsDir)) {
            fs.mkdirSync(this.resultsDir, { recursive: true });
        }
        
        console.log('🕵️ Browser Fingerprinting Integration Initialized');
        console.log(`📁 Config: ${this.configPath}`);
        console.log(`📊 Results: ${this.resultsDir}`);
    }
    
    loadConfig() {
        try {
            const configData = fs.readFileSync(this.configPath, 'utf8');
            return JSON.parse(configData);
        } catch (error) {
            console.error('❌ Failed to load config:', error.message);
            return this.getDefaultConfig();
        }
    }
    
    getDefaultConfig() {
        return {
            fingerprinting: {
                enabled: true,
                strategies: {
                    random_fingerprint: true,
                    device_specific: true,
                    geolocation_spoofing: true
                },
                devices: ['desktop', 'mobile'],
                operatingSystems: ['windows', 'macos', 'linux'],
                browsers: ['chrome', 'firefox', 'safari']
            },
            scraping_profiles: {
                stealth: {
                    fingerprint_rotation: 'every_request',
                    use_proxies: true,
                    delay_between_requests: '2-5s'
                },
                balanced: {
                    fingerprint_rotation: 'session',
                    use_proxies: false,
                    delay_between_requests: '1-3s'
                }
            }
        };
    }
    
    async testFingerprintInjection() {
        console.log('🧪 Testing fingerprint injection...');
        
        try {
            const browser = await chromium.launch({ 
                headless: false,
                args: ['--disable-blink-features=AutomationControlled']
            });
            
            // Create context with injected fingerprint
            const context = await newInjectedContext(browser, {
                fingerprintOptions: {
                    devices: ['desktop'],
                    operatingSystems: ['macos'],
                    browsers: ['chrome'],
                    locales: ['en-US']
                },
                newContextOptions: {
                    viewport: { width: 1920, height: 1080 },
                    geolocation: {
                        latitude: 40.7128,
                        longitude: -74.0060
                    },
                    timezoneId: 'America/New_York'
                }
            });
            
            const page = await context.newPage();
            
            // Navigate to fingerprint test site
            console.log('🌐 Navigating to fingerprint test site...');
            await page.goto('https://bot.sannysoft.com');
            
            // Take screenshot
            const screenshotPath = path.join(this.resultsDir, 'fingerprint_test.png');
            await page.screenshot({ path: screenshotPath, fullPage: true });
            console.log(`📸 Screenshot saved: ${screenshotPath}`);
            
            // Wait for user to see results
            console.log('👀 Check the browser window for fingerprint test results');
            console.log('⏳ Waiting 30 seconds for manual verification...');
            await new Promise(resolve => setTimeout(resolve, 30000));
            
            await browser.close();
            console.log('✅ Fingerprint injection test complete');
            
            return true;
            
        } catch (error) {
            console.error('❌ Fingerprint injection test failed:', error);
            return false;
        }
    }
    
    async createStealthScraper(profile = 'balanced') {
        console.log(`🛡️ Creating stealth scraper (Profile: ${profile})`);
        
        const profileConfig = this.config.scraping_profiles[profile] || 
                             this.config.scraping_profiles.balanced;
        
        const browser = await chromium.launch({ 
            headless: true,  // Change to false for debugging
            args: [
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        });
        
        const context = await newInjectedContext(browser, {
            fingerprintOptions: {
                devices: ['desktop'],
                operatingSystems: ['windows', 'macos'],
                browsers: ['chrome', 'firefox'],
                locales: ['en-US', 'en-GB']
            },
            newContextOptions: {
                viewport: { width: 1366, height: 768 },
                userAgent: this.generateUserAgent(),
                javaScriptEnabled: true,
                bypassCSP: true
            }
        });
        
        console.log('✅ Stealth scraper created with fingerprint injection');
        
        return {
            browser,
            context,
            profile: profileConfig,
            config: this.config
        };
    }
    
    generateUserAgent() {
        const userAgents = [
            // Chrome on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            // Chrome on macOS
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            // Firefox on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            // Safari on macOS
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
        ];
        
        return userAgents[Math.floor(Math.random() * userAgents.length)];
    }
    
    async scrapeWithFingerprint(url, options = {}) {
        console.log(`🌐 Scraping with fingerprint: ${url}`);
        
        const {
            saveScreenshot = true,
            saveHTML = false,
            waitForSelector = null,
            timeout = 30000
        } = options;
        
        const scraper = await this.createStealthScraper('balanced');
        const page = await scraper.context.newPage();
        
        try {
            // Navigate to URL
            await page.goto(url, { 
                waitUntil: 'networkidle',
                timeout: timeout 
            });
            
            // Wait for optional selector
            if (waitForSelector) {
                await page.waitForSelector(waitForSelector, { timeout: 10000 });
            }
            
            // Get page content
            const content = await page.content();
            const title = await page.title();
            
            console.log(`✅ Successfully scraped: ${title}`);
            
            // Save results
            const timestamp = Date.now();
            const results = {
                url,
                title,
                timestamp,
                fingerprint: scraper.profile,
                content_length: content.length
            };
            
            const resultsPath = path.join(this.resultsDir, `scrape_${timestamp}.json`);
            fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));
            console.log(`📁 Results saved: ${resultsPath}`);
            
            // Save screenshot if requested
            if (saveScreenshot) {
                const screenshotPath = path.join(this.resultsDir, `screenshot_${timestamp}.png`);
                await page.screenshot({ path: screenshotPath, fullPage: true });
                console.log(`📸 Screenshot saved: ${screenshotPath}`);
            }
            
            // Save HTML if requested
            if (saveHTML) {
                const htmlPath = path.join(this.resultsDir, `page_${timestamp}.html`);
                fs.writeFileSync(htmlPath, content);
                console.log(`📄 HTML saved: ${htmlPath}`);
            }
            
            await scraper.browser.close();
            
            return {
                success: true,
                title,
                content,
                resultsPath,
                screenshotPath: saveScreenshot ? path.join(this.resultsDir, `screenshot_${timestamp}.png`) : null
            };
            
        } catch (error) {
            console.error('❌ Scraping failed:', error.message);
            
            // Save error screenshot
            const errorPath = path.join(this.resultsDir, `error_${Date.now()}.png`);
            await page.screenshot({ path: errorPath });
            console.log(`📸 Error screenshot: ${errorPath}`);
            
            await scraper.browser.close();
            
            return {
                success: false,
                error: error.message,
                errorScreenshot: errorPath
            };
        }
    }
    
    async runBatchScrape(urls, options = {}) {
        console.log(`📋 Batch scraping ${urls.length} URLs...`);
        
        const results = [];
        const delayBetweenRequests = options.delayBetweenRequests || 2000; // 2 seconds
        
        for (let i = 0; i < urls.length; i++) {
            const url = urls[i];
            console.log(`\n[${i + 1}/${urls.length}] Scraping: ${url}`);
            
            try {
                const result = await this.scrapeWithFingerprint(url, options);
                results.push(result);
                
                // Delay between requests (except last one)
                if (i < urls.length - 1) {
                    console.log(`⏳ Waiting ${delayBetweenRequests}ms before next request...`);
                    await new Promise(resolve => setTimeout(resolve, delayBetweenRequests));
                }
                
            } catch (error) {
                console.error(`❌ Failed to scrape ${url}:`, error.message);
                results.push({
                    url,
                    success: false,
                    error: error.message
                });
            }
        }
        
        // Save batch results
        const batchResultsPath = path.join(this.resultsDir, `batch_${Date.now()}.json`);
        fs.writeFileSync(batchResultsPath, JSON.stringify(results, null, 2));
        
        console.log(`\n📊 Batch scraping complete:`);
        console.log(`   Total URLs: ${urls.length}`);
        console.log(`   Successful: ${results.filter(r => r.success).length}`);
        console.log(`   Failed: ${results.filter(r => !r.success).length}`);
        console.log(`   Results: ${batchResultsPath}`);
        
        return results;
    }
}

// Command line interface
async function main() {
    console.log('🚀 Browser Fingerprinting Suite');
    console.log('='.repeat(60));
    
    const configPath = path.join(__dirname, 'config/fingerprinting_config.json');
    const fingerprint = new FingerprintIntegration(configPath);
    
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch (command) {
        case 'test':
            await fingerprint.testFingerprintInjection();
            break;
            
        case 'scrape':
            if (args.length < 2) {
                console.error('❌ Usage: node fingerprint_integration.js scrape <url>');
                process.exit(1);
            }
            const url = args[1];
            await fingerprint.scrapeWithFingerprint(url, {
                saveScreenshot: true,
                saveHTML: true
            });
            break;
            
        case 'batch':
            if (args.length < 2) {
                console.error('❌ Usage: node fingerprint_integration.js batch <urls_file>');
                process.exit(1);
            }
            const urlsFile = args[1];
            const urls = fs.readFileSync(urlsFile, 'utf8')
                .split('\n')
                .filter(url => url.trim() && url.startsWith('http'));
            
            await fingerprint.runBatchScrape(urls, {
                delayBetweenRequests: 3000
            });
            break;
            
        default:
            console.log('Available commands:');
            console.log('  test          - Test fingerprint injection');
            console.log('  scrape <url>  - Scrape single URL with fingerprint');
            console.log('  batch <file>  - Batch scrape URLs from file');
            console.log('\nExample:');
            console.log('  node fingerprint_integration.js test');
            console.log('  node fingerprint_integration.js scrape https://example.com');
            console.log('  node fingerprint_integration.js batch urls.txt');
    }
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = FingerprintIntegration;