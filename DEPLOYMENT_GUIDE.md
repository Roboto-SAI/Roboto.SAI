# 🚀 Roboto SAI Deployment Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Platform-Specific Deployment](#platform-specific-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Common Deployment Issues](#common-deployment-issues)
6. [Health Checks](#health-checks)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/ytkrobthugod-ux/codespaces-jupyter.git
cd codespaces-jupyter

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your API keys (see Environment Configuration section)

# 5. Run the application
python run_app.py
# Or use: python main.py 5001
```

The application will be available at `http://localhost:5000` (or the specified port).

---

## Prerequisites

### System Requirements
- **Python**: 3.12.x (specified in `runtime.txt`)
- **RAM**: Minimum 2GB (4GB+ recommended due to ML dependencies)
- **Disk Space**: 2GB+ for dependencies
- **OS**: Linux, macOS, or Windows with WSL

### Required Environment Variables
The following environment variables **must** be set in your `.env` file:

```bash
# CRITICAL - Required for app to start
SESSION_SECRET=your_secure_random_string_here

# Optional but recommended
FLASK_ENV=production
DATABASE_URL=sqlite:///roboto_sai_complete.db
```

### Optional API Keys (for full functionality)
```bash
OPENAI_API_KEY=your_openai_api_key
XAI_API_KEY=your_xai_api_key
PINECONE_API_KEY=your_pinecone_key
GITHUB_APP_ID=your_github_app_id
```

---

## Platform-Specific Deployment

### 1. Heroku Deployment

**Steps:**

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set SESSION_SECRET=$(openssl rand -hex 32)
heroku config:set FLASK_ENV=production
heroku config:set OPENAI_API_KEY=your_key_here
# Add other keys as needed

# Deploy
git push heroku main

# Open the app
heroku open
```

**Important Heroku Configurations:**

1. **Buildpacks**: Heroku will auto-detect Python
2. **Dyno Type**: Use at least Standard-1X (due to heavy ML dependencies)
3. **Timeout**: Configure longer timeout for initialization:
   ```bash
   heroku config:set WEB_CONCURRENCY=2
   ```

**Files Required:**
- ✅ `Procfile` (already configured: `web: gunicorn main:app`)
- ✅ `runtime.txt` (Python version: 3.12.7)
- ✅ `requirements.txt` (all dependencies including gunicorn)

**Potential Issues:**
- **Slug size**: PyTorch and ML libraries can make slug >500MB. Consider using Docker or lighter alternatives.
- **Memory**: Standard dynos may struggle. Monitor with `heroku logs --tail`
- **Build timeout**: Initial build may take 10-15 minutes due to torch/qiskit

---

### 2. Railway Deployment

**Steps:**

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect settings from `Procfile`
5. Add environment variables in Settings → Variables:
   ```
   SESSION_SECRET=<generate_random_string>
   FLASK_ENV=production
   OPENAI_API_KEY=<your_key>
   ```
6. Deploy automatically on push

**Advantages:**
- Free tier available
- Automatic HTTPS
- Easy rollbacks
- Better for heavy dependencies than Heroku free tier

---

### 3. Render Deployment

**Steps:**

1. Go to [Render.com](https://render.com)
2. Create new "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - **Environment**: Python 3
5. Add environment variables
6. Deploy

**Recommended Plan**: Starter ($7/mo) or higher for ML workloads

---

### 4. Google Cloud Run

**Steps:**

```bash
# 1. Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# 2. Create Dockerfile (see Docker section below)

# 3. Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/roboto-sai

# 4. Deploy
gcloud run deploy roboto-sai \
  --image gcr.io/PROJECT_ID/roboto-sai \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --timeout 300s \
  --set-env-vars SESSION_SECRET=xxx,FLASK_ENV=production
```

**Advantages:**
- Pay per use
- Auto-scaling
- Good for heavy workloads

---

### 5. Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for audio/ML libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "main:app"]
```

**Build and Run:**
```bash
docker build -t roboto-sai .
docker run -p 5000:5000 --env-file .env roboto-sai
```

---

## Environment Configuration

### Creating Secure Environment Variables

**Generate SESSION_SECRET:**
```bash
# Linux/Mac
openssl rand -hex 32

# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Complete .env Template

```bash
# ============================================
# CRITICAL - REQUIRED FOR STARTUP
# ============================================
SESSION_SECRET=<GENERATE_WITH_OPENSSL>

# ============================================
# FLASK CONFIGURATION
# ============================================
FLASK_ENV=production
FLASK_APP=app_enhanced.py
DEBUG=false
LOG_LEVEL=INFO

# ============================================
# DATABASE
# ============================================
DATABASE_URL=sqlite:///roboto_sai_complete.db
SQLALCHEMY_TRACK_MODIFICATIONS=false

# ============================================
# API KEYS (Add as needed)
# ============================================
OPENAI_API_KEY=sk-...
XAI_API_KEY=xai-...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=roboto-memory

# ============================================
# GITHUB APP (Optional)
# ============================================
GITHUB_APP_ID=123456
GITHUB_PRIVATE_KEY_PATH=/path/to/key.pem
GITHUB_WEBHOOK_SECRET=...

# ============================================
# QUANTUM & VOICE (Optional toggles)
# ============================================
QUANTUM_AVAILABLE=true
QISKIT_AVAILABLE=true
SPEECH_RECOGNITION_AVAILABLE=true
PYGAME_AVAILABLE=true
```

---

## Common Deployment Issues

### 1. Missing `gunicorn` Error

**Error:**
```
bash: gunicorn: command not found
```

**Solution:**
✅ **FIXED** - `gunicorn>=21.2.0` is now in `requirements.txt`

---

### 2. Python Version Mismatch

**Error:**
```
Requested runtime (python-3.12.1) is not available
```

**Solution:**
✅ **FIXED** - Updated `runtime.txt` to `python-3.12.7`

Alternative: Use whatever version is supported by your platform (3.11.x or 3.12.x)

---

### 3. Missing `SESSION_SECRET`

**Error:**
```
RuntimeError: SESSION_SECRET environment variable is required for security
```

**Solution:**
1. Generate a secure secret:
   ```bash
   openssl rand -hex 32
   ```
2. Add to `.env`:
   ```bash
   SESSION_SECRET=<generated_value>
   ```
3. Or set directly in platform settings

---

### 4. Heavy Dependencies Causing Build Failures

**Issue**: PyTorch (2.8.0), Qiskit, and transformers make deployment slow/fail

**Solutions:**

**Option A - Reduce Dependencies (Recommended for small deployments):**
- Use CPU-only PyTorch: `torch==2.8.0+cpu`
- Remove unused dependencies
- Use lighter alternatives

**Option B - Use Docker with Pre-built Images:**
```dockerfile
FROM pytorch/pytorch:2.8.0-cuda11.8-runtime
# Your app code
```

**Option C - Deploy to Platforms with Better Resources:**
- Google Cloud Run (2-4GB RAM)
- AWS ECS/Fargate
- Azure Container Instances

---

### 5. Database Connection Issues

**Error:**
```
sqlalchemy.exc.OperationalError: unable to open database file
```

**Solution:**
1. Ensure the app has write permissions
2. For production, use PostgreSQL instead of SQLite:
   ```bash
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```
3. Add to requirements.txt:
   ```
   psycopg2-binary>=2.9.0
   ```

---

### 6. xai-sdk Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'xai'
```

**Solution:**
1. Verify `xai-sdk>=0.1.0` is in requirements.txt ✅
2. If still failing, the app should gracefully handle missing modules (check `app_enhanced.py`)
3. Or remove xai-sdk if not needed

---

## Health Checks

### Testing Your Deployment

After deployment, verify the app is working:

```bash
# 1. Check if app is responding
curl https://your-app.herokuapp.com/

# 2. Check health endpoint (if implemented)
curl https://your-app.herokuapp.com/health

# 3. Check logs
heroku logs --tail  # For Heroku
# Or check platform-specific logs
```

### Expected Response
The root endpoint `/` should return the web interface (HTML page).

---

## Troubleshooting

### Step-by-Step Debugging

1. **Check Logs:**
   ```bash
   # Heroku
   heroku logs --tail --app your-app-name
   
   # Railway
   # Check in Railway dashboard
   
   # Docker
   docker logs <container_id>
   ```

2. **Verify Environment Variables:**
   ```bash
   # Heroku
   heroku config --app your-app-name
   
   # Local
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('SESSION_SECRET'))"
   ```

3. **Test Locally First:**
   ```bash
   # Use production settings locally
   FLASK_ENV=production python main.py
   ```

4. **Check Port Binding:**
   - Heroku provides `$PORT` environment variable
   - Gunicorn config should bind to `0.0.0.0:$PORT` or `0.0.0.0:5000`

5. **Memory Issues:**
   ```bash
   # Monitor resource usage
   heroku ps:scale web=1:standard-2x  # Upgrade dyno size
   ```

---

## Performance Optimization

### 1. Reduce Dependencies
Remove unused packages from `requirements.txt`:
- If not using quantum features, remove qiskit
- If not using voice, remove librosa, pyttsx3
- Consider CPU-only PyTorch if no GPU needed

### 2. Use CDN for Static Files
Configure Flask to serve static files via CDN in production.

### 3. Enable Caching
Add Redis for session storage and caching:
```bash
pip install redis flask-caching
```

### 4. Database Optimization
- Use connection pooling
- Enable query optimization
- Use PostgreSQL for production

---

## Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` ✅
2. **Use strong SESSION_SECRET** - Generate with `openssl rand -hex 32`
3. **Enable HTTPS** - Most platforms provide this automatically
4. **Set FLASK_ENV=production** - Disables debug mode
5. **Validate all user inputs** - Already implemented in Flask routes
6. **Keep dependencies updated** - Regularly run `pip list --outdated`

---

## Support & Resources

- **Repository**: https://github.com/ytkrobthugod-ux/codespaces-jupyter
- **Issues**: Report deployment issues on GitHub
- **Heroku Docs**: https://devcenter.heroku.com/articles/python-support
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/

---

## Quick Reference Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python run_app.py

# Run with gunicorn locally
gunicorn main:app

# Deploy to Heroku
git push heroku main

# Check logs (Heroku)
heroku logs --tail

# Set env var (Heroku)
heroku config:set KEY=value

# Restart app (Heroku)
heroku restart
```

---

**Last Updated**: November 2025
**Maintainer**: Roberto Villarreal Martinez
