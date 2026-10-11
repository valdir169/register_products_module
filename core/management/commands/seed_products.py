import random
import re
import shutil
import string

from django.core.management.base import BaseCommand, CommandError

from core import storage
from core.constants import CODE as CODE_RE
CATEGORIAS = {
    "JUG": (["Jugo de naranja", "Jugo de piña", "Jugo de papaya", "Jugo de maracuyá", "Jugo de arándano"], "l"),
    "FRU": (["Manzana", "Plátano", "Uva", "Mandarina", "Palta", "Fresa"], "kg"),
    "VER": (["Tomate", "Cebolla", "Zanahoria", "Papa", "Lechuga", "Pimiento"], "kg"),
    "LAC": (["Leche entera", "Yogurt natural", "Queso fresco", "Mantequilla", "Leche light"], "unidad"),
    "ABA": (["Arroz", "Fideos", "Azúcar", "Aceite vegetal", "Harina", "Lentejas"], "paquete"),
    "BEB": (["Agua mineral", "Gaseosa cola", "Té helado", "Energizante", "Néctar de durazno"], "unidad"),
    "LIM": (["Detergente", "Lejía", "Limpiador multiusos", "Suavizante", "Jabón de ropa"], "unidad"),
    "CAR": (["Pollo entero", "Carne molida", "Chuleta de cerdo", "Filete de res", "Jamón"], "kg"),
    "PAN": (["Pan francés", "Pan de molde", "Croissant", "Bizcocho", "Galletas de soda"], "paquete"),
    "SNA": (["Papas fritas", "Maní salado", "Chifles", "Barra de cereal", "Chocolate"], "unidad"),
    "CON": (["Nuggets de pollo", "Papas prefritas", "Helado de vainilla", "Pizza congelada", "Vegetales mixtos"], "caja"),
    "HIG": (["Shampoo", "Jabón de tocador", "Pasta dental", "Desodorante", "Papel higiénico"], "unidad"),
}
PRESENTACIONES = ["250 g", "500 g", "1 kg", "330 ml", "500 ml", "1 L", "2 L", "pack x6", "pack x12"]
MARCAS = ["Bell's", "Selecta", "Frescampo", "Don Victorio", "Casa Grande", "Natura", "Premium", "Económico"]

ALNUM = string.ascii_uppercase + string.digits


def make_code(rng, prefijo, seq):
    """Mezcla de estilos; todos de 3 a 10 caracteres."""
    estilo = rng.choice(["prefix", "prefix", "compact", "sku", "alnum", "short"])
    if estilo == "prefix":          # JUG-001
        return f"{prefijo}-{seq:03d}"
    if estilo == "compact":         # JUG4821
        return f"{prefijo}{rng.randint(1000, 9999)}"
    if estilo == "sku":             # 20481735
        return str(rng.randint(20_000_000, 29_999_999))
    if estilo == "alnum":           # A7K-92X
        return "".join(rng.choices(ALNUM, k=3)) + "-" + "".join(rng.choices(ALNUM, k=3))
    return f"{prefijo[:2]}{rng.randint(1, 99)}"   # JU7 (corto)


class Command(BaseCommand):
    help = "Genera productos de prueba en products.json (por defecto 1200)."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=1200)
        parser.add_argument("--append", action="store_true", help="Agrega a los existentes")

    def handle(self, *args, **opts):
        count = opts["count"]
        if not 1 <= count <= 5000:
            raise CommandError("--count debe estar entre 1 y 5000.")

        rng = random.Random(42)
        prefijos = list(CATEGORIAS)

        if storage.JSON_PATH.exists() and storage.JSON_PATH.stat().st_size > 2:
            backup = storage.JSON_PATH.with_name("products.backup.json")
            shutil.copy(storage.JSON_PATH, backup)
            self.stdout.write(f"Copia de seguridad: {backup.name}")

        items = storage.all_products() if opts["append"] else []
        codes = {p.get("code", "").upper() for p in items}
        next_id = max((p["id"] for p in items), default=0) + 1
        secuencia = {pre: 0 for pre in prefijos}

        creados, intentos = 0, 0
        while creados < count:
            intentos += 1
            if intentos > count * 50:
                raise CommandError("No se pudieron generar códigos únicos suficientes.")

            pre = prefijos[creados % len(prefijos)]
            secuencia[pre] += 1
            code = make_code(rng, pre, secuencia[pre])

            if code in codes or not CODE_RE.fullmatch(code):
                continue

            nombres, unidad = CATEGORIAS[pre]
            nombre = rng.choice(nombres)
            items.append({
                "id": next_id,
                "code": code,
                "description": f"{nombre} {rng.choice(MARCAS)} {rng.choice(PRESENTACIONES)}",
                "price": round(rng.uniform(1.5, 85), 2),
                "stock": rng.randint(0, 250),
                "unit_measure": unidad,
            })
            codes.add(code)
            next_id += 1
            creados += 1

        storage._write(items)
        self.stdout.write(self.style.SUCCESS(f"{creados} productos generados. Total en archivo: {len(items)}."))