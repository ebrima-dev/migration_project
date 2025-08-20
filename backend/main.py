import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Allow frontend on localhost:5173 or 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data/samples"
os.makedirs(DATA_DIR, exist_ok=True)

@app.post("/upload-file/")
async def ingest(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return JSONResponse(content={"filename": file.filename, "location": file_path})
    

@app.get("/profile/")
async def profile():
    return {"message": "profiling endpoint ready"}