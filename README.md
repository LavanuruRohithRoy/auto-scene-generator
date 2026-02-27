# AI Shorts Engine

A fully local AI-powered short video generation pipeline.

This system automatically generates:

- Structured educational scripts (LLM)
- Scene abstraction with timing
- Voice narration (TTS)
- AI-generated images (Stable Diffusion)
- Media assets ready for video assembly

Designed for batch short-form educational content generation and system architecture learning.

---

## Architecture Overview

Pipeline Flow:

1. Topic Input  
2. Script Generation (Ollama + Mistral 7B)  
3. Scene Builder (Text → Timed Segments)  
4. Audio Engine (TTS + Real Duration Detection)  
5. Image Engine (Stable Diffusion local CPU)  
6. Video Assembly (FFmpeg – upcoming stage)  
7. Optional Automation (n8n Docker orchestration)

Each layer is modular and independent.

---

## System Requirements

This project runs fully locally. Performance depends heavily on hardware.

### Minimum Recommended

- 16GB RAM
- Modern multi-core CPU
- 10GB+ free disk space (model downloads)
- Python 3.11+

### GPU

GPU is NOT required.

Stable Diffusion is configured to run on CPU.

If you have a modern NVIDIA GPU (8GB+ VRAM), the system can later be upgraded to GPU acceleration.

---

## Performance Expectations (CPU Setup)

Performance varies depending on:

- CPU speed
- Available RAM
- Disk speed
- Background processes

Typical timings (CPU-only system):

- Script generation (Mistral 7B): ~60–100 seconds
- Image generation (Stable Diffusion CPU): ~60–120 seconds per image
- Audio generation (gTTS): <3 seconds per scene

This system is designed for batch processing, not real-time serving.

---

## Project Structure

```

ai-shorts-engine/
│
├── scripts/
│   ├── script_engine.py
│   ├── scene_engine.py
│   ├── audio_engine.py
│   └── image_engine.py
│
├── assets/
│   ├── audio/
│   └── images/
│
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md

```

---

## Technologies Used

### AI / ML
- Ollama (local LLM runtime)
- Mistral 7B
- Stable Diffusion v1.5 (via diffusers, CPU mode)

### Audio
- gTTS (Text-to-Speech)
- FFmpeg (duration probing and future video assembly)

### Automation
- n8n (Docker-based optional workflow automation)

---

## Setup Instructions

### 1. Clone Repository

```

git clone <your_repo_url>
cd ai-shorts-engine

```

---

### 2. Create Virtual Environment

```

python -m venv venv
venv\Scripts\activate

```

---

### 3. Install CPU PyTorch

```

pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)

```

---

### 4. Install Project Dependencies

```

pip install -r requirements.txt

```

---

### 5. Install Ollama

Download from:

https://ollama.com

Pull the model:

```

ollama pull mistral

```

Start Ollama:

```

ollama serve

```

---

### 6. Run Script Engine

```

python scripts/script_engine.py

```

Generates structured JSON script.

---

### 7. Run Scene Builder

```

python scripts/scene_engine.py

```

Converts script into timed scenes.

---

### 8. Run Audio Engine

```

python scripts/audio_engine.py

```

Generates:
- MP3 narration files
- Real duration metadata

---

### 9. Run Image Engine

First run downloads Stable Diffusion (~4–7GB).

```

python scripts/image_engine.py

```

Generates scene images locally.

---

## Environment Variables

This project currently runs fully locally and does NOT require API keys.

However, `.env.example` is included for future scalability.

Example `.env.example`:

```

HF_API_TOKEN=
REPLICATE_API_TOKEN=
YOUTUBE_API_KEY=

```

You do NOT need to fill these for the current local setup.

If future external APIs are added, create a `.env` file (not committed to git) and place secrets there.

`.env` must NEVER be committed.

---

## Version Control Rules

### Safe to Commit

- All Python scripts
- requirements.txt
- README.md
- .env.example

### Never Commit

- venv/
- assets/
- Model cache directories
- .env
- API keys
- Generated media files

`.gitignore` already excludes these.

---

## Why Fully Local?

- No unstable public API dependencies
- No rate limits
- No external cost
- Full control over inference
- Reproducible environment
- Clean system design learning

---

## Current Project Status

✔ Script Generation  
✔ Scene Abstraction  
✔ Audio Generation  
✔ Local Image Generation  
⬜ Video Assembly (next stage)  
⬜ Full Automation Integration  

---

## Future Enhancements

- GPU acceleration
- Ken Burns animation for static images
- Background music integration
- Subtitle generation
- YouTube upload automation
- Metadata auto-generation
- Batch queue system
- Scene transition effects

---

## License

Educational and experimental use.
```
