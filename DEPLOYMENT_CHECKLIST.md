# 📋 Deployment Checklist for Roboto SAI

Use this checklist to ensure successful deployment to any platform.

## Pre-Deployment Checklist

### 1. Code Preparation
- [x] All code changes committed to Git
- [x] No `.env` file in repository (check `.gitignore`)
- [x] `requirements.txt` is up to date
- [x] `runtime.txt` specifies correct Python version (3.12.7)
- [x] `Procfile` is configured correctly
- [ ] All tests passing (run: `pytest`)
- [ ] Code linting complete (run: `flake8`)

### 2. Dependencies
- [x] `gunicorn>=21.2.0` in requirements.txt
- [x] All Flask dependencies listed
- [ ] Heavy dependencies reviewed (torch, qiskit) - consider optimization
- [ ] Run `pip install -r requirements.txt` locally to verify

### 3. Environment Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Generate `SESSION_SECRET`:
  ```bash
  openssl rand -hex 32
  ```
- [ ] Add all required API keys to `.env`
- [ ] Set `FLASK_ENV=production`
- [ ] Configure `DATABASE_URL` if using external database

### 4. Local Testing
- [ ] Run verification script:
  ```bash
  python verify_deployment.py
  ```
- [ ] Start app locally:
  ```bash
  python run_app.py
  ```
- [ ] Test in browser: `http://localhost:5000`
- [ ] Check for errors in console
- [ ] Test with production-like settings:
  ```bash
  FLASK_ENV=production gunicorn main:app
  ```

### 5. Platform Selection
Choose your deployment platform:
- [ ] Heroku
- [ ] Railway
- [ ] Render
- [ ] Google Cloud Run
- [ ] AWS (ECS/Fargate)
- [ ] Azure
- [ ] DigitalOcean
- [ ] Docker (self-hosted)

---

## Platform-Specific Checklists

### Heroku Deployment

#### Setup
- [ ] Install Heroku CLI: `brew install heroku` (Mac) or download from heroku.com
- [ ] Login: `heroku login`
- [ ] Create app: `heroku create your-app-name`

#### Configuration
- [ ] Set environment variables:
  ```bash
  heroku config:set SESSION_SECRET=$(openssl rand -hex 32)
  heroku config:set FLASK_ENV=production
  heroku config:set OPENAI_API_KEY=your_key
  # Add other variables as needed
  ```

#### Files Check
- [x] `Procfile` exists with: `web: gunicorn main:app`
- [x] `runtime.txt` exists with: `python-3.12.7`
- [x] `requirements.txt` includes `gunicorn`

#### Database Setup (if using PostgreSQL)
- [ ] Add Heroku Postgres addon:
  ```bash
  heroku addons:create heroku-postgresql:mini
  ```
- [ ] Verify DATABASE_URL is set: `heroku config:get DATABASE_URL`
- [ ] Add `psycopg2-binary` to requirements.txt

#### Deployment
- [ ] Deploy: `git push heroku main`
- [ ] Monitor logs: `heroku logs --tail`
- [ ] Open app: `heroku open`
- [ ] Scale if needed: `heroku ps:scale web=1:standard-1x`

#### Post-Deployment
- [ ] Test all major features
- [ ] Check error logs for warnings
- [ ] Monitor memory usage: `heroku ps`
- [ ] Set up monitoring/alerts

---

### Railway Deployment

#### Setup
- [ ] Create account at railway.app
- [ ] Install Railway CLI (optional): `npm i -g @railway/cli`
- [ ] Connect GitHub repository

#### Configuration
- [ ] Add repository to Railway
- [ ] Configure environment variables in Settings → Variables:
  - SESSION_SECRET
  - FLASK_ENV=production
  - Other API keys
- [ ] Railway auto-detects `Procfile`

#### Deployment
- [ ] Push to GitHub (auto-deploys)
- [ ] Or manual deploy via CLI: `railway up`
- [ ] Check deployment logs
- [ ] Get deployment URL from dashboard

#### Post-Deployment
- [ ] Test application
- [ ] Monitor resource usage
- [ ] Configure custom domain (optional)

---

### Docker Deployment

#### Setup
- [ ] Create `Dockerfile` (see DEPLOYMENT_GUIDE.md)
- [ ] Create `.dockerignore`:
  ```
  .env
  .venv
  __pycache__
  *.pyc
  .git
  ```

