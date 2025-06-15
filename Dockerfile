FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone Moshi repository
RUN git clone https://github.com/kyutai-labs/moshi.git .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir gradio fastrtc[vad,stt,tts]

# Set environment variables
ENV HF_REPO=kyutai/moshiko-pytorch-bf16
ENV PYTHONUNBUFFERED=1
# HF_TOKEN will be provided at runtime via Koyeb secrets

# Create a custom server script with FastRTC integration
COPY server.py /app/custom_server.py

# Expose port
EXPOSE 8998

# Run the server
CMD ["python", "/app/custom_server.py"]