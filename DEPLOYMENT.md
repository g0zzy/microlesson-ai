# Deployment Guide

Step-by-step instructions for deploying MicroLesson AI to various platforms.

## Prerequisites

- GitHub account (for most platforms)
- Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
- Your code pushed to a GitHub repository

---

## Option 1: Render.com (Recommended for Hackathons)

**Best for**: Quick deployment, free tier available, easy setup

### Backend Deployment

1. **Create account** at [render.com](https://render.com)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - Name: `microlesson-ai-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variable**
   - Key: `ANTHROPIC_API_KEY`
   - Value: Your API key

5. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes
   - Note your service URL: `https://microlesson-ai-backend.onrender.com`

### Frontend Deployment

1. **Update API URL**
   Edit `frontend/script.js`, line 7:
   ```javascript
   const API_URL = 'https://microlesson-ai-backend.onrender.com';
   ```

2. **Deploy Frontend**
   - Go to Render Dashboard
   - Click "New +" → "Static Site"
   - Connect same repository
   - Publish directory: `frontend`
   - Click "Create Static Site"

3. **Done!** Your app is live at `https://microlesson-ai.onrender.com`

---

## Option 2: Vercel (Frontend) + Railway (Backend)

**Best for**: Fastest deployment, great DX, generous free tiers

### Backend on Railway

1. **Create account** at [railway.app](https://railway.app)

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - Railway auto-detects Python
   - Add environment variable: `ANTHROPIC_API_KEY`
   - Railway generates a URL automatically

4. **Custom Start Command** (if needed)
   - Go to Settings → Start Command
   - Add: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### Frontend on Vercel

1. **Create account** at [vercel.com](https://vercel.com)

2. **Import Project**
   - Click "New Project"
   - Import from GitHub
   - Select your repository

3. **Configure Build Settings**
   - Framework Preset: Other
   - Root Directory: `frontend`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

4. **Update API URL**
   - Before deploying, update `frontend/script.js`
   - Change `API_URL` to your Railway backend URL

5. **Deploy**
   - Click "Deploy"
   - Your app is live in ~30 seconds!

---

## Option 3: Fly.io (Full Stack)

**Best for**: Single deployment, Docker-based, production-ready

### Setup

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploy

```bash
# Launch app
fly launch

# Set secret
fly secrets set ANTHROPIC_API_KEY=your_key_here

# Deploy
fly deploy

# Open app
fly open
```

### Serve Frontend

Update `backend/main.py` to serve static files:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
```

---

## Option 4: Heroku

**Best for**: Traditional PaaS, well-documented

### Create Procfile

Create `Procfile` in root:

```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Deploy

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Create app
heroku create microlesson-ai

# Set environment variable
heroku config:set ANTHROPIC_API_KEY=your_key_here

# Deploy
git push heroku main

# Open app
heroku open
```

---

## Option 5: Google Cloud Run

**Best for**: Scalability, pay-per-use

### Build Container

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/microlesson-ai
```

### Deploy

```bash
gcloud run deploy microlesson-ai \
  --image gcr.io/PROJECT_ID/microlesson-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key_here
```

---

## Option 6: Netlify (Frontend Only)

**Best for**: Static frontend hosting with serverless functions

### Deploy Frontend

1. Drag & drop `frontend` folder to [netlify.com/drop](https://app.netlify.com/drop)
2. Update `API_URL` in `script.js` to your backend URL
3. Done!

### Alternative: Netlify CLI

```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod
```

---

## Environment Variables

All platforms need this environment variable:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

**Security Notes**:
- Never commit `.env` to Git
- Use platform-specific secret management
- Rotate API keys regularly

---

## CORS Configuration

If you deploy frontend and backend separately, update CORS in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "http://localhost:3000"  # For local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Custom Domain

### Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records as shown

### Vercel
1. Go to Settings → Domains
2. Add domain
3. Configure DNS

### Railway
1. Go to Settings → Domains
2. Add custom domain
3. Point CNAME to Railway

---

## Monitoring & Logs

### Render
- Logs tab in dashboard
- Auto-restarts on crashes

### Railway
- Real-time logs in dashboard
- Metrics available in Pro plan

### Fly.io
```bash
fly logs
fly status
```

### Heroku
```bash
heroku logs --tail
```

---

## Cost Estimates

### Free Tier Comparison

| Platform | Backend Free Tier | Frontend Free Tier | Best For |
|----------|------------------|-------------------|----------|
| Render | 750 hrs/month | Unlimited static sites | Hackathons |
| Railway | $5 credit/month | N/A | Quick demos |
| Vercel | N/A | Unlimited bandwidth | Frontend |
| Netlify | N/A | 100GB bandwidth | Static sites |
| Fly.io | Limited | Limited | Full control |
| Heroku | 550 hrs/month | Via static buildpack | Legacy apps |

### Claude API Costs (Sonnet 4.5)

- Input: $3 / million tokens
- Output: $15 / million tokens
- **Per lesson**: ~$0.01-0.03
- **1000 lessons**: ~$10-30

---

## Troubleshooting

### Build Fails
- Check Python version (needs 3.9+)
- Verify `requirements.txt` is in root
- Check build logs for missing dependencies

### API Key Not Working
- Verify key is set in environment
- Check for extra spaces or quotes
- Test with `curl` to API endpoint

### CORS Errors
- Update `allow_origins` in `main.py`
- Clear browser cache
- Check browser console for exact error

### Frontend Can't Reach Backend
- Verify backend URL in `script.js`
- Check if backend is running: visit `/health` endpoint
- Ensure HTTPS if frontend is HTTPS

---

## Performance Tips

1. **Enable Caching**
   - Cache common topics
   - Use CDN for frontend

2. **Optimize Claude Calls**
   - Reduce max_tokens if lessons are too long
   - Use Haiku model for faster responses

3. **Monitor Usage**
   - Set up alerts for API costs
   - Track popular topics

---

## Post-Deployment Checklist

- [ ] Backend is accessible at `/health` endpoint
- [ ] Frontend loads without errors
- [ ] Can generate text lessons
- [ ] Can generate voice lessons
- [ ] Can generate visual lessons
- [ ] API key is kept secret
- [ ] CORS is properly configured
- [ ] Error messages display correctly
- [ ] Mobile responsive design works
- [ ] Share URL with teammates!

---

**Need help?** Check the main [README.md](README.md) or create an issue on GitHub.
