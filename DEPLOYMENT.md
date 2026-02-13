# 🚀 Deployment Guide

This guide covers different deployment options for the Faculty Management System.

## Table of Contents
1. [Local Development](#local-development)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Setup Steps

1. **Navigate to project directory**
   ```bash
   cd faculty-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate demo data (optional)**
   ```bash
   python generate_demo_data.py
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open browser to: `http://localhost:8501`
   - Login with: `admin` / `admin123`

### Development Tips
- Edit `app.py` for code changes
- Modify `config.py` for configuration
- Data is stored in `data/` directory
- Streamlit auto-reloads on file changes

---

## Production Deployment

### Option 1: Streamlit Cloud (Recommended)

Streamlit Cloud offers free hosting for Streamlit apps.

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository, branch, and main file (`app.py`)
6. Click "Deploy"

**Configuration:**
- Create `.streamlit/config.toml` for custom settings
- Set secrets in Streamlit Cloud dashboard for sensitive data
- Data will be stored in Streamlit Cloud's file system

**Pros:**
- ✅ Free hosting
- ✅ Automatic updates on git push
- ✅ HTTPS included
- ✅ Easy to use

**Cons:**
- ❌ Limited resources on free tier
- ❌ Public by default (can make private with login)
- ❌ File storage is temporary (resets on sleep)

### Option 2: Heroku

**Steps:**

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create Heroku app**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Create necessary files**
   
   `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
   
   `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku master
   ```

### Option 3: Virtual Private Server (VPS)

For DigitalOcean, Linode, AWS EC2, etc.

**Steps:**

1. **SSH into your server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install Python and dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   ```

3. **Clone/upload your project**
   ```bash
   git clone your-repo-url
   cd faculty-management-system
   ```

4. **Install requirements**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run with systemd (for persistent service)**
   
   Create `/etc/systemd/system/faculty-app.service`:
   ```ini
   [Unit]
   Description=Faculty Management System
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/path/to/faculty-management-system
   ExecStart=/usr/local/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **Enable and start service**
   ```bash
   sudo systemctl enable faculty-app
   sudo systemctl start faculty-app
   ```

7. **Setup Nginx as reverse proxy**
   
   Create `/etc/nginx/sites-available/faculty-app`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

8. **Enable site and restart Nginx**
   ```bash
   sudo ln -s /etc/nginx/sites-available/faculty-app /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

---

## Docker Deployment

### Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  faculty-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_ENABLE_CORS=false
```

### Commands

```bash
# Build image
docker build -t faculty-management .

# Run container
docker run -p 8501:8501 -v $(pwd)/data:/app/data faculty-management

# Or use docker-compose
docker-compose up -d
```

---

## Cloud Deployment

### AWS (Amazon Web Services)

**Option 1: AWS Elastic Beanstalk**
1. Install AWS EB CLI
2. Initialize: `eb init`
3. Create environment: `eb create`
4. Deploy: `eb deploy`

**Option 2: AWS EC2**
- Follow VPS deployment steps above
- Configure security groups to allow port 8501
- Use Elastic IP for static IP address

### Google Cloud Platform

**Option 1: Cloud Run**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/faculty-app
gcloud run deploy --image gcr.io/PROJECT_ID/faculty-app --platform managed
```

**Option 2: Compute Engine**
- Create VM instance
- Follow VPS deployment steps

### Azure

**Azure App Service**
```bash
# Create app
az webapp up --name faculty-app --runtime "PYTHON:3.9"

# Deploy
git push azure master
```

---

## Environment Configuration

### Streamlit Configuration

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### Environment Variables

Create `.env` file (for sensitive data):
```env
DEFAULT_ADMIN_PASSWORD=your-secure-password
SECRET_KEY=your-secret-key
ENVIRONMENT=production
```

**Important:** Add `.env` to `.gitignore`!

---

## Security Best Practices

1. **Change Default Credentials**
   - Change admin password immediately
   - Use strong passwords (12+ characters)

2. **HTTPS/SSL**
   - Use SSL certificates (Let's Encrypt is free)
   - Enable HTTPS for production

3. **Firewall Configuration**
   ```bash
   sudo ufw allow 22/tcp  # SSH
   sudo ufw allow 80/tcp  # HTTP
   sudo ufw allow 443/tcp # HTTPS
   sudo ufw enable
   ```

4. **Regular Backups**
   - Backup `data/` directory regularly
   - Use automated backup solutions
   - Test restore procedures

5. **Access Control**
   - Limit SSH access
   - Use SSH keys instead of passwords
   - Configure fail2ban for brute force protection

---

## Database Migration (Future)

For production at scale, consider migrating to a proper database:

### SQLite (Simple)
- Good for small deployments
- File-based, easy backup
- No separate server needed

### PostgreSQL (Recommended)
- Best for production
- Concurrent access
- Advanced features

### MySQL/MariaDB
- Alternative to PostgreSQL
- Wide hosting support
- Good documentation

---

## Monitoring & Maintenance

### Health Checks

Create `healthcheck.py`:
```python
import requests
import sys

try:
    response = requests.get('http://localhost:8501')
    if response.status_code == 200:
        print("✅ App is running")
        sys.exit(0)
    else:
        print("❌ App returned error")
        sys.exit(1)
except Exception as e:
    print(f"❌ App is down: {e}")
    sys.exit(1)
```

### Log Management
```bash
# View logs
journalctl -u faculty-app -f

# Or for Docker
docker logs -f faculty-app
```

### Automated Backups
```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backups/data_$DATE.tar.gz data/
# Upload to cloud storage (S3, Google Cloud Storage, etc.)
```

---

## Troubleshooting

### Common Issues

**Issue: Port already in use**
```bash
# Find process using port 8501
sudo lsof -i :8501
# Kill process
sudo kill -9 <PID>
```

**Issue: Permission denied on data directory**
```bash
sudo chown -R $USER:$USER data/
chmod 755 data/
```

**Issue: Module not found**
```bash
pip install -r requirements.txt --upgrade
```

**Issue: App doesn't auto-reload**
- Check Streamlit config
- Restart Streamlit server
- Clear browser cache

### Performance Optimization

1. **Enable caching**
   - Use `@st.cache_data` for expensive operations

2. **Optimize data loading**
   - Load data only when needed
   - Use pagination for large datasets

3. **Resource limits (Docker)**
   ```yaml
   services:
     faculty-app:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 2G
   ```

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Migrate to database for shared storage
- Implement session management

### Vertical Scaling
- Increase server resources
- Optimize code performance
- Add caching layer (Redis)

---

## Support & Updates

### Getting Updates
```bash
git pull origin main
pip install -r requirements.txt --upgrade
sudo systemctl restart faculty-app
```

### Rollback
```bash
git log # Find previous commit
git checkout <commit-hash>
sudo systemctl restart faculty-app
```

---

## Checklist for Production

- [ ] Change default admin password
- [ ] Set up HTTPS/SSL
- [ ] Configure firewall
- [ ] Set up automated backups
- [ ] Configure monitoring
- [ ] Test disaster recovery
- [ ] Document access procedures
- [ ] Set up logging
- [ ] Configure error alerting
- [ ] Plan maintenance windows
- [ ] Test scalability
- [ ] Security audit

---

**Questions?** Refer to:
- [Streamlit Docs](https://docs.streamlit.io)
- [Deployment FAQ](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)
- Project README.md

---

**Last Updated:** February 2026  
**Version:** 1.0.0
