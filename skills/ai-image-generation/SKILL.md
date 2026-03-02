# AI Image Generation Skill for OpenClaw

**Based on:** antigravity/imagen skill from skills.sh (Google Gemini image generation)
**Adapted for:** OpenClaw with available tools
**Status:** Workflow implementation (requires Google Gemini API setup)

---

## Overview

This skill implements AI image generation workflows using Google Gemini's image generation model (`gemini-3-pro-image-preview`). It enables seamless image creation for UI placeholders, documentation, marketing materials, and design assets.

## Prerequisites

### **For Full Implementation (Required)**
- Google Cloud Platform Account
- Gemini API enabled (https://makersuite.google.com/app/apikey)
- Google Gemini API Key
- Python 3.8+ with required packages

### **For Workflow Testing (Current)**
- OpenClaw with exec tool access
- Basic understanding of AI image generation concepts

---

## Core Workflows (Adapted from Imagen Skill)

### 1. **Basic Image Generation**

**Best Practices:**
- Use descriptive, specific prompts for better results
- Specify image style, composition, and mood
- Include resolution/quality requirements
- Consider aspect ratio for intended use

**Prompt Engineering Tips:**
- **Be specific:** "A futuristic city at sunset with flying cars" vs "city"
- **Specify style:** "in the style of cyberpunk anime"  
- **Include details:** "highly detailed, 8K resolution, cinematic lighting"
- **Set mood:** "serene, peaceful, morning light"

**Implementation Steps:**
1. Validate and enhance prompt
2. Call Gemini API with generation parameters
3. Handle response and extract image
4. Save image to specified location
5. Return file path for use

### 2. **Batch Image Generation**

**Best Practices:**
- Generate variations for selection
- Use consistent style across batch
- Track generation parameters
- Organize output by project/use case

**Use Cases:**
- UI/UX design assets
- Blog post illustrations
- Social media content
- Product mockups
- Marketing materials

### 3. **Image Editing & Enhancement**

**Best Practices:**
- Start with base image generation
- Iterate with refinement prompts
- Maintain consistency across edits
- Version control generated images

**Editing Workflows:**
1. Generate base image
2. Refine specific elements
3. Adjust style/color palette
4. Add text/overlays if needed

---

## Implementation Options

### **Option A: Google Gemini API (Recommended)**
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-3-pro-image-preview')

response = model.generate_content(
    "A futuristic city skyline at sunset, cyberpunk style"
)
# Extract and save image from response
```

### **Option B: Inference.sh CLI**
```bash
# Requires inference.sh account and login
infsh app run falai/flux-dev-lora --input '{"prompt": "sunset over mountains"}'
```

### **Option C: Multiple Model Support**
- **Google Gemini:** `gemini-3-pro-image-preview` (latest)
- **FLUX Dev LoRA:** `falai/flux-dev-lora` (high quality with custom styles)
- **FLUX.2 Klein LoRA:** `falai/flux-2-klein-lora` (fast with LoRA support)
- **Seedream 4.5:** `bytedance/seedream-4-5` (2K-4K cinematic quality)

---

## OpenClaw Integration

### **Skill Structure**
```
ai-image-generation/
├── SKILL.md (this file)
├── scripts/
│   ├── image-generate.py (Basic generation)
│   ├── image-batch.py (Batch processing)
│   ├── image-edit.py (Editing/refinement)
│   └── image-utils.py (Utility functions)
├── config/
│   └── image-config.example.json
└── examples/
    └── prompt-examples.md
```

### **Configuration File**
```json
{
  "google_api_key": "YOUR_GEMINI_API_KEY",
  "default_model": "gemini-3-pro-image-preview",
  "default_size": "1024x1024",
  "default_quality": "high",
  "output_directory": "./generated_images",
  "max_images_per_day": 100,
  "style_presets": {
    "photorealistic": "photorealistic, highly detailed, 8K",
    "anime": "anime style, vibrant colors, detailed",
    "cyberpunk": "cyberpunk, neon, futuristic, detailed",
    "minimalist": "minimalist, clean, simple, elegant"
  }
}
```

---

## Rate Limits & Best Practices

### **Google Gemini API Limits**
- **Free tier:** 60 requests per minute
- **Paid tier:** Higher limits based on pricing
- **Image generation:** Counts toward text generation quotas

### **Best Practices**
1. **Prompt Quality:** Invest time in crafting good prompts
2. **Batch Processing:** Generate multiple options at once
3. **Caching:** Store and reuse successful generations
4. **Style Consistency:** Use style presets for brand consistency
5. **Ethical Use:** Avoid generating harmful or misleading content

### **Cost Optimization**
- Use appropriate resolution for use case
- Cache and reuse images when possible
- Generate in batches to minimize API calls
- Consider alternative models for different needs

---

## Workflow Examples

### **Social Media Content Creation**
```bash
# 1. Generate base image for post
# 2. Create variations for A/B testing
# 3. Generate matching images for carousel
# 4. Create profile/header images
```

### **UI/UX Design Assets**
```bash
# 1. Generate placeholder images
# 2. Create icon sets in consistent style
# 3. Generate product mockups
# 4. Create illustration for empty states
```

### **Marketing & Advertising**
```bash
# 1. Generate ad creatives
# 2. Create product visualization
# 3. Generate lifestyle context images
# 4. Create branded template elements
```

### **Documentation & Blogs**
```bash
# 1. Generate cover images
# 2. Create diagram/illustration replacements
# 3. Generate step-by-step visuals
# 4. Create featured images for sections
```

---

## Prompt Templates

### **Product Visualization**
```
[Product name] in [setting/context], [style description], 
[lighting conditions], [composition], highly detailed, 
professional product photography, [resolution]
```

### **Social Media Post**
```
[Subject] doing [action], [mood/emotion], [style], 
trending on Instagram, vibrant colors, engaging composition, 
[aspect ratio] for social media
```

### **UI/UX Design**
```
[Element type] for [app type], [style guide], clean design, 
modern aesthetics, [color palette], usable in Figma/Sketch, 
[dimensions]
```

### **Blog/Article Illustration**
```
Illustration for article about [topic], [style], 
conceptual representation, engaging, shareable, 
works as featured image, [dimensions]
```

---

## Next Steps for Full Implementation

### **Phase 1: Setup (1 day)**
1. Get Google Cloud Platform account
2. Enable Gemini API
3. Generate API key
4. Test basic image generation

### **Phase 2: Core Features (2-3 days)**
1. Implement basic generation
2. Add batch processing
3. Create style presets
4. Build prompt enhancement

### **Phase 3: Integration (1-2 days)**
1. Integrate with OpenClaw skill system
2. Add configuration management
3. Create documentation
4. Test end-to-end workflows

### **Phase 4: Advanced Features (Ongoing)**
1. Add multiple model support
2. Implement image editing
3. Create template system
4. Add analytics and reporting

---

## Current Status

**✅ Completed:**
- Workflow documentation from Imagen skill
- Best practices extraction
- Implementation options analysis
- OpenClaw integration plan

**⚡ In Progress:**
- Script creation for basic functionality
- Configuration template
- Prompt template library

**🔧 Needs Setup:**
- Google Cloud Platform account
- Gemini API enabled
- API key generation
- Testing environment

---

## Files to Create

1. `scripts/image-generate.py` - Basic image generation
2. `scripts/image-batch.py` - Batch processing
3. `scripts/image-utils.py` - Utility functions
4. `config/image-config.json` - Configuration template
5. `examples/prompt-examples.md` - Prompt library

---

## Integration with Other Skills

### **Twitter Automation**
- Generate images for social media posts
- Create profile/header images
- Generate visual content for threads

### **Lead Generation**
- Create visual assets for outreach
- Generate personalized images for prospects
- Create branded marketing materials

### **Content Creation**
- Generate blog post images
- Create presentation visuals
- Produce video thumbnails

---

**Note:** This skill provides the framework and best practices. Full functionality requires Google Gemini API access and proper authentication setup.
