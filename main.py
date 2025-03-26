
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from vision_utils import extract_text
from cert_generator import generate_certificate
import uuid
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# slúž statické súbory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    temp_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(temp_path, "wb") as f:
        f.write(contents)

    text = extract_text(temp_path)
    os.remove(temp_path)

    return {"extracted_text": text}

@app.post("/generate/")
async def generate(data: dict):
    pdf_path = generate_certificate(data)
    return JSONResponse({"message": "Certificate generated", "path": pdf_path})
