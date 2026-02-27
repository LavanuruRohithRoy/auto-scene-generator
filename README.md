# AI Shorts Engine (Local Autonomous Pipeline)

An end-to-end fully local AI-powered short video generation system.

This system automatically generates:

- Structured script (LLM – Ollama)
- Scene breakdown
- Neural voice narration
- AI-generated cinematic images (Stable Diffusion)
- Background music mix
- Final stitched vertical video (FFmpeg)
- API endpoint for automation (FastAPI)
- n8n workflow integration (Docker self-hosted)

Everything runs locally. No cloud dependency required.

---

# System Architecture

User Topic
   ↓
Ollama (LLM – Script JSON)
   ↓
Scene Engine (Text → Timed Scenes)
   ↓
Audio Engine (Edge TTS)
   ↓
Image Engine (Stable Diffusion v1.5)
   ↓
Video Engine (FFmpeg Assembly + BGM)
   ↓
Final MP4 Output
   ↓
FastAPI Endpoint (/generate)
   ↓
n8n Workflow Automation

---

# Core Technologies Used

## 1. Ollama (LLM)
- Model: mistral
- Purpose: Generates structured JSON script
- Runs locally on port 11434
- No API keys required

Used for:
- Hook
- Body
- Visual prompts
- CTA

---

## 2. Stable Diffusion (runwayml/stable-diffusion-v1-5)
- Runs locally via diffusers
- ~5.5GB model download
- CPU-based in current setup (GPU optional)

Used for:
- Scene image generation
- 512x512 → scaled to 1280x720 in video phase

Note:
Performance depends heavily on:
- CPU cores
- RAM
- GPU availability

---

## 3. Edge-TTS
- Neural voice generation
- Produces MP3 narration per scene
- Voice parameters adjustable

---

## 4. FFmpeg
- Scene rendering
- Image → video conversion
- Audio mixing
- Scene transitions
- Final merge

Current Output:
- 1280x720
- 25fps
- AAC audio
- H264 encoding

---

## 5. FastAPI
- Exposes pipeline as HTTP service
- Endpoint: POST /generate?topic=...
- Runs on port 8000
- Enables workflow automation

---

## 6. n8n (Docker Local)
- Self-hosted workflow automation
- HTTP Request → FastAPI trigger
- Manual trigger supported
- Uses host.docker.internal to reach local API

---

# Project Structure

```

shorts-engine/
│
├── scripts/
│   ├── script_engine.py
│   ├── scene_engine.py
│   ├── audio_engine.py
│   ├── image_engine.py
│   ├── video_engine.py
│   ├── pipeline.py
│   ├── api_server.py
│   │
│   ├── config.py
│   ├── schema.py
│   └── utils.py
│
├── assets/
│   ├── audio/          # Generated voice files (ignored in git)
│   ├── images/         # Generated SD images (ignored in git)
│   ├── music/          # Background music (optional track)
│   ├── temp/           # Temporary video segments (ignored)
│   └── output/         # Final rendered videos (ignored)
│
├── venv/               # Virtual environment (ignored)
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```

git clone <repo>
cd shorts-engine

```

---

## 2. Create Virtual Environment

```

python -m venv venv
venv\Scripts\activate

```

Verify:

```

where python

```

It must point to:
```

shorts-engine\venv\Scripts\python.exe

```

---

## 3. Install Dependencies

```

pip install -r requirements.txt

```

---

## 4. Install & Run Ollama

Install Ollama.

Pull model:

```

ollama pull mistral

```

Start Ollama automatically (runs in background).

---

## 5. First Run (Manual Test)

```

python scripts/pipeline.py

```

This will:
- Generate script
- Create scenes
- Generate audio
- Generate images
- Build final video

Output:
```

assets/output/final_video.mp4

```

---

# Running API Server

Important: Activate venv first.

```

venv\Scripts\activate
python scripts/api_server.py

```

Server runs on:
```

[http://localhost:8000](http://localhost:8000)

```

Test in browser:
```

[http://localhost:8000/docs](http://localhost:8000/docs)

```

Test endpoint:
```

POST /generate?topic=Black Holes

```

---

# n8n Integration

If running n8n via Docker:

Use URL:

```

[http://host.docker.internal:8000/generate?topic=YourTopic](http://host.docker.internal:8000/generate?topic=YourTopic)

```

Method:
POST

Do NOT send topic in body.
Send as query parameter.

---

# Performance Notes

This system is hardware dependent.

Performance depends on:

- CPU cores
- Available RAM
- GPU availability (currently CPU mode)
- Disk speed (model loading)
- Stable Diffusion inference speed

Expected timings (CPU mode):

- Script generation: 30–60s
- Image generation (4 scenes): 3–6 min
- Video assembly: <30s

Total: ~5–8 minutes per video (CPU-only system)

GPU acceleration can reduce this drastically.

---

# Important Operational Notes

- Deleting assets/audio and assets/images before rerun is safe.
- assets/temp is auto-managed.
- Stable Diffusion loads once per pipeline execution.
- Always run FastAPI inside virtual environment.
- Never mix global Python with venv.

---

# Known Limitations (Current Version)

- CPU-only image generation
- Slideshow style (not true 3D)
- Basic fade transitions
- No motion synthesis yet
- No subtitle rendering yet

---

# Future Upgrade Directions

- GPU acceleration (CUDA)
- Motion interpolation
- Camera zoom effects
- Subtitle overlay (burned-in)
- Better voice tuning
- Parallel processing
- Model warm-loading
- Persistent SD pipeline memory

---

# Requirements.txt

Ensure it includes:

```

fastapi
uvicorn
requests
edge-tts
diffusers
transformers
torch
Pillow
python-dotenv
replicate

```

---

# .gitignore Essentials

```

venv/
**pycache**/
*.pyc
assets/audio/
assets/images/
assets/temp/
assets/output/
.env

```

---

# Final Output

Final rendered file:

```

assets/output/final_video.mp4

```

Fully local.
Fully automated.
Pipeline-ready.
Workflow-ready.

---

System Status: Functional End-to-End  
Automation Status: FastAPI + n8n Connected  
Deployment Mode: Local  
Dependency Mode: Offline-first  

```
# License

Educational and experimental use.
