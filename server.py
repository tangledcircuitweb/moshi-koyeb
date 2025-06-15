import os
import threading
import numpy as np
from fastapi import FastAPI
from fastrtc import Stream, ReplyOnPause
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Audio processing function for Moshi integration
def process_audio(audio: tuple[int, np.ndarray]):
    """Process audio through Moshi - placeholder for now"""
    # audio is a tuple of (sample_rate, audio_data)
    sample_rate, audio_data = audio
    
    # For now, just echo the audio back
    # In production, this would send audio to Moshi and return the response
    yield audio

# Create FastRTC stream
stream = Stream(
    handler=ReplyOnPause(process_audio),
    modality="audio",
    mode="send-receive"
)

# Mount FastRTC stream to FastAPI
stream.mount(app)

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
    try:
        # Add the moshi repo to Python path and run server
        os.system("cd /app/moshi_repo && python -m moshi.server --gradio-tunnel --hf-repo $HF_REPO")
    except Exception as e:
        print(f"Moshi server failed to start: {e}")

if __name__ == "__main__":
    # Try to start Moshi server in background if available
    try:
        import sys
        sys.path.insert(0, '/app/moshi_repo')
        import moshi.server
        print("Starting Moshi server in background...")
        moshi_thread = threading.Thread(target=run_moshi_server, daemon=True)
        moshi_thread.start()
        import time
        time.sleep(5)
    except ImportError as e:
        print(f"Moshi not available: {e} - running FastRTC server only")
    
    # Run FastAPI with FastRTC (this will work even without Moshi)
    uvicorn.run("server:app", host="0.0.0.0", port=8998)