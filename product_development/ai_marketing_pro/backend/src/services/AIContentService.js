/**
 * AI Content Generation Service
 * Handles all AI-powered content creation for marketing materials
 */

const { OpenAI } = require('openai');
const Anthropic = require('@anthropic-ai/sdk');

class AIContentService {
  constructor() {
    // Initialize AI clients (will use environment variables in production)
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY || 'mock-key-for-development',
    });
    
    this.anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY || 'mock-key-for-development',
    });
    
    // Content templates for different types
    this.templates = {
      social_media: {
        instagram: "Create an engaging Instagram post about {topic} for {audience}. Include relevant hashtags.",
        twitter: "Write a compelling tweet about {topic} that will get retweets from {audience}.",
        linkedin: "Create a professional LinkedIn post about {topic} for {audience} in the {industry} industry.",
        facebook: "Write a Facebook post about {topic} that encourages engagement from {audience}."
      },
      email: {
        newsletter: "Write a newsletter email about {topic} for {audience} subscribers.",
        promotional: "Create a promotional email for {product} targeting {audience}.",
        followup: "Write a follow-up email for {situation} to {audience}."
      },
      advertising: {
        google_ads: "Write Google Ads copy for {product} targeting {audience} with {keywords}.",
        facebook_ads: "Create Facebook Ad copy for {product} targeting {audience} aged {age_range}.",
        linkedin_ads: "Write LinkedIn Ad copy for {service} targeting {audience} professionals."
      },
      website: {
        landing_page: "Write landing page copy for {product} targeting {audience} with value proposition {value_prop}.",
        about_page: "Create about page content for {company} in the {industry} industry.",
        blog_post: "Write a blog post about {topic} for {audience} with SEO keywords {keywords}."
      }
    };
    
    // Tone options
    this.tones = {
      formal: "Use a formal, professional tone suitable for corporate communications.",
      casual: "Use a casual, friendly tone suitable for social media and informal communications.",
      persuasive: "Use a persuasive tone that encourages action and conversion.",
      informative: "Use an informative, educational tone that provides value to the reader.",
      inspirational: "Use an inspirational, motivational tone that uplifts and encourages."
    };
  }
  
  /**
   * Generate marketing content using AI
   * @param {Object} options - Content generation options
   * @returns {Promise<Object>} Generated content and metadata
   */
  async generateContent(options) {
    const {
      contentType,
      topic,
      audience,
      tone = 'persuasive',
      wordCount = 150,
      keywords = [],
      brandVoice = null,
      examples = []
    } = options;
    
    try {
      // Build the prompt based on content type
      const prompt = this.buildPrompt(contentType, topic, audience, tone, wordCount, keywords, brandVoice, examples);
      
      // Generate content using OpenAI (primary) with fallback to Anthropic
      let content;
      let modelUsed = 'gpt-4';
      
      try {
        const response = await this.openai.chat.completions.create({
          model: 'gpt-4',
          messages: [
            {
              role: 'system',
              content: 'You are an expert marketing copywriter specializing in creating engaging, conversion-focused content for businesses.'
            },
            {
              role: 'user',
              content: prompt
            }
          ],
          temperature: 0.7,
          max_tokens: Math.min(wordCount * 4, 2000)
        });
        
        content = response.choices[0].message.content;
      } catch (openaiError) {
        console.warn('OpenAI failed, falling back to Anthropic:', openaiError.message);
        
        // Fallback to Anthropic
        const response = await this.anthropic.messages.create({
          model: 'claude-3-opus-20240229',
          max_tokens: Math.min(wordCount * 4, 2000),
          messages: [
            {
              role: 'user',
              content: prompt
            }
          ]
        });
        
        content = response.content[0].text;
        modelUsed = 'claude-3-opus';
      }
      
      // Analyze the generated content
      const analysis = await this.analyzeContent(content, contentType);
      
      // Generate variations if requested
      const variations = options.generateVariations 
        ? await this.generateVariations(content, contentType, tone)
        : [];
      
      // Generate hashtags for social media content
      const hashtags = contentType.includes('social_media') 
        ? await this.generateHashtags(topic, audience)
        : [];
      
      // Generate call-to-action suggestions
      const ctas = await this.generateCTAs(contentType, audience);
      
      return {
        success: true,
        content: content,
        metadata: {
          contentType,
          topic,
          audience,
          tone,
          wordCount: this.countWords(content),
          characterCount: content.length,
          modelUsed,
          analysis,
          variations: variations.slice(0, 3), // Limit to 3 variations
          hashtags: hashtags.slice(0, 10), // Limit to 10 hashtags
          ctas: ctas.slice(0, 3), // Limit to 3 CTAs
          readabilityScore: this.calculateReadability(content),
          sentimentScore: this.analyzeSentiment(content),
          generatedAt: new Date().toISOString()
        }
      };
      
    } catch (error) {
      console.error('Error generating AI content:', error);
      return {
        success: false,
        error: error.message,
        content: this.getFallbackContent(contentType, topic, audience, tone)
      };
    }
  }
  
  /**
   * Build a detailed prompt for AI content generation
   */
  buildPrompt(contentType, topic, audience, tone, wordCount, keywords, brandVoice, examples) {
    let prompt = `Create ${contentType.replace('_', ' ')} content with the following specifications:\n\n`;
    
    prompt += `Topic: ${topic}\n`;
    prompt += `Target Audience: ${audience}\n`;
    prompt += `Tone: ${tone} - ${this.tones[tone] || 'Use appropriate tone for the audience.'}\n`;
    prompt += `Word Count: Approximately ${wordCount} words\n`;
    
    if (keywords && keywords.length > 0) {
      prompt += `Keywords to include: ${keywords.join(', ')}\n`;
    }
    
    if (brandVoice) {
      prompt += `Brand Voice Guidelines: ${brandVoice}\n`;
    }
    
    if (examples && examples.length > 0) {
      prompt += `Examples to follow:\n${examples.map((ex, i) => `${i + 1}. ${ex}`).join('\n')}\n`;
    }
    
    // Add content type specific instructions
    const template = this.getTemplate(contentType);
    if (template) {
      prompt += `\nContent Format: ${template}\n`;
    }
    
    // Add quality requirements
    prompt += `\nRequirements:\n`;
    prompt += `- Engaging and attention-grabbing\n`;
    prompt += `- Clear and concise\n`;
    prompt += `- Action-oriented\n`;
    prompt += `- Professional quality\n`;
    prompt += `- Optimized for ${contentType.replace('_', ' ')} platform\n`;
    
    if (contentType.includes('social_media')) {
      prompt += `- Include emojis where appropriate\n`;
      prompt += `- Use line breaks for readability\n`;
    }
    
    if (contentType.includes('email')) {
      prompt += `- Include compelling subject line\n`;
      prompt += `- Use proper email formatting\n`;
      prompt += `- Include clear call-to-action\n`;
    }
    
    if (contentType.includes('advertising')) {
      prompt += `- Focus on benefits, not just features\n`;
      prompt += `- Create urgency where appropriate\n`;
      prompt += `- Include strong value proposition\n`;
    }
    
    return prompt;
  }
  
  /**
   * Get template for specific content type
   */
  getTemplate(contentType) {
    const parts = contentType.split('_');
    if (parts.length === 2 && this.templates[parts[0]] && this.templates[parts[0]][parts[1]]) {
      return this.templates[parts[0]][parts[1]];
    }
    return null;
  }
  
  /**
   * Analyze generated content
   */
  async analyzeContent(content, contentType) {
    // Simple analysis - in production would use more sophisticated NLP
    const analysis = {
      wordCount: this.countWords(content),
      sentenceCount: this.countSentences(content),
      averageSentenceLength: this.averageSentenceLength(content),
      readingLevel: this.calculateReadingLevel(content),
      keywordDensity: this.calculateKeywordDensity(content),
      emotionalTone: this.detectEmotionalTone(content),
      engagementScore: this.calculateEngagementScore(content, contentType)
    };
    
    return analysis;
  }
  
  /**
   * Generate content variations
   */
  async generateVariations(originalContent, contentType, tone) {
    const variations = [];
    
    // Generate different tones
    const otherTones = Object.keys(this.tones).filter(t => t !== tone);
    for (const variationTone of otherTones.slice(0, 2)) { // Limit to 2 variations
      try {
        const prompt = `Rewrite the following content in a ${variationTone} tone:\n\n${originalContent}\n\n${this.tones[variationTone]}`;
        
        const response = await this.openai.chat.completions.create({
          model: 'gpt-3.5-turbo',
          messages: [
            {
              role: 'user',
              content: prompt
            }
          ],
          temperature: 0.8,
          max_tokens: 500
        });
        
        variations.push({
          tone: variationTone,
          content: response.choices[0].message.content
        });
      } catch (error) {
        console.warn(`Failed to generate ${variationTone} variation:`, error.message);
      }
    }
    
    return variations;
  }
  
  /**
   * Generate relevant hashtags
   */
  async generateHashtags(topic, audience) {
    try {
      const prompt = `Generate 15 relevant hashtags for content about "${topic}" targeting "${audience}". Include a mix of popular and niche hashtags.`;
      
      const response = await this.openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.7,
        max_tokens: 200
      });
      
      const hashtagsText = response.choices[0].message.content;
      // Extract hashtags from response
      const hashtags = hashtagsText.match(/#[\w]+/g) || [];
      return hashtags.map(h => h.toLowerCase()).slice(0, 15);
      
    } catch (error) {
      console.warn('Failed to generate hashtags:', error.message);
      return [`#${topic.replace(/\s+/g, '')}`, `#${audience.replace(/\s+/g, '')}`, '#marketing', '#business'];
    }
  }
  
  /**
   * Generate call-to-action suggestions
   */
  async generateCTAs(contentType, audience) {
    const ctas = [
      "Learn more on our website",
      "Sign up for free trial",
      "Download our guide",
      "Schedule a consultation",
      "Join our community",
      "Follow us for more tips",
      "Share with your network",
      "Book a demo today"
    ];
    
    // Filter based on content type
    if (contentType.includes('social_media')) {
      return ctas.filter(cta => 
        cta.includes('Follow') || 
        cta.includes('Share') || 
        cta.includes('Join')
      );
    } else if (contentType.includes('email')) {
      return ctas.filter(cta => 
        cta.includes('Sign up') || 
        cta.includes('Download') || 
        cta.includes('Schedule')
      );
    } else if (contentType.includes('advertising')) {
      return ctas.filter(cta => 
        cta.includes('Learn more') || 
        cta.includes('Book') || 
        cta.includes('Download')
      );
    }
    
    return ctas.slice(0, 3);
  }
  
  /**
   * Get fallback content if AI generation fails
   */
  getFallbackContent(contentType, topic, audience, tone) {
    const fallbacks = {
      social_media_instagram: `Check out our latest update about ${topic}! Perfect for ${audience}. #${topic.replace(/\s+/g, '')} #business`,
      social_media_twitter: `Exciting news about ${topic}! Great insights for ${audience}.`,
      email_newsletter: `In this edition: ${topic}. Valuable information for ${audience}.`,
      advertising_google_ads: `Discover ${topic} - Perfect solution for ${audience}. Learn more!`
    };
    
    const key = `${contentType}`;
    return fallbacks[key] || `Content about ${topic} for ${audience}.`;
  }
  
  // Utility methods
  
  countWords(text) {
    return text.trim().split(/\s+/).length;
  }
  
  countSentences(text) {
    return text.split(/[.!?]+/).filter(s => s.trim().length > 0).length;
  }
  
  averageSentenceLength(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    if (sentences.length === 0) return 0;
    const totalWords = sentences.reduce((sum, sentence) => sum + this.countWords(sentence), 0);
    return Math.round(totalWords / sentences.length);
  }
  
  calculateReadingLevel(text) {
    // Simple Flesch-Kincaid approximation
    const words = this.countWords(text);
    const sentences = this.countSentences(text);
    const syllables = this.estimateSyllables(text);
    
    if (words === 0 || sentences === 0) return 'Unknown';
    
    const score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words);
    
    if (score >= 90) return 'Very Easy (5th grade)';
    if (score >= 80) return 'Easy (6th grade)';
    if (score >= 70) return 'Fairly Easy (7th grade)';
    if (score >= 60) return 'Standard (8th-9th grade)';
    if (score >= 50) return 'Fairly Difficult (10th-12th grade)';
    if (score >= 30) return 'Difficult (College)';
    return 'Very Difficult (College graduate)';
  }
  
  estimateSyllables(text) {
    // Simple syllable estimation
    const words = text.toLowerCase().split(/\s+/);
    let syllables = 0;
    
    words.forEach(word => {
      word = word.replace(/[^a-z]/g, '');
      if (word.length <= 3) {
        syllables += 1;
      } else {
        syllables += Math.max(1, Math.floor(word.length / 3));
      }
    });
    
    return syllables;
  }
  
  calculateKeywordDensity(text) {
    const words = text.toLowerCase().split(/\s+/);
    const uniqueWords = [...new Set(words)];
    const densities = {};
    
    uniqueWords.forEach(word => {
      if (word.length > 3) { // Ignore short words
        const count = words.filter(w => w === word).length;
        densities[word] = (count / words.length * 100).toFixed(2) + '%';
      }
    });
    
    // Return top 5 keywords by density
    return Object.entries(densities)
      .sort((a, b) => parseFloat(b[1]) - parseFloat(a[1]))
      .slice(0, 5)
      .map(([word, density]) => ({ word, density }));
  }
  
  detectEmotionalTone(text) {
    const positiveWords = ['great', 'excellent', 'amazing', 'wonderful', 'perfect', 'best', 'love', 'happy'];
    const negativeWords = ['bad', 'terrible', 'awful', 'worst', 'hate', 'sad', 'angry'];
    
    const words = text.toLowerCase().split(/\s+/);
    let positive = 0;
    let negative = 0;
    
    words.forEach(word => {
      if (positiveWords.includes(word)) positive++;
      if (negativeWords.includes(word)) negative++;
    });
    
    const total = positive + negative;
    if (total === 0) return 'Neutral';
    
    const score = (positive - negative) / total;
    
    if (score > 0.3) return 'Very Positive';
    if (score > 0.1) return 'Positive';
    if (score > -0.1) return 'Neutral';
    if (score > -0.3) return 'Negative';
    return 'Very Negative';
  }
  
  calculateEngagementScore(content, contentType) {
    let score = 50; // Base score
    
    // Content length scoring
    const wordCount = this.countWords(content);
    if (contentType.includes('social_media')) {
      if (wordCount >= 50 && wordCount <= 280) score += 20; // Good length for social
    } else if (contentType.includes('email')) {
      if (wordCount >= 100 && wordCount <= 500) score += 20; // Good length for email
    }
    
    // Question marks increase engagement
    const questionCount = (content.match(/\?/g) || []).length;
    score += Math.min(questionCount * 5, 15);
    
    // Exclamation marks increase excitement
    const exclamationCount = (content.match(/!/g) || []).length;
    score += Math.min(exclamationCount * 3, 10);
    
    // Emojis increase social media engagement
    const emojiCount = (content.match(/[\u{1F300}-\u{1F9FF}]/gu) || []).length;
    if (contentType.includes('social_media')) {
      score += Math.min(emojiCount * 2, 10);
    }
    
    // Hashtags increase discoverability
    const hashtagCount = (content.match(/#[\w]+/g) || []).length;
    if (contentType.includes('social_media')) {
      score += Math.min(hashtagCount * 3, 15);
    }
    
    // Call-to-action presence
    const ctaWords = ['click', 'learn', 'sign', 'download', 'join', 'follow', 'share', 'book'];
    const hasCTA = ctaWords.some(word => content.toLowerCase().includes(word));
    if (hasCTA) score += 10;
    
    // Ensure score is between 0-100
    return Math.max(0, Math.min(100, score));
  }
  
  calculateReadability(text) {
    // Simple readability score (0-100)
    const words = this.countWords(text);
    const sentences = this.countSentences(text);
    const avgSentenceLength = this.averageSentenceLength(text);
    
    if (words === 0 || sentences === 0) return 50;
    
    // Shorter sentences and common words increase readability
    let score = 70;
    
    if (avgSentenceLength > 20) score -= 20;
    else if (avgSentenceLength > 15) score -= 10;
    else if (avgSentenceLength < 10) score += 10;
    
    // Check for complex words (more than 3 syllables)
    const complexWordCount = this.countComplexWords(text);
    const complexWordRatio = complexWordCount / words;
    
    if (complexWordRatio > 0.2) score -= 20;
    else if (complexWordRatio > 0.1) score -= 10;
    else if (complexWordRatio < 0.05) score += 10;
    
    return Math.max(0, Math.min(100, score));
  }
  
  countComplexWords(text) {
    // Simple complex word detection (words with 4+ syllables)
    const words = text.toLowerCase().split(/\s+/);
    let complexCount = 0;
    
    words.forEach(word => {
      word = word.replace(/[^a-z]/g, '');
      if (word.length >= 8) { // Approximation for complex words
        complexCount++;
      }
    });
    
    return complexCount;
  }
  
  analyzeSentiment(text) {
    // Simple sentiment analysis (-1 to 1)
    const positiveWords = [
      'great', 'excellent', 'amazing', 'wonderful', 'perfect', 'best', 
      'love', 'happy', 'good', 'awesome', 'fantastic', 'superb', 'outstanding'
    ];
    const negativeWords = [
      'bad', 'terrible', 'awful', 'worst', 'hate', 'sad', 'angry',
      'poor', 'horrible', 'disappointing', 'frustrating', 'annoying'
    ];
    
    const words = text.toLowerCase().split(/\s+/);
    let positive = 0;
    let negative = 0;
    
    words.forEach(word => {
      const cleanWord = word.replace(/[^a-z]/g, '');
      if (positiveWords.includes(cleanWord)) positive++;
      if (negativeWords.includes(cleanWord)) negative++;
    });
    
    const total = positive + negative;
    if (total === 0) return 0;
    
    return (positive - negative) / total;
  }
  
  /**
   * Batch generate multiple pieces of content
   */
  async batchGenerateContent(batchOptions) {
    const results = [];
    
    for (const options of batchOptions) {
      try {
        const result = await this.generateContent(options);
        results.push(result);
      } catch (error) {
        results.push({
          success: false,
          error: error.message,
          options
        });
      }
    }
    
    return {
      success: true,
      batchId: `batch_${Date.now()}`,
      total: batchOptions.length,
      successful: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      results
    };
  }
  
  /**
   * Generate content based on competitor analysis
   */
  async generateFromCompetitorAnalysis(competitorData, targetAudience) {
    // Analyze competitor content and generate improved version
    const analysisPrompt = `Analyze this competitor content and create better version for ${targetAudience}:\n\n${competitorData}`;
    
    try {
      const response = await this.openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          {
            role: 'system',
            content: 'You are a competitive marketing analyst. Analyze competitor content and create improved versions that outperform them.'
          },
          {
            role: 'user',
            content: analysisPrompt
          }
        ],
        temperature: 0.8,
        max_tokens: 1000
      });
      
      return {
        success: true,
        originalAnalysis: competitorData,
        improvedContent: response.choices[0].message.content,
        improvements: await this.identifyImprovements(competitorData, response.choices[0].message.content)
      };
      
    } catch (error) {
      console.error('Error generating from competitor analysis:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  /**
   * Identify improvements between original and improved content
   */
  async identifyImprovements(original, improved) {
    const prompt = `Compare these two pieces of content and list the key improvements in the second one:\n\nORIGINAL:\n${original}\n\nIMPROVED:\n${improved}\n\nList 3-5 key improvements.`;
    
    try {
      const response = await this.openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.7,
        max_tokens: 300
      });
      
      return response.choices[0].message.content.split('\n').filter(line => line.trim().length > 0);
    } catch (error) {
      return ['More engaging tone', 'Clearer value proposition', 'Stronger call-to-action'];
    }
  }
}

module.exports = AIContentService;