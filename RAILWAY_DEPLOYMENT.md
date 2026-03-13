# Railway Deployment Guide

## 🚀 Construction Estimator Deployment

### Prerequisites
1. Railway.app account connected to GitHub
2. GitHub repository with the Construction Estimator code
3. (Optional) OpenAI API key for AI suggestions

### Deployment Steps

#### 1. Connect Railway to GitHub
1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select the repository: `zan-maker/Mac-Mini-claw`

#### 2. Configure Environment Variables
In Railway dashboard, add these environment variables:

**Required:**
- `PORT`: `5000` (Railway automatically sets this)

**Optional AI Configuration:**
- `USE_OLLAMA`: `false` (set to `true` if you have Ollama deployed separately)
- `OLLAMA_URL`: `http://your-ollama-service:11434/v1/chat/completions`
- `OPENAI_API_KEY`: `your-openai-api-key` (for OpenAI-based suggestions)

#### 3. Deploy
1. Railway will automatically detect the `railway.json` configuration
2. It will install dependencies from `requirements.txt`
3. It will start the application using the command in `railway.json`

### Configuration Files

#### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "python construction-estimator-railway.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 60,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

#### `requirements.txt`
```
Flask==2.3.3
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

### Application Structure

#### Primary Deployment File: `construction-estimator-railway.py`
- Production-ready Flask application
- Supports multiple AI providers (Ollama, OpenAI, or static fallback)
- Health check endpoint at `/health`
- Quick estimates at `/quick/<project_type>/<size>`
- Detailed estimates with AI at `/estimate` (POST)

#### Alternative: `construction-web.py`
- Original version with Ollama integration
- Requires Ollama to be running locally
- Better for local development

### API Endpoints

#### `GET /`
- API information and version

#### `GET /health`
- Health check with AI provider status

#### `GET /quick/<project_type>/<size>`
- Quick estimate without AI
- Example: `/quick/deck/20x12`

#### `POST /estimate`
- Detailed estimate with AI suggestions
- Request body: `{"project_type": "deck", "dimensions": {"length": 20, "width": 12}}`

### AI Provider Configuration

#### Option 1: Static Fallback (Default)
- No API keys required
- Pre-defined construction suggestions
- Works immediately after deployment

#### Option 2: OpenAI
- Set `OPENAI_API_KEY` environment variable
- Uses GPT-3.5-turbo for AI suggestions
- Requires OpenAI API credits

#### Option 3: Ollama
- Set `USE_OLLAMA=true` and `OLLAMA_URL`
- Requires separate Ollama deployment
- Zero-cost AI inference

### Monitoring and Logs

#### Railway Dashboard
- View deployment logs
- Monitor resource usage
- Check deployment status
- View environment variables

#### Application Logs
- Access via Railway logs tab
- Includes startup messages and errors
- API request logging

### Custom Domains
1. In Railway project settings, go to "Domains"
2. Add your custom domain
3. Configure DNS settings as instructed
4. Railway provides SSL certificates automatically

### Scaling
- Railway automatically scales based on traffic
- No configuration needed for basic usage
- Upgrade plan for higher resource limits

### Backup and Recovery
- Railway provides automatic backups
- Rollback to previous deployments
- Environment variable management

### Cost
- Free tier available with limited resources
- Pay-as-you-go pricing for higher usage
- No cost for static fallback mode

### Troubleshooting

#### Common Issues

1. **Deployment fails**
   - Check Railway logs for error messages
   - Verify `requirements.txt` has correct packages
   - Ensure Python version is compatible

2. **AI suggestions not working**
   - Check environment variables are set
   - Verify API keys are valid
   - Check network connectivity to AI services

3. **Health check fails**
   - Verify application is starting correctly
   - Check port configuration
   - Review application logs

#### Logs Location
- Railway dashboard → Project → Deployments → Select deployment → Logs
- Application logs show startup and runtime messages

### Updates and Maintenance

#### Deploy Updates
1. Push changes to GitHub
2. Railway automatically detects changes
3. New deployment starts automatically
4. Zero-downtime deployment when healthy

#### Rollback
1. Go to Railway dashboard
2. Select previous deployment
3. Click "Promote to Production"
4. Application rolls back instantly

### Security Best Practices

1. **Environment Variables**
   - Never commit API keys to GitHub
   - Use Railway environment variables
   - Rotate keys regularly

2. **Dependencies**
   - Keep dependencies updated
   - Use specific versions in `requirements.txt`
   - Regularly check for security updates

3. **API Security**
   - Consider adding API key authentication
   - Implement rate limiting if needed
   - Use HTTPS (provided by Railway)

### Performance Optimization

1. **Caching**
   - Consider adding Redis for caching
   - Cache frequent estimate calculations
   - Cache AI responses when appropriate

2. **Database**
   - Add SQLite or PostgreSQL for persistent storage
   - Store estimate history
   - Enable customer preference learning

3. **CDN**
   - Railway provides global CDN
   - Static assets served efficiently
   - Automatic SSL/TLS

### Support
- Railway documentation: https://docs.railway.app
- GitHub repository: https://github.com/zan-maker/Mac-Mini-claw
- Application issues: Check Railway logs first

---

## 🎯 Quick Start

1. **Connect Railway to GitHub**
2. **Add environment variables** (optional for AI)
3. **Deploy** - Railway does the rest
4. **Access your API** at the provided Railway URL
5. **Test endpoints**: `/health` and `/quick/deck/20x12`

Your Construction Estimator API is now live on Railway! 🚀