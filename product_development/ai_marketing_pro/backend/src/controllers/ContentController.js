/**
 * Content Controller
 * Handles HTTP requests for content generation
 */

class ContentController {
  constructor(aiContentService) {
    this.aiContentService = aiContentService;
    this.contentHistory = []; // In-memory storage for demo - would be database in production
  }

  /**
   * Generate single piece of content
   */
  async generateContent(req, res) {
    try {
      const {
        contentType = 'social_media_instagram',
        topic = 'Digital Marketing',
        audience = 'Small Business Owners',
        tone = 'persuasive',
        wordCount = 150,
        keywords = [],
        brandVoice = null,
        examples = [],
        generateVariations = false
      } = req.body;

      // Validate input
      if (!topic || !audience) {
        return res.status(400).json({
          success: false,
          error: 'Topic and audience are required'
        });
      }

      // Generate content
      const result = await this.aiContentService.generateContent({
        contentType,
        topic,
        audience,
        tone,
        wordCount: Math.min(Math.max(parseInt(wordCount), 50), 2000),
        keywords: Array.isArray(keywords) ? keywords : [keywords],
        brandVoice,
        examples: Array.isArray(examples) ? examples : [examples],
        generateVariations
      });

      // Store in history
      if (result.success) {
        const historyEntry = {
          id: `content_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          ...result.metadata,
          generatedAt: new Date().toISOString(),
          request: { contentType, topic, audience, tone, wordCount }
        };
        
        this.contentHistory.unshift(historyEntry);
        
        // Keep only last 100 entries in memory
        if (this.contentHistory.length > 100) {
          this.contentHistory = this.contentHistory.slice(0, 100);
        }
      }

      // Return response
      return res.status(result.success ? 200 : 500).json(result);

    } catch (error) {
      console.error('Content generation error:', error);
      return res.status(500).json({
        success: false,
        error: 'Failed to generate content',
        message: error.message
      });
    }
  }

  /**
   * Batch generate multiple pieces of content
   */
  async batchGenerate(req, res) {
    try {
      const { batch } = req.body;

      if (!Array.isArray(batch) || batch.length === 0) {
        return res.status(400).json({
          success: false,
          error: 'Batch array is required and must not be empty'
        });
      }

      // Limit batch size for demo
      const limitedBatch = batch.slice(0, 10).map(item => ({
        contentType: item.contentType || 'social_media_instagram',
        topic: item.topic || 'Digital Marketing',
        audience: item.audience || 'Small Business Owners',
        tone: item.tone || 'persuasive',
        wordCount: Math.min(Math.max(parseInt(item.wordCount || 150), 50), 500),
        keywords: Array.isArray(item.keywords) ? item.keywords : [item.keywords || ''],
        brandVoice: item.brandVoice || null,
        examples: Array.isArray(item.examples) ? item.examples : [item.examples || ''],
        generateVariations: item.generateVariations || false
      }));

      const result = await this.aiContentService.batchGenerateContent(limitedBatch);

      // Store successful results in history
      if (result.success && result.results) {
        result.results.forEach((item, index) => {
          if (item.success && item.metadata) {
            const historyEntry = {
              id: `batch_${Date.now()}_${index}_${Math.random().toString(36).substr(2, 6)}`,
              ...item.metadata,
              generatedAt: new Date().toISOString(),
              request: limitedBatch[index]
            };
            
            this.contentHistory.unshift(historyEntry);
          }
        });

        // Keep only last 100 entries in memory
        if (this.contentHistory.length > 100) {
          this.contentHistory = this.contentHistory.slice(0, 100);
        }
      }

      return res.status(200).json(result);

    } catch (error) {
      console.error('Batch generation error:', error);
      return res.status(500).json({
        success: false,
        error: 'Failed to batch generate content',
        message: error.message
      });
    }
  }

  /**
   * Get available content templates
   */
  async getTemplates(req, res) {
    try {
      const templates = {
        social_media: {
          instagram: 'Instagram post with image caption and hashtags',
          twitter: 'Twitter tweet with character limit optimization',
          linkedin: 'Professional LinkedIn post for business audience',
          facebook: 'Facebook post for community engagement'
        },
        email: {
          newsletter: 'Email newsletter for subscriber engagement',
          promotional: 'Promotional email for product/service offers',
          followup: 'Follow-up email for customer nurturing'
        },
        advertising: {
          google_ads: 'Google Ads copy with keyword optimization',
          facebook_ads: 'Facebook Ads copy with audience targeting',
          linkedin_ads: 'LinkedIn Ads for professional audience'
        },
        website: {
          landing_page: 'Landing page copy for conversion optimization',
          about_page: 'About page content for brand storytelling',
          blog_post: 'Blog post for content marketing and SEO'
        }
      };

      const tones = {
        formal: 'Professional and corporate tone',
        casual: 'Friendly and conversational tone',
        persuasive: 'Convincing and action-oriented tone',
        informative: 'Educational and value-focused tone',
        inspirational: 'Motivational and uplifting tone'
      };

      return res.status(200).json({
        success: true,
        templates,
        tones,
        defaultSettings: {
          wordCount: 150,
          tone: 'persuasive',
          contentType: 'social_media_instagram'
        }
      });

    } catch (error) {
      console.error('Get templates error:', error);
      return res.status(500).json({
        success: false,
        error: 'Failed to get templates'
      });
    }
  }

  /**
   * Get content generation history
   */
  async getHistory(req, res) {
    try {
      const { limit = 20, offset = 0 } = req.query;
      const limitNum = Math.min(parseInt(limit), 100);
      const offsetNum = Math.max(parseInt(offset), 0);

      const paginatedHistory = this.contentHistory.slice(offsetNum, offsetNum + limitNum);

      return res.status(200).json({
        success: true,
        history: paginatedHistory,
        pagination: {
          total: this.contentHistory.length,
          limit: limitNum,
          offset: offsetNum,
          hasMore: offsetNum + limitNum < this.contentHistory.length
        }
      });

    } catch (error) {
      console.error('Get history error:', error);
      return res.status(500).json({
        success: false,
        error: 'Failed to get history'
      });
    }
  }

  /**
   * Analyze competitor and generate improved content
   */
  async analyzeCompetitor(req, res) {
    try {
      const { competitorContent, targetAudience, industry } = req.body;

      if (!competitorContent || !targetAudience) {
        return res.status(400).json({
          success: false,
          error: 'Competitor content and target audience are required'
        });
      }

      const result = await this.aiContentService.generateFromCompetitorAnalysis(
        competitorContent,
        targetAudience
      );

      // Store in history
      if (result.success) {
        const historyEntry = {
          id: `competitor_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          type: 'competitor_analysis',
          targetAudience,
          industry,
          generatedAt: new Date().toISOString(),
          improvements: result.improvements,
          originalLength: competitorContent.length,
          improvedLength: result.improvedContent?.length || 0
        };
        
        this.contentHistory.unshift(historyEntry);
        
        // Keep only last 100 entries in memory
        if (this.contentHistory.length > 100) {
          this.contentHistory = this.contentHistory.slice(0, 100);
        }
      }

      return res.status(result.success ? 200 : 500).json(result);

    } catch (error) {
      console.error('Competitor analysis error:', error);
      return res.status(500).json({
        success: false,
        error: 'Failed to analyze competitor',
        message: error.message
      });
    }
  }

