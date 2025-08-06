# 🚀 Deployment Guide - Deerfields Mall Gamification System

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Development Deployment](#development-deployment)
4. [Production Deployment](#production-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Configuration](#configuration)
7. [Security Setup](#security-setup)
8. [Performance Optimization](#performance-optimization)
9. [Monitoring](#monitoring)
10. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: Minimum 2GB RAM (4GB recommended)
- **Storage**: Minimum 1GB free space
- **Network**: Internet access for package installation

### Software Dependencies
- **Flask**: Web framework
- **PostgreSQL**: Primary database (sharded via DSN suffix)
- **Redis**: Optional, for enhanced caching
- **Docker**: Optional, for containerized deployment

## ⚡ Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd mall-gamification-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Configuration
```bash
# Copy environment file
cp env.example .env

# Edit configuration (optional)
nano .env
```

### 3. Initialize Database
```bash
# Create PostgreSQL databases for each shard
createdb mall_gamification_shard0
# createdb mall_gamification_shard1  # repeat if SHARD_COUNT > 1

# Run migrations across shards
alembic upgrade head
```
Set `SHARD_COUNT` in your environment to control how many databases are
created. The application uses a hash of `user_id` to route queries to the
appropriate shard.

### 4. Start Application
```bash
# Start basic web interface
python web_interface.py

# Or start optimized version
python optimized_web_interface.py
```

### 5. Access Application
- **Main URL**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **Admin Dashboard**: http://localhost:5000/admin

## 🛠️ Development Deployment

### Step 1: Environment Setup
```bash
# Set development environment
export FLASK_ENV=development
export DEBUG=True
export LOG_LEVEL=DEBUG

# Or use .env file
echo "FLASK_ENV=development" >> .env
echo "DEBUG=True" >> .env
echo "LOG_LEVEL=DEBUG" >> .env
```

### Step 2: Database Setup
```bash
# Create PostgreSQL databases for each shard
createdb mall_gamification_shard0

# Run migrations
alembic upgrade head

# Create test data (optional)
python -c "
from mall_gamification_system import MallGamificationSystem
system = MallGamificationSystem()
system.create_test_data()
print('Test data created successfully')
"
```
Set the `SHARD_COUNT` environment variable before running migrations if more
than one shard is required. The application uses a hash of `user_id` for shard
selection.

### Step 3: Run Tests
```bash
# Run comprehensive system check
python comprehensive_system_check.py

# Run specific test suites
python test_security_features.py
python test_performance_module_comprehensive.py
python test_web_interface_comprehensive.py
python test_integration_comprehensive.py
```

### Step 4: Start Development Server
```bash
# Start with auto-reload
python web_interface.py

# Or use Flask development server
export FLASK_APP=web_interface.py
flask run --host=0.0.0.0 --port=5000 --debug
```

### Step 5: Development Tools
```bash
# Access development tools
# pgAdmin: http://localhost:8080 (if using Docker)
# Redis Commander: http://localhost:8081 (if using Docker)
# Grafana: http://localhost:3000 (if using Docker)
```

## 🏭 Production Deployment

### Step 1: Server Preparation
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv redis-server nginx -y

# Create application user
sudo useradd -m -s /bin/bash mallapp
sudo usermod -aG sudo mallapp
```

### Step 2: Application Setup
```bash
# Switch to application user
sudo su - mallapp

# Clone repository
git clone <repository-url> /home/mallapp/mall-gamification
cd /home/mallapp/mall-gamification

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Production Configuration
```bash
# Copy and configure environment
cp env.example .env
nano .env

# Set production values
FLASK_ENV=production
DEBUG=False
LOG_LEVEL=WARNING
SECRET_KEY=your-secure-secret-key-here
JWT_SECRET_KEY=your-secure-jwt-secret-key-here
DATABASE_URL=sqlite:///prod_mall_gamification.db
REDIS_ENABLED=True
REDIS_URL=redis://localhost:6379/0
MISSION_TEMPLATE_CACHE_BACKEND=redis
MISSION_TEMPLATE_CACHE_TTL=600
```

### Step 4: Database Setup
```bash
# Initialize production database
alembic upgrade head

# Set proper permissions
chmod 600 prod_mall_gamification.db
chown mallapp:mallapp prod_mall_gamification.db
```

### Step 5: Systemd Service Setup
```bash
# Create systemd service file
sudo nano /etc/systemd/system/mall-gamification.service
```

```ini
[Unit]
Description=Mall Gamification System
After=network.target

[Service]
Type=simple
User=mallapp
WorkingDirectory=/home/mallapp/mall-gamification
Environment=PATH=/home/mallapp/mall-gamification/venv/bin
ExecStart=/home/mallapp/mall-gamification/venv/bin/python optimized_web_interface.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable mall-gamification
sudo systemctl start mall-gamification
sudo systemctl status mall-gamification
```

### Step 6: Nginx Configuration
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/mall-gamification
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/mallapp/mall-gamification/static;
        expires 30d;
    }
}
```

```bash
# Enable site and restart Nginx
sudo ln -s /etc/nginx/sites-available/mall-gamification /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🐳 Docker Deployment

### Step 1: Docker Setup
```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 2: Environment Configuration
```bash
# Copy environment file
cp env.example .env

# Edit Docker-specific settings
nano .env
```

```env
# Docker-specific settings
DATABASE_URL=postgresql://mall_user:mall_password@db:5432/mall_gamification
REDIS_URL=redis://redis:6379/0
FLASK_ENV=production
DEBUG=False
```

### Step 3: Development Deployment
```bash
# Start development services
docker-compose --profile development up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f app
```

### Step 4: Production Deployment
```bash
# Start production services
docker-compose --profile production up -d

# Check all services
docker-compose ps

# Monitor logs
docker-compose logs -f
```

### Step 5: Staging Deployment
```bash
# Start staging services
docker-compose --profile staging up -d

# Access monitoring
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
```

## ⚙️ Configuration

### Environment Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Flask environment | development | Yes |
| `SECRET_KEY` | Flask secret key | auto-generated | Yes |
| `JWT_SECRET_KEY` | JWT signing key | auto-generated | Yes |
| `DATABASE_URL` | Database connection | sqlite:///mall_gamification.db | Yes |
| `REDIS_URL` | Redis connection | redis://localhost:6379/0 | No |
| `REDIS_ENABLED` | Enable Redis caching | True | No |
| `MISSION_TEMPLATE_CACHE_BACKEND` | Mission template cache backend (`memory` or `redis`) | memory | No |
| `MISSION_TEMPLATE_CACHE_TTL` | Cache TTL for mission templates (seconds) | 300 | No |
| `LOG_LEVEL` | Logging level | INFO | No |
| `DEBUG` | Debug mode | False | No |
| `MFA_ENABLED` | Enable MFA | True | No |
| `CSRF_ENABLED` | Enable CSRF protection | True | No |

### Database Configuration
```bash
# SQLite (default)
DATABASE_URL=sqlite:///mall_gamification.db

# PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost/mall_gamification

# MySQL
DATABASE_URL=mysql://user:pass@localhost/mall_gamification
```

### Redis Configuration
```bash
# Local Redis
REDIS_URL=redis://localhost:6379/0

# Remote Redis
REDIS_URL=redis://redis-server:6379/0

# Redis with authentication
REDIS_URL=redis://:password@redis-server:6379/0
```

### Mission Template Cache
```bash
# In-memory cache (default)
MISSION_TEMPLATE_CACHE_BACKEND=memory
MISSION_TEMPLATE_CACHE_TTL=300

# Redis cache
MISSION_TEMPLATE_CACHE_BACKEND=redis
MISSION_TEMPLATE_CACHE_TTL=600

# Refresh cached templates (after updates)
python -c "from ai_mission_generator import AIMissionGenerator; AIMissionGenerator().refresh_template_cache()"
```

## 🔐 Security Setup

### Step 1: Secret Keys
```bash
# Generate secure secret keys
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

### Step 2: SSL/TLS Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Step 3: Firewall Configuration
```bash
# Configure UFW firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### Step 4: Security Headers
```bash
# Add security headers to Nginx
sudo nano /etc/nginx/sites-available/mall-gamification
```

```nginx
# Add to server block
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## ⚡ Performance Optimization

### Step 1: Redis Caching
```bash
# Install Redis
sudo apt install redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf
```

```conf
# Performance settings
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### Step 2: Database Optimization
```bash
# Run database optimization
alembic upgrade head

# Create indexes
python -c "
from database import MallDatabase
db = MallDatabase()
db.create_indexes()
print('Indexes created')
"
```

### Step 3: Application Optimization
```bash
# Use optimized web interface
python optimized_web_interface.py

# Enable performance monitoring
export PERFORMANCE_MONITORING=True
export ENABLE_METRICS=True
```

### Step 4: Nginx Optimization
```bash
# Configure Nginx for performance
sudo nano /etc/nginx/nginx.conf
```

```nginx
# Worker processes
worker_processes auto;

# Connection settings
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

# Gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
```

## 📊 Monitoring

### Step 1: Health Checks
```bash
# Manual health check
curl http://localhost:5000/health

# Automated health check
while true; do
    curl -f http://localhost:5000/health || echo "Health check failed"
    sleep 30
done
```

### Step 2: Log Monitoring
```bash
# View application logs
tail -f logs/app.log

# View security logs
tail -f logs/security.log

# View performance logs
tail -f logs/performance.log
```

### Step 3: System Monitoring
```bash
# Monitor system resources
htop
iotop
nethogs

# Monitor application
ps aux | grep python
netstat -tlnp | grep 5000
```

### Step 4: Prometheus & Grafana
```bash
# Start monitoring stack
docker-compose --profile production up -d prometheus grafana

# Access Grafana
# URL: http://localhost:3000
# Username: admin
# Password: admin_password
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 2. Database Issues
```bash
# Check database connection
python -c "
from database import MallDatabase
db = MallDatabase()
print('Database connection:', db.check_connection())
"

# Reset database (development only)
rm mall_gamification.db
alembic upgrade head
```

#### 3. Redis Issues
```bash
# Check Redis connection
redis-cli ping

# Restart Redis
sudo systemctl restart redis

# Check Redis logs
sudo journalctl -u redis -f
```

#### 4. Port Conflicts
```bash
# Check port usage
sudo netstat -tlnp | grep 5000

# Kill process using port
sudo fuser -k 5000/tcp
```

#### 5. Permission Issues
```bash
# Fix file permissions
sudo chown -R mallapp:mallapp /home/mallapp/mall-gamification
sudo chmod -R 755 /home/mallapp/mall-gamification
sudo chmod 600 /home/mallapp/mall-gamification/.env
```

### Debug Mode
```bash
# Enable debug mode
export FLASK_ENV=development
export DEBUG=True
export LOG_LEVEL=DEBUG

# Start with debug
python web_interface.py
```

### Log Analysis
```bash
# View recent errors
grep -i error logs/app.log | tail -20

# View security events
grep -i security logs/security.log | tail -20

# View performance issues
grep -i slow logs/performance.log | tail -20
```

## 📞 Support

### Getting Help
- **Documentation**: Check README.md and other .md files
- **Logs**: Check application and system logs
- **Tests**: Run test suites to identify issues
- **Health Check**: Use /health endpoint for system status

### Emergency Procedures
```bash
# Stop application
sudo systemctl stop mall-gamification

# Backup database
cp mall_gamification.db mall_gamification.db.backup.$(date +%Y%m%d_%H%M%S)

# Restart application
sudo systemctl start mall-gamification

# Check status
sudo systemctl status mall-gamification
```

### Contact Information
- **Technical Support**: support@deerfields-mall.com
- **Emergency**: +971-XX-XXX-XXXX
- **Documentation**: See README.md and other documentation files

---

**Deerfields Mall Gamification System** - Deployment Guide v1.0
Last updated: December 2024 