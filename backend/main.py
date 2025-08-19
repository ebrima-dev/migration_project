import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil

app = FastAPI()

# Allow frontend on localhose:5173 or 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data/samples"
os.makedirs(DATA_DIR, exist_ok=True)

@app.post("/ingest/")
async def ingest(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "saved", "path": file_path}

@app.get("/profile/")
async def profile():
    return {"message": "profiling endpoint ready"}