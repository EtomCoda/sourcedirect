import tkinter as tk
from tkinter import messagebox
from modules.constants import *
from modules.catalog_components import CatalogComponents
from modules.list_row_components import ListRowComponents
from modules.catalog_components import BEST_SELLER_PRODUCTS, CatalogComponents


class BuyerDashboard(tk.Frame):
    def __init__(self, root_window, data_manager, on_view_stock_callback,
                 business_name: str = "", username: str = ""):
        super().__init__(root_window, bg=BG_DARK)
        self.data_manager = data_manager
        self.on_view_stock = on_view_stock_callback
        self.business_name = business_name or username.title() or "Buyer"
        self.username = username
        self._root_window = root_window
        self.active_category = tk.StringVar(value="All")
        self._cat_buttons = {}
        self._profile_menu = None
        self._build_layout()
        # Register for live data changes from seller
        self.data_manager.on_change(self._reload_scroll_content)

    def _build_layout(self):
        self._build_header()
        self._build_search_bar()
        self.render_categories_bar(self)
        self._build_scroll_canvas()

    def _build_header(self):
        header = tk.Frame(self, bg=BG_HEADER, padx=16, pady=12,
                          highlightbackground=BORDER, highlightthickness=1)
        header.pack(fill="x")

        left = tk.Frame(header, bg=BG_HEADER)
        left.pack(side="left", fill="y")
        tk.Label(left, text="🌿 SourceDirect",
                 font=(FONT_FAMILY, 13, "bold"), bg=BG_HEADER, fg=PRIMARY).pack(anchor="w")

        market_row = tk.Frame(left, bg=BG_HEADER)
        market_row.pack(anchor="w")
        tk.Label(market_row, text="📍", bg=BG_HEADER, font=(FONT_FAMILY, 8)).pack(side="left")
        self.selected_market = tk.StringVar(value="Mile 12 Market, Lagos")
        _markets = [
            "Mile 12 Market, Lagos",
            "Oyingbo Market, Lagos",
            "Bodija Market, Ibadan",
            "Wuse Market, Abuja",
        ]
        market_menu = tk.OptionMenu(market_row, self.selected_market, *_markets,
                                    command=self._on_market_change)
        market_menu.config(
            bg=BG_HEADER, fg=ACCENT, activebackground=BG_CARD_ALT,
            activeforeground=ACCENT, relief="flat", bd=0,
            font=(FONT_FAMILY, 8), cursor="hand2", padx=0, pady=0,
            highlightthickness=0,
        )
        market_menu["menu"].config(
            bg=BG_CARD, fg=TEXT_WHITE, activebackground=PRIMARY,
            activeforeground="#FFFFFF", relief="flat", bd=0,
            font=(FONT_FAMILY, 9),
        )
        market_menu.pack(side="left")

        right = tk.Frame(header, bg=BG_HEADER)
        right.pack(side="right")

        self.cart_btn = tk.Button(
            right, text="🛒 (0)", font=(FONT_FAMILY, 11, "bold"),
            bg=PRIMARY, fg="#FFFFFF", relief="flat", bd=0,
            padx=12, pady=4, cursor="hand2",
            command=self._open_cart
        )
        self.cart_btn.pack(side="left", padx=(0, 8))

        import modules.cart_manager as cart
        cart.on_change(self._update_cart_badge)
        self._update_cart_badge()

        # Profile button with dropdown
        self._profile_btn = tk.Button(
            right, text="👤", font=(FONT_FAMILY, 14),
            bg=BG_CARD, fg=TEXT_GRAY, relief="flat", bd=0,
            padx=8, pady=4, cursor="hand2",
            command=self._toggle_profile_menu,
        )
        self._profile_btn.pack(side="left")

    def _toggle_profile_menu(self):
        # Close if already open
        if self._profile_menu and self._profile_menu.winfo_exists():
            self._profile_menu.destroy()
            self._profile_menu = None
            return

        # Position dropdown below the profile button
        btn = self._profile_btn
        x = btn.winfo_rootx()
        y = btn.winfo_rooty() + btn.winfo_height()

        menu = tk.Toplevel(self)
        menu.overrideredirect(True)
        menu.geometry(f"+{x - 120}+{y + 2}")
        menu.configure(bg=BG_CARD)
        menu.attributes("-topmost", True)
        self._profile_menu = menu

        frame = tk.Frame(menu, bg=BG_CARD,
                         highlightbackground=BORDER, highlightthickness=1)
        frame.pack(fill="both", expand=True)

        # Business name header
        biz_row = tk.Frame(frame, bg=BG_CARD, padx=14, pady=10)
        biz_row.pack(fill="x")
        tk.Label(biz_row, text="👤", font=(FONT_FAMILY, 11),
                 bg=BG_CARD, fg=PRIMARY).pack(side="left", padx=(0, 8))
        name_col = tk.Frame(biz_row, bg=BG_CARD)
        name_col.pack(side="left")
        tk.Label(name_col, text=self.business_name,
                 font=(FONT_FAMILY, 10, "bold"), bg=BG_CARD,
                 fg=TEXT_WHITE, anchor="w").pack(anchor="w")
        tk.Label(name_col, text="Buyer Account",
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY, anchor="w").pack(anchor="w")

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x")

        # Logout button
        def _do_logout():
            menu.destroy()
            self._profile_menu = None
            if hasattr(self._root_window, 'show_login'):
                self._root_window.show_login()

        tk.Button(
            frame, text="🚪  Log Out", font=FONT_SM_BOLD,
            bg=BG_CARD, fg=DANGER, activebackground=BG_CARD_ALT,
            activeforeground=DANGER, relief="flat", bd=0,
            padx=14, pady=10, cursor="hand2", anchor="w",
            command=_do_logout,
        ).pack(fill="x")

        # Close menu if clicking elsewhere
        def _close_on_click(e):
            if self._profile_menu and self._profile_menu.winfo_exists():
                self._profile_menu.destroy()
                self._profile_menu = None
        menu.bind("<FocusOut>", _close_on_click)
        menu.focus_set()

    def _update_cart_badge(self):
        import modules.cart_manager as cart
        count = cart.item_count()
        self.cart_btn.config(text=f"🛒 ({count})")
        self.cart_btn.config(bg=PRIMARY if count > 0 else BG_CARD,
                             fg="#FFFFFF" if count > 0 else TEXT_WHITE)

    def _open_cart(self):
        from modules.cart_page import CartPage
        page = CartPage(self, on_checkout_success=self._reload_scroll_content,
                        data_manager=self.data_manager,
                        buyer_name=self.business_name)
        page.open()

    def _build_search_bar(self):
        wrap = tk.Frame(self, bg=BG_DARK, padx=16)
        wrap.pack(fill="x", pady=(10, 0))
        bar = tk.Frame(wrap, bg=BG_INPUT, padx=12, pady=10,
                       highlightbackground=BORDER, highlightthickness=1)
        bar.pack(fill="x")
        tk.Label(bar, text="🔍", bg=BG_INPUT, font=(FONT_FAMILY, 12)).pack(side="left")
        entry = tk.Entry(bar, font=FONT_BASE, bg=BG_INPUT, fg=TEXT_GRAY,
                         insertbackground=PRIMARY, relief="flat", bd=0)
        entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
        entry.insert(0, "Search products, sellers, bulk orders…")
        entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END) if "Search" in entry.get() else None)
        entry.bind("<Return>",  lambda e: messagebox.showinfo("Search", f"Searching for: {entry.get()}"))
        tk.Label(bar, text="⚙", bg=BG_INPUT, fg=TEXT_GRAY,
                 font=(FONT_FAMILY, 14), cursor="hand2").pack(side="right")

    def render_categories_bar(self, parent):
        wrap = tk.Frame(parent, bg=BG_DARK, pady=10)
        wrap.pack(fill="x")

        canvas = tk.Canvas(wrap, bg=BG_DARK, height=44, highlightthickness=0)
        h_scroll = tk.Scrollbar(wrap, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=h_scroll.set)
        canvas.pack(fill="x", padx=4)

        inner = tk.Frame(canvas, bg=BG_DARK)
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        self._cat_buttons.clear()
        all_cats = [("✦", "All")] + list(CATEGORIES)
        for icon, name in all_cats:
            btn = self._cat_badge(inner, icon, name)
            self._cat_buttons[name] = btn

        def _on_inner_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            if inner.winfo_reqwidth() > canvas.winfo_width():
                h_scroll.pack(fill="x", padx=4)
            else:
                h_scroll.pack_forget()

        inner.bind("<Configure>", _on_inner_configure)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, height=44))
        canvas.bind("<Shift-MouseWheel>", lambda e: canvas.xview_scroll(int(-1 * e.delta / 120), "units"))

    def _cat_badge(self, parent, icon: str, name: str):
        is_active = (name == self.active_category.get())
        bg = PRIMARY if is_active else BG_CARD
        fg = "#FFFFFF" if is_active else TEXT_GRAY
        btn = tk.Button(
            parent, text=f"{icon} {name}",
            font=(FONT_FAMILY, 9, "bold"),
            bg=bg, fg=fg, activebackground=PRIMARY_DARK, activeforeground="#FFFFFF",
            relief="flat", bd=0, padx=12, pady=6, cursor="hand2",
            command=lambda n=name: self._select_category(n),
        )
        btn.pack(side="left", padx=4)
        return btn

    def _select_category(self, name: str):
        self.active_category.set(name)
        for cat_name, btn in self._cat_buttons.items():
            if cat_name == name:
                btn.config(bg=PRIMARY, fg="#FFFFFF")
            else:
                btn.config(bg=BG_CARD, fg=TEXT_GRAY)
        self._reload_scroll_content()

    def _on_market_change(self, market: str):
        messagebox.showinfo("Market Changed",
                            f"Now showing suppliers from:\n{market}\n\nListings will update.")

    def _build_scroll_canvas(self):
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(self.canvas, bg=BG_DARK)
        self.scroll_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>",       self._on_canvas_configure)
        self.canvas.bind("<MouseWheel>",      self._on_mousewheel)

        self._reload_scroll_content()

    def _reload_scroll_content(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        data = self.data_manager.get_all_sellers()
        sellers = data.get("sellers", {})
        active_cat = self.active_category.get()

        catalog = CatalogComponents()
        list_rows = ListRowComponents()

        if active_cat != "All":
            cat_icon = next((icon for icon, name in CATEGORIES if name == active_cat), "🛒")
            self._section_label(self.scroll_frame, f"{cat_icon}  {active_cat} Products")

            pgrid = tk.Frame(self.scroll_frame, bg=BG_DARK, padx=12)
            pgrid.pack(fill="x", pady=(0, 8))
            col = 0
            for sname, sdata in sellers.items():
                if sdata.get("category", "") != active_cat:
                    continue
                for pname, pdata in sdata["products"].items():
                    catalog.render_product_card(
                        pgrid, pname, sname,
                        f"N{pdata['price']:,.0f} / {pdata['unit']}",
                        col % 2,
                        unit_price=pdata["price"],
                        unit=pdata["unit"],
                        seller_data=sdata,
                    )
                    col += 1
            if col == 0:
                tk.Label(self.scroll_frame,
                        text=f"No products found in '{active_cat}' category.",
                        font=FONT_MD, bg=BG_DARK, fg=TEXT_MUTED, pady=30).pack()
            return

        # ── BEST RATED SELLERS (TOP 3 BY RATING & ORDER_COUNT) ──────────
        self._section_label(self.scroll_frame, "Best rated sellers")
        grid = tk.Frame(self.scroll_frame, bg=BG_DARK, padx=12)
        grid.pack(fill="x", pady=(0, 8))
        
        # Sort sellers by rating (descending), then by order_count (descending)
        sorted_sellers = sorted(
            sellers.items(),
            key=lambda x: (x[1].get("rating", 0), x[1].get("order_count", 0)),
            reverse=True
        )
        # Take only top 3
        for sname, sdata in sorted_sellers[:3]:
            catalog.render_seller_card(grid, sname, sdata["rating"], sdata["order_count"],
                                    seller_data=sdata)

        # ── BEST SELLING PRODUCTS (ONLY BEST SELLER TAG, MAX 4) ──────────
        self._section_label(self.scroll_frame, "Best selling products")
        pgrid = tk.Frame(self.scroll_frame, bg=BG_DARK, padx=12)
        pgrid.pack(fill="x", pady=(0, 8))
        
        # Collect products that are in BEST_SELLER_PRODUCTS set
        best_seller_products = []
        for sname, sdata in sellers.items():
            for pname, pdata in sdata["products"].items():
                if pname.lower() in BEST_SELLER_PRODUCTS:
                    best_seller_products.append((sname, sdata, pname, pdata))
        
        # Take only first 4 (preserves order of discovery)
        col = 0
        for sname, sdata, pname, pdata in best_seller_products[:4]:
            catalog.render_product_card(
                pgrid, pname, sname,
                f"N{pdata['price']:,.0f} / {pdata['unit']}",
                col,
                unit_price=pdata["price"],
                unit=pdata["unit"],
                seller_data=sdata,
            )
            col += 1
        
        # If fewer than 4 best-seller products, fill with regular products
        if len(best_seller_products) < 4:
            for sname, sdata in sellers.items():
                for pname, pdata in sdata["products"].items():
                    if pname.lower() not in BEST_SELLER_PRODUCTS and col < 4:
                        catalog.render_product_card(
                            pgrid, pname, sname,
                            f"N{pdata['price']:,.0f} / {pdata['unit']}",
                            col,
                            unit_price=pdata["price"],
                            unit=pdata["unit"],
                            seller_data=sdata,
                        )
                        col += 1

        # ── LOW COST - SELLING FAST ──────────────────────────────────────
        self._section_label(self.scroll_frame, "Low cost - selling fast")
        for sname, sdata in sellers.items():
            for pname, pdata in sdata["products"].items():
                if pdata["stock"] <= 90:
                    list_rows.render_low_cost_row(
                        self.scroll_frame, pname, sname, pdata["stock"])

        # ── RESPONDS FAST (ONLY ONLINE NOW, MAX 3) ───────────────────────
        self._section_label(self.scroll_frame, "Responds fast")
        # Filter sellers with "Online Now" status
        online_sellers = [
            (sname, sdata)
            for sname, sdata in sellers.items()
            if sdata.get("response_time", "").lower() == "online now"
        ]
        # Take only first 3
        for sname, sdata in online_sellers[:3]:
            list_rows.render_fast_response_row(
                self.scroll_frame, sname, sdata.get("response_time", "Unknown"))

    def _section_label(self, parent, text: str):
        wrap = tk.Frame(parent, bg=BG_DARK, padx=12)
        wrap.pack(fill="x", pady=(14, 4))
        tk.Label(wrap, text=text, font=FONT_LG_BOLD, bg=BG_DARK, fg=TEXT_WHITE).pack(side="left")
        tk.Frame(wrap, bg=BORDER_LIGHT, height=1).pack(side="left", fill="x", expand=True,
                                                        padx=(10, 0), pady=6)

    def _on_frame_configure(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.scroll_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