  /**
   * Get content statistics
   */
  async getStats(req, res) {
    try {
      const stats = {
        totalGenerated: this.contentHistory.length,
        byContentType: {},
        byTone: {},
        averageWordCount: 0,
        averageEngagementScore: 0,
        recentActivity: this.contentHistory.slice(0, 5)
      };

      // Calculate statistics
      if (this.contentHistory.length > 0) {
        let totalWords = 0;
        let totalEngagement = 0;

        this.contentHistory.forEach(entry => {
          // Count by content type
          const contentType = entry.contentType || 'unknown';
          stats.byContentType[contentType] = (stats.byContentType[contentType] || 0) + 1;

          // Count by tone
          const tone = entry.tone || 'unknown';
          stats.byTone[tone] = (stats.byTone[tone] || 0) + 1;

          // Sum for averages
          totalWords += entry.wordCount || 0;
          totalEngagement += entry.engagementScore || 0;
        });

        stats.averageWordCount = Math.round(totalWords / this.contentHistory.length);
        stats.averageEngagementScore = Math.round(totalEngagement / this.contentHistory.length);
      }

      return res.status(200).json({
        success: true,
        stats,
        generatedAt: new Date().toISOString()
      });

    } catch (error) {
      console.error('Get stats error:', error);
      return res.status(500).json({
        success: false,
        error: 'Failed to get statistics'
      });
    }
  }
}

module.exports = ContentController;