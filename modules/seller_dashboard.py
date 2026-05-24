import tkinter as tk
from tkinter import messagebox
from modules.constants import *


class SellerDashboard(tk.Frame):

    def __init__(self, root_window, seller_name: str, data_manager, on_logout_callback):
        super().__init__(root_window, bg=BG_DARK)
        self.seller_name  = seller_name
        self.data_manager = data_manager
        self.on_logout    = on_logout_callback
        self._entry_refs  = {}   # {product_name: (price_var, stock_var)}
        self._build_layout()
        self.populate_inventory_editor()

    # ── Layout skeleton ───────────────────────────────────────────
    def _build_layout(self):
        # ── Fixed header (never scrolls) ──────────────────────────
        header = tk.Frame(self, bg=BG_HEADER, padx=16, pady=14,
                          relief="flat", bd=0,
                          highlightbackground=BORDER, highlightthickness=1)
        header.pack(fill="x")

        left = tk.Frame(header, bg=BG_HEADER)
        left.pack(side="left", fill="y")
        tk.Label(left, text="🌿 SourceDirect",
                 font=(FONT_FAMILY, 13, "bold"), bg=BG_HEADER, fg=PRIMARY).pack(anchor="w")
        tk.Label(left, text=f"Seller Console  ·  {self.seller_name}",
                 font=FONT_XS, bg=BG_HEADER, fg=ACCENT).pack(anchor="w")

        tk.Button(
            header, text="Log Out  ↩",
            font=(FONT_FAMILY, 9, "bold"),
            bg=DANGER, fg="#FFFFFF",
            activebackground="#AA0022", activeforeground="#FFFFFF",
            relief="flat", bd=0, padx=12, pady=6, cursor="hand2",
            command=self._confirm_logout,
        ).pack(side="right")

        # ── Fixed save button at bottom (never scrolls) ───────────
        tk.Button(
            self, text="Save All Changes",
            font=(FONT_FAMILY, 11, "bold"),
            bg=PRIMARY, fg="#FFFFFF",
            activebackground=PRIMARY_DARK, activeforeground="#FFFFFF",
            relief="flat", bd=0, pady=14, cursor="hand2",
            command=self.save_inventory_changes,
        ).pack(side="bottom", fill="x")

        # ── Single scrollable area fills everything in between ────
        wrap = tk.Frame(self, bg=BG_DARK)
        wrap.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(wrap, bg=BG_DARK, highlightthickness=0)
        sb = tk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # editor_frame is the single inner frame for ALL scrollable content
        self.editor_frame = tk.Frame(self.canvas, bg=BG_DARK)
        self.editor_window = self.canvas.create_window(
            (0, 0), window=self.editor_frame, anchor="nw"
        )

        self.editor_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.editor_window, width=e.width)
        )
        self.canvas.bind(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * e.delta / 120), "units")
        )

    # ── Scrollable content sections ───────────────────────────────
    def _build_stats_strip(self, parent):
        products    = self.data_manager.get_seller_products(self._resolve_seller_name())
        total_items = len(products)
        total_stock = sum(p["stock"] for p in products.values())
        low_stock   = sum(1 for p in products.values() if p["stock"] <= 50)

        stats = tk.Frame(parent, bg=BG_CARD, padx=16, pady=12,
                         highlightbackground=BORDER, highlightthickness=1)
        stats.pack(fill="x", pady=(0, 2))

        for label, val, color in [
            (" Products",   str(total_items),        TEXT_WHITE),
            ("Total Stock", f"{total_stock:,} units", INFO),
            ("Low Stock",  str(low_stock),           DANGER if low_stock else SUCCESS),
        ]:
            col = tk.Frame(stats, bg=BG_CARD)
            col.pack(side="left", expand=True)
            tk.Label(col, text=val,   font=(FONT_FAMILY, 18, "bold"), bg=BG_CARD, fg=color).pack()
            tk.Label(col, text=label, font=FONT_XS,                   bg=BG_CARD, fg=TEXT_GRAY).pack()

    def _build_welcome_section(self, parent):
        """Welcome banner, business overview, and ongoing orders — all inside parent."""
        import random

        # Welcome banner
        welcome = tk.Frame(parent, bg=PRIMARY, padx=16, pady=14)
        welcome.pack(fill="x")
        short = self.seller_name.split()[0] if self.seller_name else "Seller"
        tk.Label(welcome, text=f"Welcome back, {short}! 👋",
                 font=(FONT_FAMILY, 15, "bold"), bg=PRIMARY, fg="#FFFFFF").pack(anchor="w")
        tk.Label(welcome, text="Here's what's happening with your store today.",
                 font=FONT_XS, bg=PRIMARY, fg="#CCFFDD").pack(anchor="w", pady=(2, 0))

        # Business overview this month
        overview_wrap = tk.Frame(parent, bg=BG_DARK, padx=12, pady=8)
        overview_wrap.pack(fill="x")
        tk.Label(overview_wrap, text="Business Overview (This Month)",
                 font=FONT_LG_BOLD, bg=BG_DARK, fg=TEXT_WHITE).pack(anchor="w", pady=(0, 6))

        overview_card = tk.Frame(overview_wrap, bg=BG_CARD,
                                 highlightbackground=BORDER, highlightthickness=1)
        overview_card.pack(fill="x")

        products    = self.data_manager.get_seller_products(self._resolve_seller_name())
        total_stock = sum(p["stock"] for p in products.values())
        revenue_mock = sum(p["price"] * random.randint(4, 18) for p in products.values())
        orders_mock  = random.randint(12, 60)
        buyers_mock  = random.randint(8, 40)

        for icon, label, val, color in [
            ("💰", "Revenue", f"N{revenue_mock:,.0f}", SUCCESS),
            ("📦", "Orders",  str(orders_mock),         INFO),
            ("👥", "Buyers",  str(buyers_mock),          ACCENT),
            ("📊", "Stock",   f"{total_stock:,}",        TEXT_WHITE),
        ]:
            col = tk.Frame(overview_card, bg=BG_CARD, padx=10, pady=12)
            col.pack(side="left", expand=True)
            tk.Label(col, text=icon, font=(FONT_FAMILY, 16), bg=BG_CARD).pack()
            tk.Label(col, text=val,  font=(FONT_FAMILY, 14, "bold"), bg=BG_CARD, fg=color).pack()
            tk.Label(col, text=label, font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack()

        # Ongoing orders section
        orders_wrap = tk.Frame(parent, bg=BG_DARK)
        orders_wrap.pack(fill="x", padx=12, pady=(0, 4))
        tk.Label(orders_wrap, text="Ongoing Orders",
                 font=FONT_LG_BOLD, bg=BG_DARK, fg=TEXT_WHITE).pack(anchor="w", pady=(4, 6))

        real_orders = self.data_manager.get_seller_orders(self._resolve_seller_name())

        if not real_orders:
            tk.Label(orders_wrap,
                     text="No orders yet. Orders placed by buyers will appear here.",
                     font=FONT_XS, bg=BG_DARK, fg=TEXT_MUTED, pady=8).pack(anchor="w")
        else:
            STATUS_COLORS = {
                "Pending":    ACCENT,
                "Processing": WARNING,
                "Confirmed":  SUCCESS,
                "Cancelled":  DANGER,
            }
            for odata in real_orders:
                oid    = odata["order_id"]
                buyer  = odata["buyer"]
                status = odata["status"]
                color  = STATUS_COLORS.get(status, TEXT_GRAY)
                lines  = odata.get("items", [])
                # Summarise items: "Catfish × 10, Sardine × 5"
                item_summary = ", ".join(
                    f"{l['product']} × {l['qty']}" for l in lines
                )
                if len(item_summary) > 38:
                    item_summary = item_summary[:36] + "…"

                row = tk.Frame(orders_wrap, bg=BG_CARD, padx=12, pady=10,
                               highlightbackground=BORDER, highlightthickness=1)
                row.pack(fill="x", pady=(0, 3))

                lft = tk.Frame(row, bg=BG_CARD)
                lft.pack(side="left", fill="both", expand=True)
                tk.Label(lft, text=f"{oid}  ·  {buyer}",
                         font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
                tk.Label(lft, text=item_summary,
                         font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")
                tk.Label(row, text=status, font=(FONT_FAMILY, 8, "bold"),
                         bg=BG_CARD, fg=color).pack(side="right")

    # ── Inventory editor (also inside editor_frame) ───────────────
    def populate_inventory_editor(self):
        for widget in self.editor_frame.winfo_children():
            widget.destroy()
        self._entry_refs.clear()

        # Rebuild ALL scrollable sections in order
        self._build_stats_strip(self.editor_frame)
        self._build_welcome_section(self.editor_frame)
        self._build_inventory_rows(self.editor_frame)

    def _build_inventory_rows(self, parent):
        seller_key = self._resolve_seller_name()
        products   = self.data_manager.get_seller_products(seller_key)

        hdr = tk.Frame(parent, bg=BG_DARK, padx=16, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Inventory",
                 font=FONT_LG_BOLD, bg=BG_DARK, fg=TEXT_WHITE).pack(side="left")
        tk.Label(hdr, text="Edit prices & stock · then Save",
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_GRAY).pack(side="right")

        col_bar = tk.Frame(parent, bg=BG_CARD_ALT, padx=16, pady=6)
        col_bar.pack(fill="x")
        for txt in ["Product", "Price (N)", "Stock", "Unit"]:
            tk.Label(col_bar, text=txt, font=(FONT_FAMILY, 8, "bold"),
                     bg=BG_CARD_ALT, fg=TEXT_GRAY, anchor="w").pack(side="left", padx=(0, 24))

        for idx, (pname, pdata) in enumerate(products.items()):
            row_bg = BG_CARD if idx % 2 == 0 else BG_CARD_ALT
            row = tk.Frame(parent, bg=row_bg, padx=16, pady=8,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x")

            tk.Label(row, text=pname, font=FONT_SM_BOLD,
                     bg=row_bg, fg=TEXT_WHITE, width=20, anchor="w").pack(side="left")

            price_var = tk.StringVar(value=str(int(pdata["price"])))
            tk.Entry(row, textvariable=price_var, font=FONT_BASE,
                     bg=BG_INPUT, fg=TEXT_WHITE, insertbackground=PRIMARY,
                     relief="flat", bd=1, highlightbackground=BORDER,
                     highlightthickness=1, width=10
                     ).pack(side="left", padx=(0, 14), ipady=4)

            stock_var = tk.StringVar(value=str(pdata["stock"]))
            tk.Entry(row, textvariable=stock_var, font=FONT_BASE,
                     bg=BG_INPUT, fg=TEXT_WHITE, insertbackground=PRIMARY,
                     relief="flat", bd=1, highlightbackground=BORDER,
                     highlightthickness=1, width=8
                     ).pack(side="left", padx=(0, 14), ipady=4)

            tk.Label(row, text=pdata.get("unit", "—"),
                     font=FONT_XS, bg=row_bg, fg=TEXT_MUTED).pack(side="left")

            if pdata["stock"] <= 50:
                tk.Label(row, text="⚠ Low", font=(FONT_FAMILY, 8, "bold"),
                         bg=row_bg, fg=DANGER).pack(side="right")

            self._entry_refs[pname] = (price_var, stock_var)

    # ── Save ──────────────────────────────────────────────────────
    def save_inventory_changes(self):
        seller_key = self._resolve_seller_name()
        errors = []
        saved  = 0

        for pname, (price_var, stock_var) in self._entry_refs.items():
            raw_price = price_var.get().strip()
            raw_stock = stock_var.get().strip()
            try:
                new_price = float(raw_price)
                new_stock = int(raw_stock)
                success = self.data_manager.update_seller_product(
                    seller_key, pname, new_price, new_stock
                )
                if success:
                    saved += 1
                else:
                    errors.append(f"'{pname}' — save failed.")
            except ValueError:
                errors.append(
                    f"'{pname}' — invalid value: price='{raw_price}', stock='{raw_stock}'"
                )

        if errors:
            messagebox.showwarning(
                "Save Warnings",
                f"{saved} product(s) saved.\n\nIssues:\n" + "\n".join(errors),
            )
        else:
            messagebox.showinfo(
                "Saved Successfully ✅",
                f"All {saved} products updated!\nBuyer dashboard will reflect changes immediately.",
            )
        self.populate_inventory_editor()

    # ── Helpers ───────────────────────────────────────────────────
    def _resolve_seller_name(self) -> str:
        all_data = self.data_manager.get_all_sellers()
        sellers  = all_data.get("sellers", {})

        # 1. Exact match
        if self.seller_name in sellers:
            return self.seller_name

        lower = self.seller_name.lower()

        # 2. Data key starts with the full display name (e.g. "Mama Fish" -> "Mama Fish Mile 12")
        for key in sellers:
            if key.lower().startswith(lower):
                return key

        # 3. Display name starts with the full data key (unlikely but safe)
        for key in sellers:
            if lower.startswith(key.lower()):
                return key

        # 4. All words of display name appear in data key
        words = lower.split()
        for key in sellers:
            key_lower = key.lower()
            if all(w in key_lower for w in words):
                return key

        # 5. First word match (last resort — least specific)
        first = lower.split()[0]
        for key in sellers:
            if key.lower().startswith(first):
                return key

        return self.seller_name

    def _confirm_logout(self):
        if messagebox.askyesno("Logout", f"Log out of your seller account?\n({self.seller_name})"):
            self.on_logout()
