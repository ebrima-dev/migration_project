import os
import shutil
import pandas as pd
import chardet
import csv
import io
import re
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


### Create App ###
app = FastAPI()

# Allow frontend on localhost:5173 or 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### Generate Directories ###
DATA_DIR = "data/samples"
os.makedirs(DATA_DIR, exist_ok=True)

### Helper Functions ###

# Detect delimiter by sampling the file
def detect_delimiter(sample: str):
    delimiters = [",", ";", "|", "\t"]
    counts = {d: sample.count(d) for d in delimiters}
    return max(counts, key=counts.get)

# Infer simple data type checks
def validate_data(df: pd.DataFrame):
    issues = []

    email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone_pattern = re.compile(r"^[\d\s\-\+()]{6,}$")
    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%Y.%m.%d", "%d-%b-%y", "%Y-%m-%d"]

    for col in df.columns:
        for i, val in enumerate(df[col]):
            if pd.isna(val) or str(val).strip().lower() in ["", "na", "n/a", "null", "none", "unkown"]:
                issues.append({"row": i+1, "column": col, "issue": "Missing or placeholder value"})
                continue
            sval = str(val).strip()

            # Simple rules by column name
            if "email" in col.lower():
                if not email_pattern.match(sval):
                    issues.append({"row": i+1, "column": col, "issue": f"Invalid phone {sval}"})
            
            elif "phone" in col.lower():
                if not phone_pattern.match(sval):
                    issues.append({"row": i+1, "column": col, "issue": f"Invalid phone '{sval}'"})
            
            elif "date" in col.lower():
                parsed = False
                for fmt in date_formats:
                    try:
                        pd.to_datetime(sval, format=fmt, errors="raise")
                        parsed = True
                        break
                    except Exception:
                        continue
                if not parsed:
                    issues.append({"row": i+1, "column": col, "issue": f"Inconsistent date format '{sval}'"})
 
    return issues

# To handle multiple delimiters
def normalize_delimiters(raw: str):
    # Define all possible delimiters
    possible_delimiters = [",", ";", "|", "\t"]
    found = {d for d in possible_delimiters if d in raw}

    # Replace them all with a single delimiter (comma)
    normalized = raw
    for d in found:
        normalized = normalized.replace (d, ",")

    return normalized, found


### Create Endpoints ###
@app.post("/upload-file/")
async def ingest(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return JSONResponse(content={"filename": file.filename, "location": file_path})

@app.get("/csv-cleaner/")
async def csv_cleaner():
    pass

# May have to change how this is done so it reads from the already uploaded file
@app.post("/validate-csv")
async def validate_csv(file: UploadFile = File(...)):
    # Detect encoding
    raw = await file.read()
    encoding = chardet.detect(raw)["encoding"] or "utf-8"

    # Decode file
    decoded = raw.decode(encoding, errors="replace")

    # Detect delimiter
    # delimiter = detect_delimiter(decoded[:1000])

    # Normalize delimiters
    normalized, delimiters_found = normalize_delimiters(decoded)

    # Load CSV
    df = pd.read_csv(io.StringIO(decoded), delimiter=",", engine="python")

    # Validate data
    issues = validate_data(df)

    return JSONResponse({
        "encoding": encoding,
        "delimiters_detected": list(delimiters_found),
        "final_delimiter_used": ",",
        "columns": df.columns.tolist(),
        "issues_found": len(issues),
        "issues": issues[:50] # limit output
    })

@app.get("/profile/")
async def profile():
    return {"message": "profiling endpoint ready"}