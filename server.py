import os
import asyncio
from fastapi import FastAPI
from fastrtc import RTCApp, Audio, AudioToAudio
import uvicorn
from moshi.server import run_server
import threading

# Initialize FastAPI app
app = FastAPI()

# Initialize FastRTC
rtc = RTCApp()

# Create audio stream handler for Moshi
@rtc.stream(audio=True)
async def moshi_stream(audio: Audio) -> AudioToAudio:
    """WebRTC audio stream handler for Moshi"""
    # This would integrate with Moshi's audio processing
    # For now, we'll create a placeholder that echoes audio
    async for frame in audio:
        # In production, you'd process audio through Moshi here
        yield frame

# Mount FastRTC to FastAPI
rtc.mount(app, path="/rtc")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "moshi-fastrtc"}

# Info endpoint
@app.get("/")
async def info():
    return {
        "service": "Moshi with FastRTC",
        "endpoints": {
            "gradio": "http://localhost:8998",
            "rtc": "/rtc",
            "health": "/health"
        }
    }

def run_moshi_server():
    """Run Moshi server in a separate thread"""
    # This runs the original Moshi Gradio server
    os.system("python -m moshi.server --gradio-tunnel --hf-repo $HF_REPO")

if __name__ == "__main__":
    # Start Moshi server in background thread
    moshi_thread = threading.Thread(target=run_moshi_server, daemon=True)
    moshi_thread.start()
    
    # Run FastAPI with FastRTC
    uvicorn.run(app, host="0.0.0.0", port=8998)