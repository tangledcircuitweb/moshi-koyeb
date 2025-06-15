FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone Moshi repository
RUN git clone https://github.com/kyutai-labs/moshi.git moshi_repo

# Install Moshi dependencies first
WORKDIR /app/moshi_repo
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Go back to app directory and copy our files
WORKDIR /app
COPY . .

# Install our additional dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV HF_REPO=kyutai/moshiko-pytorch-bf16
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/moshi_repo:$PYTHONPATH
# HF_TOKEN will be provided at runtime via Koyeb secrets

# Expose port
EXPOSE 8998

# Run the server
CMD ["python", "server.py"]