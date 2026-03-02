from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from pipeline import run_pipeline

app = FastAPI()


class TopicRequest(BaseModel):
    topic: str


@app.post("/generate")
def generate(request: TopicRequest):
    try:
        result = run_pipeline(request.topic)

        return {
            "status": "completed",
            "video_path": result.get("video_path"),
            "youtube_video_id": result.get("youtube_video_id")
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )