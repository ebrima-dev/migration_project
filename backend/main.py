from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/ingest/")
async def ingest(file: UploadFile = File(...)):
    return {"filename": file.filename, "status": "recieved"}

@app.get("/profile/")
async def profile():
    return {"message": "profiling endpoint ready"}