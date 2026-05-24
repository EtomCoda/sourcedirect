import json
import os
import copy
from datetime import datetime


class DataManager:
    DATA_FILE = "market_data.json"

    INITIAL_DATA = {
        "meta": {
            "market_name": "Mile 12 Market",
            "location": "Mile 12, Lagos, Nigeria",
            "last_updated": "",
            "total_sellers": 7,
        },
        "sellers": {
            "Mama Rashidat Stores": {
                "id": 1, "rating": 4.9, "order_count": 276,
                "phone": "+234 803 111 2233",
                "location": "Block A, Mile 12 Market",
                "response_time": "Online Now", "category": "Veggies",
                "products": {
                    "Ugu Leaves":   {"price": 3000,   "stock": 450,  "unit": "bundle"},
                    "Waterleaf":    {"price": 3000,   "stock": 310,  "unit": "bundle"},
                    "Ewedu":        {"price": 2800,   "stock": 90,   "unit": "bundle"},
                    "Bitter Leaf":  {"price": 4000,   "stock": 510,  "unit": "bundle"},
                    "Tomatoes":     {"price": 2500,   "stock": 190,  "unit": "bundle"},
                },
            },
            "Alhaji Musa Fish Depot": {
                "id": 2, "rating": 4.8, "order_count": 340,
                "phone": "+234 805 222 3344",
                "location": "Block C, Mile 12 Market",
                "response_time": "Online 12m ago", "category": "Fish",
                "products": {
                    "Catfish":      {"price": 3000, "stock": 200,   "unit": "kg"},
                    "Sardine":      {"price": 2800, "stock": 200,   "unit": "kg"},
                    "Mackarel":     {"price": 3500, "stock": 470,   "unit": "kg"},
                    "Tilapia":      {"price": 2500, "stock": 320,   "unit": "kg"},
                },
            },
            "Mama Fish Mile 12": {
                "id": 3, "rating": 4.9, "order_count": 223,
                "phone": "+234 807 333 4455",
                "location": "Fish Row, Mile 12 Market",
                "response_time": "Online Now", "category": "Fish",
                "products": {
                    "Croaker":      {"price": 3200,  "stock": 300, "unit": "kg"},
                },
            },
            "Alhaja Spices": {
                "id": 4, "rating": 4.8, "order_count": 221,
                "phone": "+234 809 444 5566",
                "location": "Spice Alley, Mile 12 Market",
                "response_time": "Online 38m ago", "category": "Spices",
                "products": {
                    "Uziza Leaves":     {"price": 1500,   "stock": 40,  "unit": "bundle"},
                    "Scent Leaf":       {"price": 1200,   "stock": 90,  "unit": "bundle"},
                    "Ginger":           {"price": 2000,   "stock": 500, "unit": "bundle"},
                    "Turmeric":         {"price": 2500,   "stock": 500, "unit": "bundle"},
                    "Garlic":           {"price": 3000,   "stock": 500, "unit": "bundle"},
                },
            },
            "The Tuber House": {
                "id": 5, "rating": 4.9, "order_count": 201,
                "phone": "+234 811 555 6677",
                "location": "Block F, Mile 12 Market",
                "response_time": "Online 1h ago", "category": "Tubers",
                "products": {
                    "Cassava":          {"price": 1000, "stock": 500, "unit": "kg"},
                    "Cocoyam":          {"price": 1200, "stock": 300, "unit": "kg"},
                    "Irish Potato":     {"price": 3600, "stock": 75,  "unit": "kg"},
                },
            },
            "Yam Empire": {
                "id": 6, "rating": 4.7, "order_count": 335,
                "phone": "+234 815 777 8899",
                "location": "Block G, Mile 12 Market",
                "response_time": "Online Now", "category": "Tubers",
                "products": {
                    "White Yam":        {"price": 3500, "stock": 150, "unit": "kg"},
                    "Sweet Potato":     {"price": 2800, "stock": 110, "unit": "kg"},
                },
            },
            "Alhaji Yakubu Meat": {
                "id": 7, "rating": 4.6, "order_count": 634,
                "phone": "+234 817 888 9900",
                "location": "Meat Section, Mile 12 Market",
                "response_time": "Online Now", "category": "Meat",
                "products": {
                    "Beef":         {"price": 4500, "stock": 200, "unit": "kg"},
                    "Shaki":        {"price": 2500, "stock": 150, "unit": "kg"},
                    "Ponmo":        {"price": 2500, "stock": 300, "unit": "kg"},
                    "Cow Leg":      {"price": 4000, "stock": 300, "unit": "kg"},
                    "Goat Meat":    {"price": 5000, "stock": 300, "unit": "kg"},
                },
            },
        },
    }

    def __init__(self):
        seed = copy.deepcopy(self.INITIAL_DATA)
        seed["meta"]["last_updated"] = datetime.now().isoformat()
        seed["_orders"] = {}   # always starts empty — resets on every app close
        seed["_users"]  = {}   # likewise for registered users
        self._data = seed
        # Registered change callbacks for live buyer refresh
        self._change_callbacks = []
        print("[DataManager] In-memory data initialized (resets on close).")

    def on_change(self, callback):
        if callback not in self._change_callbacks:
            self._change_callbacks.append(callback)

    def _notify_change(self):
        for cb in self._change_callbacks:
            try:
                cb()
            except Exception:
                pass

    def get_all_sellers(self) -> dict:
        return copy.deepcopy(self._data)

    def update_seller_product(self, seller_name: str, product_name: str,
                              new_price: float, new_stock: int = None) -> bool:
        sellers = self._data.get("sellers", {})
        if seller_name not in sellers:
            print(f"[DataManager] ERROR — Seller '{seller_name}' not found.")
            return False
        if product_name not in sellers[seller_name]["products"]:
            print(f"[DataManager] ERROR — Product '{product_name}' not found.")
            return False

        sellers[seller_name]["products"][product_name]["price"] = float(new_price)
        if new_stock is not None:
            sellers[seller_name]["products"][product_name]["stock"] = int(new_stock)
        self._data["meta"]["last_updated"] = datetime.now().isoformat()
        print(f"[DataManager] Updated: '{product_name}' @ '{seller_name}' -> N{new_price:,.0f}"
              + (f", stock={new_stock}" if new_stock is not None else ""))
        self._notify_change()
        return True

    def get_seller_products(self, seller_name: str) -> dict:
        return copy.deepcopy(
            self._data["sellers"].get(seller_name, {}).get("products", {})
        )

    def get_seller_names(self) -> list:
        return list(self._data["sellers"].keys())

    def place_order(self, buyer_name: str, cart_items: dict) -> list:
        """
        Record a new order for each seller involved in the cart.
        cart_items: {product_name: {vendor, unit_price, unit, qty, seller_data}}
        Returns list of order IDs created.
        """
        by_seller: dict = {}
        for pname, pdata in cart_items.items():
            seller = pdata.get("vendor", "Unknown")
            by_seller.setdefault(seller, []).append({
                "product":    pname,
                "qty":        pdata["qty"],
                "unit_price": pdata["unit_price"],
                "unit":       pdata["unit"],
            })

        order_ids = []
        existing  = self._data["_orders"]
        next_num  = 5000 + len(existing)

        for seller, lines in by_seller.items():
            oid = f"#SD-{next_num}"
            next_num += 1
            existing[oid] = {
                "seller":    seller,
                "buyer":     buyer_name,
                "items":     lines,
                "status":    "Pending",
                "timestamp": datetime.now().isoformat(),
            }
            order_ids.append(oid)
            print(f"[DataManager] Order {oid} placed by '{buyer_name}' → '{seller}'")

        self._notify_change()
        return order_ids

    def get_seller_orders(self, seller_name: str) -> list:
        """
        Return all orders destined for this seller, newest first.
        Each entry: {order_id, buyer, items, status, timestamp}
        """
        result = []
        for oid, odata in self._data["_orders"].items():
            if odata["seller"].lower() == seller_name.lower():
                result.append({"order_id": oid, **odata})
        result.sort(key=lambda x: x["timestamp"], reverse=True)
        return result

    def add_user(self, username: str, password: str, business_name: str) -> bool:
        if "_users" not in self._data:
            self._data["_users"] = {}
        if username in self._data["_users"]:
            return False
        self._data["_users"][username] = {
            "password": password,
            "business_name": business_name,
            "role": "Buyer",
        }
        print(f"[DataManager] New buyer registered: '{username}'")
        return True

    def validate_user(self, username: str, password: str) -> str | None:
        users = self._data.get("_users", {})
        if username in users and users[username]["password"] == password:
            return users[username]["role"]
        return None