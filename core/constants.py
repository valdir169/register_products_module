import re
from pathlib import Path
from django.conf import settings

CODE = re.compile(r"[A-Z0-9-]{3,10}")

UNITS = [
    ("unidad", "Unidad"), ("kg", "Kilogramo"), ("g", "Gramo"),
    ("l", "Litro"), ("ml", "Mililitro"), ("caja", "Caja"), ("paquete", "Paquete"),
]

INPUT = "w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500"


PAGE_SIZE = 15

JSON_PATH = Path(settings.BASE_DIR) / "products.json"