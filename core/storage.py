import json
import threading
from decimal import Decimal

from .constants import JSON_PATH

_lock = threading.Lock()


def _read():
    if not JSON_PATH.exists():
        return []
    try:
        with open(JSON_PATH, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def _write(items):
    tmp = JSON_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    tmp.replace(JSON_PATH)


def _clean(data):
    return {
        "code": data["code"],
        "description": data.get("description", ""),
        "price": float(data["price"]) if isinstance(data["price"], Decimal) else data["price"],
        "stock": data["stock"],
        "unit_measure": data["unit_measure"],
    }

def all_products():
    return _read()


def get_product(pk):
    return next((p for p in _read() if p["id"] == pk), None)


def create_product(data):
    with _lock:
        items = _read()
        new_id = max((p["id"] for p in items), default=0) + 1
        product = {"id": new_id, **_clean(data)}
        items.append(product)
        _write(items)
        return product


def update_product(pk, data):
    with _lock:
        items = _read()
        for i, p in enumerate(items):
            if p["id"] == pk:
                items[i] = {"id": pk, **_clean(data)}
                _write(items)
                return items[i]
    return None


def delete_product(pk):
    with _lock:
        items = _read()
        new_items = [p for p in items if p["id"] != pk]
        if len(new_items) == len(items):
            return False
        _write(new_items)
        return True