
# Cappcert

Demo FastAPI aplikácia na správu a generovanie certifikátov zhody (COC).


Endpointy:
- POST `/upload/` – upload obrázka (JPG/PNG), OCR extrakcia
- POST `/generate/` – vygeneruj PDF certifikát zo zadaných údajov

Vyžaduje:
- Google Cloud Vision API kľúč (nastavený ako GOOGLE_APPLICATION_CREDENTIALS)
