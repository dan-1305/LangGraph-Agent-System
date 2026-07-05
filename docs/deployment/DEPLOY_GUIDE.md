# 🚀 Deployment Guide (VPS / Cloud)

This guide walks you through deploying the **LangGraph Agent System** to a Virtual Private Server (VPS) such as AWS EC2, DigitalOcean Droplet, or Hetzner using Docker Compose and Nginx.

## Step 1: Provision a Server
1. Create a VPS with at least **2GB RAM** and **2 vCPUs** (Ubuntu 22.04 LTS recommended).
2. SSH into your server:
   ```bash
   ssh root@your_server_ip
   ```

## Step 2: Install Docker and Git
Run the following commands on your server:
```bash
# Update system
apt update && apt upgrade -y

# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install docker-compose -y

# Install Git and Nginx
apt install git nginx certbot python3-certbot-nginx -y
```

## Step 3: Clone Repository and Setup Env
```bash
git clone https://github.com/yourusername/LangGraph_Agent_System.git
cd LangGraph_Agent_System

# Setup Environment variables
cp .env.example .env
nano .env # Fill in your API keys!
```

## Step 4: Run the System
```bash
# Build and start all containers in detached mode
docker-compose up -d --build
```
*Wait a few minutes for the images to build and download.*

## Step 5: Configure Nginx and SSL
1. Copy the Nginx configuration to the server's Nginx directory:
   ```bash
   cp nginx/nginx.conf /etc/nginx/sites-available/langgraph
   ln -s /etc/nginx/sites-available/langgraph /etc/nginx/sites-enabled/
   ```
2. Open `/etc/nginx/sites-available/langgraph` and replace `example.com` with your actual domain name.
3. Test Nginx and restart:
   ```bash
   nginx -t
   systemctl restart nginx
   ```
4. Obtain SSL Certificate (HTTPS):
   ```bash
   certbot --nginx -d example.com -d www.example.com
   ```

## Step 6: Verify Deployment
Navigate to your domain in a web browser:
- `https://example.com/real-estate/` (Real Estate App)
- `https://example.com/sillytavern/` (World Card Generator)
- `https://example.com/jarvis/` (Jarvis Dashboard)

**Done!** Your AI Monorepo is now live in Production.
