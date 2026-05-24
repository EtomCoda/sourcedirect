
_items: dict = {}           # {product_name: {qty, unit_price, unit, vendor, seller_data}}
_callbacks: list = []       # listeners notified on every cart change


# ── Public API ────────────────────────────────────────────────────────
def add_item(product_name: str, vendor: str, unit_price: float,
             unit: str, qty: int = 10, seller_data: dict = None):
    if product_name in _items:
        _items[product_name]["qty"] += qty
    else:
        _items[product_name] = {
            "vendor":      vendor,
            "unit_price":  float(unit_price),
            "unit":        unit,
            "qty":         int(qty),
            "seller_data": seller_data or {},
        }
    _notify()


def remove_item(product_name: str):
    _items.pop(product_name, None)
    _notify()


def update_qty(product_name: str, qty: int):
    if product_name in _items:
        _items[product_name]["qty"] = max(1, int(qty))
    _notify()


def get_items() -> dict:
    return dict(_items)


def get_total() -> float:
    return sum(v["qty"] * v["unit_price"] for v in _items.values())


def item_count() -> int:
    return len(_items)


def clear():
    _items.clear()
    _notify()


# ── Change notification ───────────────────────────────────────────────
def on_change(callback):
    if callback not in _callbacks:
        _callbacks.append(callback)


def _notify():
    for cb in _callbacks:
        try:
            cb()
        except Exception:
            pass
