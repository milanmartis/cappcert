import re
from pydantic import BaseModel, field_validator

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
