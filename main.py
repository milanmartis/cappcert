from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from vision_utils import extract_text
from cert_generator import generate_certificate
from pydantic import BaseModel, field_validator
import uuid
import os
import re

app = FastAPI()

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


class CertificateRequest(BaseModel):
    model: str
    vin: str
    manufacturer: str

    @field_validator("vin")
    def validate_vin(cls, value):
        # VIN číslo musí byť alfanumerické a nesmie obsahovať I, O, Q
        if not re.match(r"^[A-HJ-NPR-Z0-9]{17}$", value.upper()):
            raise ValueError("VIN musí mať 17 znakov a nesmie obsahovať I, O, Q")
        return value.upper()


@app.post("/generate/")
async def generate(data: CertificateRequest):
    pdf_path = generate_certificate(data.model_dump())
    return JSONResponse({"message": "Certificate generated", "path": pdf_path})
