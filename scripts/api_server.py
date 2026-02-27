from fastapi import FastAPI
from pipeline import run_pipeline
import uvicorn
from pydantic import BaseModel

app = FastAPI()
class TopicRequest(BaseModel):
    topic: str

@app.post("/generate")
def generate(request: TopicRequest):
    result = run_pipeline(request.topic)
    return {"status": "success", "output": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)