#### Build
- [ ] Build image:
  ```bash
  docker build -t roboto-sai .
  ```
- [ ] Test locally:
  ```bash
  docker run -p 5000:5000 --env-file .env roboto-sai
  ```

#### Deploy to Registry
- [ ] Tag image:
  ```bash
  docker tag roboto-sai your-registry/roboto-sai:latest
  ```
- [ ] Push to registry:
  ```bash
  docker push your-registry/roboto-sai:latest
  ```

#### Deploy to Cloud
- [ ] Deploy to Google Cloud Run / AWS ECS / Azure Container Instances
- [ ] Configure environment variables in cloud console
- [ ] Set up auto-scaling and health checks

---

## Post-Deployment Verification

### Immediate Checks (First 5 minutes)
- [ ] Application responds at deployed URL
- [ ] Home page loads without errors
- [ ] Check application logs for errors
- [ ] Test basic functionality (chat interface)
- [ ] Verify HTTPS is working

### Functional Testing (First hour)
- [ ] Test user authentication (if applicable)
- [ ] Test voice processing features
- [ ] Test API integrations (OpenAI, xAI, etc.)
- [ ] Test database operations
- [ ] Check quantum features (if enabled)
- [ ] Verify GitHub integration works

### Performance Testing
- [ ] Page load time < 3 seconds
- [ ] API response time < 500ms
- [ ] Memory usage within limits
- [ ] No memory leaks over time
- [ ] Handle concurrent users (if applicable)

### Security Checks
- [ ] HTTPS enabled and enforced
- [ ] No sensitive data in logs
- [ ] Environment variables not exposed
- [ ] CORS configured properly
- [ ] Rate limiting in place (if needed)

---

## Monitoring & Maintenance

### Set Up Monitoring
- [ ] Configure application logging
- [ ] Set up error tracking (Sentry, Rollbar, etc.)
- [ ] Enable performance monitoring
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)
- [ ] Configure alerts for:
  - Application errors
  - High memory usage
  - Slow response times
  - Downtime

### Regular Maintenance
- [ ] Review logs weekly
- [ ] Update dependencies monthly:
  ```bash
  pip list --outdated
  pip install --upgrade package_name
  ```
- [ ] Backup database regularly
- [ ] Review and rotate API keys quarterly
- [ ] Check for security vulnerabilities:
  ```bash
  pip install safety
  safety check
  ```

---

## Rollback Plan

### If Deployment Fails

#### Heroku
```bash
# Rollback to previous version
heroku rollback

# Or specific release
heroku releases
heroku rollback v123
```

#### Railway/Render
- Use platform UI to rollback to previous deployment

#### Docker
```bash
# Deploy previous image version
docker pull your-registry/roboto-sai:previous-tag
docker run ...
```

### Common Rollback Scenarios
- [ ] Build fails → Check logs, fix issues, redeploy
- [ ] App crashes on startup → Check environment variables
- [ ] Database migration fails → Rollback code and migration
- [ ] High error rate → Rollback and investigate logs

---

## Troubleshooting Quick Reference

### App Won't Start
1. Check logs for error messages
2. Verify all environment variables are set
3. Ensure DATABASE_URL is correct
4. Check if SESSION_SECRET is set
5. Verify gunicorn is installed

### 500 Internal Server Error
1. Check application logs
2. Verify database connectivity
3. Check if API keys are valid
4. Look for missing dependencies
5. Test locally with same settings

### Slow Performance
1. Check memory usage
2. Review database queries
3. Enable caching
4. Optimize heavy dependencies
5. Scale up resources

### Database Issues
1. Verify DATABASE_URL format
2. Check database credentials
3. Ensure database migrations ran
4. Check connection limits
5. Review database logs

---

## Success Criteria

Your deployment is successful when:

✅ Application accessible via HTTPS
✅ All pages load without errors
✅ Core features work as expected
✅ No critical errors in logs
✅ Performance is acceptable
✅ Monitoring is in place
✅ Backup strategy implemented
✅ Team can access and manage deployment

---

## Additional Resources

- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Comprehensive deployment guide
- [README.md](./README.md) - Project overview
- [verify_deployment.py](./verify_deployment.py) - Automated deployment checks

---

**Prepared by**: Roberto Villarreal Martinez
**Last Updated**: November 2025

**Questions?** Open an issue on GitHub or contact the maintainer.
