
from jinja2 import Template
from reportlab.pdfgen import canvas
import os
import uuid

def generate_certificate(data):
    template_str = "Certifikát zhody pre vozidlo {{ model }}\nVIN: {{ vin }}\nVýrobca: {{ manufacturer }}"
    template = Template(template_str)
    rendered = template.render(data)

    output_dir = "static/generated"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"certificate_{uuid.uuid4()}.pdf")

    c = canvas.Canvas(output_path)
    for idx, line in enumerate(rendered.split("\n")):
        c.drawString(100, 750 - (idx * 20), line)
    c.save()

    return output_path
