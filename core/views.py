import unicodedata
from urllib.parse import urlencode
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from . import storage
from .forms.product_form import ProductForm
from .constants import PAGE_SIZE


def _normalize(text):
    text = unicodedata.normalize("NFD", str(text).lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")

def _search(products, q):
    q = _normalize(q.strip())
    if not q:
        return products
    return [
        p for p in products
        if q in _normalize(p.get("code", ""))
        or q in _normalize(p.get("description", ""))
    ]
    

def _index_context(request, form=None, editing_id=None):
    q=request.GET.get("q", "").strip()
    products = sorted(storage.all_products(), key=lambda p: p.get("code", "").upper())
    products = _search(products, q)

    paginator = Paginator(products, PAGE_SIZE)
    page_number = paginator.get_page(request.GET.get("page", 1))
    return {
        "products": page_number.object_list,
        "page_obj": page_number,
        "page_range": list(paginator.get_elided_page_range(page_number.number, on_each_side=1, on_ends=1)),
        "q": q,
        "q_param": urlencode({"q": q}) if q else "",
        "form": form if form is not None else ProductForm(),
        "editing_id": editing_id,
    }


def index(request):
    return render(request, "core/index.html", _index_context(request))

def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            storage.create_product(form.cleaned_data)
            messages.success(request, "Producto creado.")
            return redirect("index")
        return render(request, "core/index.html", _index_context(request,form))
    return redirect("index")

def product_update(request, pk):
    if not storage.get_product(pk):
        raise Http404("Producto no encontrado")
    if request.method == "POST":
        form = ProductForm(request.POST, instance_id=pk)
        if form.is_valid():
            storage.update_product(pk, form.cleaned_data)
            messages.success(request, "Producto actualizado.")
            return redirect("index")
        return render(request, "core/index.html", _index_context(request,form, editing_id=pk))
    return redirect("index")


def product_delete(request, pk):
    if not storage.get_product(pk):
        raise Http404("Producto no encontrado")
    if request.method == "POST":
        storage.delete_product(pk)
        messages.success(request, "Producto eliminado.")
    return redirect("index")