import re

from django import forms
from core import storage
from core.constants import UNITS, INPUT, CODE

class ProductForm(forms.Form):
    code = forms.CharField(
        label="Código (Categoría-Número)",
        min_length=3,
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": INPUT, 
            "placeholder": "COD-00001",
            "pattern": "[A-Za-z0-9-]{3,10}",
            "title": "Letras, números y guiones (3 a 10 caracteres)"
            }),
    )
    description = forms.CharField(
        label="Descripción del producto",
        required=False,
        widget=forms.Textarea(attrs={"class": "resize-none " + INPUT, "rows": 2}),
    )
    price = forms.DecimalField(
        label="Precio", min_value=0, max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={"class": INPUT, "step": "0.01"}),
    )
    stock = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={"class": INPUT}),
    )
    unit_measure = forms.ChoiceField(
        label="Unidad de medida",
        choices=UNITS,
        widget=forms.Select(attrs={"class": INPUT}),
    )

    def __init__(self, *args, instance_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_id = instance_id

    def clean_code(self):
        code = self.cleaned_data["code"].strip().upper()
        if not CODE.fullmatch(code):
            raise forms.ValidationError("Solo letras, números y guiones (3 a 10 caracteres).")
        for p in storage.all_products():
            if p.get("code", "").upper() == code and p["id"] != self.instance_id:
                raise forms.ValidationError("Ya existe un producto con este código.")
        return code