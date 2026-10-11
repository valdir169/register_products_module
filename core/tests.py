import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from core import storage
from core.forms.product_form import ProductForm
from core.constants import PAGE_SIZE

def data(**extra):
    base = {
        "code": "JUG-001",
        "name": "Jugo",
        "description": "Jugo de naranja",
        "price": "3.50",
        "stock": "10",
        "unit_measure": "unidad",
    }
    base.update(extra)
    return base


class TempStorageMixin:
    """Redirige storage a un JSON temporal para no tocar products.json real."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "products.json"
        path.write_text("[]", encoding="utf-8")
        patcher = patch.object(storage, "JSON_PATH", path)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.json_path = path


class StorageTests(TempStorageMixin, TestCase):
    def test_crear_asigna_id(self):
        p = storage.create_product(data(price=3.5, stock=10))
        self.assertEqual(p["id"], 1)

    def test_ids_se_incrementan(self):
        storage.create_product(data(code="AAA-001", price=1, stock=1))
        p2 = storage.create_product(data(code="AAA-002", price=1, stock=1))
        self.assertEqual(p2["id"], 2)

    def test_persiste_en_archivo(self):
        storage.create_product(data(price=3.5, stock=10))
        self.assertIn("JUG-001", self.json_path.read_text(encoding="utf-8"))
        self.assertEqual(len(storage.all_products()), 1)

    def test_actualizar(self):
        p = storage.create_product(data(price=3.5, stock=10))
        storage.update_product(p["id"], data(price=9.9, stock=5))
        self.assertEqual(storage.get_product(p["id"])["price"], 9.9)

    def test_eliminar(self):
        p = storage.create_product(data(price=3.5, stock=10))
        self.assertTrue(storage.delete_product(p["id"]))
        self.assertEqual(storage.all_products(), [])

    def test_eliminar_inexistente(self):
        self.assertFalse(storage.delete_product(999))

    def test_json_corrupto_devuelve_lista_vacia(self):
        self.json_path.write_text("{ esto no es json", encoding="utf-8")
        self.assertEqual(storage.all_products(), [])


class FormTests(TempStorageMixin, TestCase):
    def test_valido(self):
        self.assertTrue(ProductForm(data()).is_valid())

    def test_codigo_en_minusculas_se_normaliza(self):
        form = ProductForm(data(code="jug-001"))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["code"], "JUG-001")

    def test_codigo_duplicado(self):
        storage.create_product(data(price=3.5, stock=10))
        form = ProductForm(data())
        self.assertFalse(form.is_valid())
        self.assertIn("code", form.errors)

    def test_editar_con_su_propio_codigo_no_choca(self):
        p = storage.create_product(data(price=3.5, stock=10))
        self.assertTrue(ProductForm(data(), instance_id=p["id"]).is_valid())

    def test_precio_negativo(self):
        self.assertFalse(ProductForm(data(price="-1")).is_valid())

    def test_stock_negativo(self):
        self.assertFalse(ProductForm(data(stock="-5")).is_valid())

    def test_stock_no_numerico(self):
        self.assertFalse(ProductForm(data(stock="abc")).is_valid())


class ViewTests(TempStorageMixin, TestCase):
    def test_listado_carga(self):
        self.assertEqual(self.client.get(reverse("index")).status_code, 200)

    def test_crear_valido_redirige_y_guarda(self):
        res = self.client.post(reverse("product_create"), data())
        self.assertRedirects(res, reverse("index"))
        self.assertEqual(len(storage.all_products()), 1)

    def test_crear_invalido_no_guarda(self):
        res = self.client.post(reverse("product_create"), data(price="-1"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(storage.all_products(), [])

    def test_editar(self):
        p = storage.create_product(data(price=3.5, stock=10))
        self.client.post(reverse("product_update", args=[p["id"]]), data(stock="99"))
        self.assertEqual(storage.get_product(p["id"])["stock"], 99)

    def test_editar_inexistente_da_404(self):
        res = self.client.post(reverse("product_update", args=[999]), data())
        self.assertEqual(res.status_code, 404)

    def test_eliminar(self):
        p = storage.create_product(data(price=3.5, stock=10))
        self.client.post(reverse("product_delete", args=[p["id"]]))
        self.assertEqual(storage.all_products(), [])

    def test_busqueda_por_codigo(self):
        storage.create_product(data(code="AAA-001", price=1, stock=1))
        storage.create_product(data(code="BBB-001", price=1, stock=1))
        res = self.client.get(reverse("index"), {"q": "bbb"})
        self.assertEqual(len(res.context["products"]), 1)

    def test_busqueda_sin_resultados(self):
        storage.create_product(data(price=1, stock=1))
        res = self.client.get(reverse("index"), {"q": "zzzz"})
        self.assertEqual(len(res.context["products"]), 0)

    def test_paginacion(self):
        total = PAGE_SIZE + 15
        for i in range(total):
            storage.create_product(data(code=f"PRD-{i:03d}", price=1, stock=1))

        page1 = self.client.get(reverse("index"))
        page2 = self.client.get(reverse("index"), {"page": 2})

        self.assertEqual(len(page1.context["products"]), PAGE_SIZE)
        self.assertEqual(len(page2.context["products"]), 20)