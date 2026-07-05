# ==============================================================================
# 🐳 MASTER DOCKERFILE FOR LANGGRAPH_AGENT_SYSTEM
# ==============================================================================
# This Dockerfile is designed for Production-level deployment of the Monorepo.
# It uses a slim Python base image to keep the footprint small while installing
# all necessary dependencies across all sub-projects.
# ==============================================================================

FROM python:3.10-slim

# Set labels for container image metadata
LABEL maintainer="AI Product Manager / DevOps Lead"
LABEL description="Production environment for LangGraph_Agent_System"

# ------------------------------------------------------------------------------
# 1. Environment Setup
# ------------------------------------------------------------------------------
WORKDIR /app

# Ensure Python output is sent straight to terminal (no buffering) and no .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# ------------------------------------------------------------------------------
# 2. Install System Dependencies
# ------------------------------------------------------------------------------
# We install essential build tools and dependencies for standard Python packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# 3. Python Dependencies (Caching optimization)
# ------------------------------------------------------------------------------
# Copy root requirements first
COPY requirements.txt .

# Install root requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Find all requirements.txt inside projects/ and install them automatically.
# This prevents manual updates to the Dockerfile when new sub-projects are added.
RUN find projects -name "requirements.txt" -exec pip install --no-cache-dir -r {} +

# ------------------------------------------------------------------------------
# 4. Playwright Setup (For Web Scrapers)
# ------------------------------------------------------------------------------
# Install Chromium browser for headless scraping (Anti-Cloudflare, etc.)
# We use --with-deps to pull OS-level dependencies required by Chromium.
RUN playwright install --with-deps chromium

# ------------------------------------------------------------------------------
# 5. Entrypoint Configuration
# ------------------------------------------------------------------------------
# By default, running the container will open the interactive dashboard.
# However, in production (via docker-compose), this CMD will be overridden 
# to run specific daemon services (Flask, Streamlit, Scheduler, etc.)
CMD ["python", "dashboard.py"]