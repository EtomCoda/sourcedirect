import tkinter as tk
from tkinter import messagebox
import modules.cart_manager as cart
from modules.constants import *

BEST_SELLER_PRODUCTS = {
    "ugu leaves", "ewedu", "ewedu leaves", "sardine", "mackarel", "mackerel",
    "cocoyam", "uziza leaves", "scent leaf", "turmeric", "beef", "shaki", "ponmo"
}

MOCK_REVIEWS = {
    "Mama Rashidat Stores": [
        ("Simisola Catering Services", "★★★★★", "Best Ugu in Mile 12. Always fresh, never soggy."),
        ("Tunde's Kitchen",            "★★★★",  "Good tomatoes but price is getting high."),
        ("Bisi's Food Canteen",        "★★★★★", "Very reliable ewedu supplier. Order weekly."),
    ],
    "Alhaji Musa Fish Depot": [
        ("Mama Cee Bukka",             "★★★★★", "Freshest catfish around. Our restaurant depends on them."),
        ("Golden Pot Catering",        "★★★★★", "Mackerel always arrives iced and clean. Five stars."),
        ("Iya Beji Kitchen",           "★★★★",  "Great fish quality, delivery communication could improve."),
    ],
    "Mama Fish Mile 12": [
        ("De-Royale Event Catering",   "★★★★★", "Croaker so fresh it practically swims to you."),
        ("Adunola's Cookhouse",        "★★★★★", "Ordered 50kg for a wedding — pristine condition."),
        ("Femi's Fast Food",           "★★★★",  "Excellent fish, availability limited on busy days."),
    ],
    "Alhaja Spices": [
        ("Nourish Bowl Catering",      "★★★★★", "Ginger and garlic absolutely top-notch. Can't do without Alhaja."),
        ("Zainab's Homemade",          "★★★★★", "Every spice bundle is well-packed and fragrant."),
        ("Korede's Kitchen",           "★★★★",  "Great selection. Uziza leaves run out fast — stock more!"),
    ],
    "The Tuber House": [
        ("Iya Gbogbo Ero Canteen",     "★★★★★", "Irish potatoes so firm and fresh. Our cafeteria orders weekly."),
        ("Chefstone Catering",         "★★★★★", "Cassava supply is consistent and well-priced."),
        ("Abuja Pepper Soup Joint",    "★★★★",  "Good tubers. Delivery once took longer than expected."),
    ],
    "Yam Empire": [
        ("Eko Buka Catering",          "★★★★★", "White yam that actually tastes like yam! Firm and well-sized."),
        ("Aunty Lara's Kitchen",       "★★★★★", "Sweet potatoes are consistently great. Bulk orders always accurate."),
        ("Sunrise Food Services",      "★★★★",  "Solid supplier. Minor delay once but resolved quickly."),
    ],
    "Alhaji Yakubu Meat": [
        ("Alheri Event Catering",      "★★★★★", "Best beef in Mile 12 — no excess fat, perfectly portioned."),
        ("Mr. Biggs Canteen Yaba",     "★★★★★", "Goat meat freshness is unmatched. Loyal customer here."),
        ("Mama Titi's Buka",           "★★★★",  "Great meat overall. Shaki occasionally needs extra trimming."),
    ],
}

_DEFAULT_REVIEWS = [
    ("Simisola Catering Services", "★★★★★", "Excellent seller — always reliable and very fresh."),
    ("Tunde's Kitchen",            "★★★★★", "Top quality supply every time. Highly recommended!"),
    ("Bisi's Food Canteen",        "★★★★",  "Very good overall, minor delays once in a while."),
]


class CatalogComponents:
    """Builds seller cards, product cards, and full detail/profile popups."""

    def __init__(self):
        self._current_row = None
        self._current_row_col = 0  # tracks how many cards in the current row

    # ── Seller card ───────────────────────────────────────────────────
    def render_seller_card(self, parent, seller_name: str, rating: float,
                           order_count: int, on_view_stock=None,
                           seller_data: dict = None):
        card = tk.Frame(parent, bg=BG_CARD, padx=14, pady=14, relief="flat", bd=0,
                        cursor="hand2", highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", pady=5)

        av = tk.Canvas(card, width=52, height=52, bg=BG_CARD, highlightthickness=0)
        av.pack(side="left", padx=(0, 12))
        av.create_oval(2, 2, 50, 50, fill=PRIMARY, outline=PRIMARY_DARK, width=2)
        av.create_text(26, 26, text="".join(w[0].upper() for w in seller_name.split()[:2]),
                       font=(FONT_FAMILY, 14, "bold"), fill="#FFFFFF")

        info = tk.Frame(card, bg=BG_CARD)
        info.pack(side="left", fill="both", expand=True)

        tk.Label(info, text=seller_name[:22] + ("…" if len(seller_name) > 22 else ""),
                 font=FONT_MD_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")

        rr = tk.Frame(info, bg=BG_CARD)
        rr.pack(anchor="w", pady=2)
        tk.Label(rr, text="★" * int(rating), font=(FONT_FAMILY, 9), bg=BG_CARD, fg=GOLD).pack(side="left")
        tk.Label(rr, text=f"  {rating}  ·  {order_count:,} orders",
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(side="left")

        br = tk.Frame(info, bg=BG_CARD)
        br.pack(anchor="w", pady=(6, 0))
        for txt, cmd in [
            ("📞", lambda n=seller_name: messagebox.showinfo("Call", f"Calling {n}…")),
            ("💬", lambda n=seller_name: messagebox.showinfo("Message", f"Chat with {n}…")),
        ]:
            tk.Button(br, text=txt, font=(FONT_FAMILY, 9), bg=BG_CARD_ALT, fg=TEXT_WHITE,
                      relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
                      command=cmd).pack(side="left", padx=(0, 6))

        tk.Button(br, text="View Profile  →", font=(FONT_FAMILY, 9, "bold"),
                  bg=PRIMARY, fg="#FFFFFF", activebackground=PRIMARY_DARK,
                  relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
                  command=lambda: self._open_seller_profile(seller_name, seller_data or {})
                  ).pack(side="left")

        for w in [card, info]:
            w.bind("<Enter>", lambda e, c=card: c.config(bg=BG_CARD_ALT))
            w.bind("<Leave>", lambda e, c=card: c.config(bg=BG_CARD))

    # ── Product card ──────────────────────────────────────────────────
    def render_product_card(self, parent, title: str, vendor: str,
                            price_string: str, col_index: int = 0,
                            unit_price: float = 0, unit: str = "unit",
                            seller_data: dict = None):
        # Start a new row every 2 cards
        if col_index % 2 == 0:
            self._current_row = tk.Frame(parent, bg=BG_DARK)
            self._current_row.pack(fill="x", pady=4)
            self._current_row.columnconfigure(0, weight=1, uniform="col")
            self._current_row.columnconfigure(1, weight=1, uniform="col")

        col = col_index % 2
        card = tk.Frame(self._current_row, bg=BG_CARD, relief="flat", bd=0,
                        cursor="hand2", highlightbackground=BORDER, highlightthickness=1)
        card.grid(row=0, column=col, padx=8, pady=4, sticky="nsew")

        ic = tk.Canvas(card, height=110, bg="#E0F0E8", highlightthickness=0)
        ic.pack(fill="x")
        # Draw icon and badge after canvas is sized
        def _draw(event, c=ic, t=title):
            w = c.winfo_width()
            c.delete("all")
            c.create_text(w // 2, 55, text=self._product_icon(t), font=(FONT_FAMILY, 32))
            is_best = t.lower() in BEST_SELLER_PRODUCTS
            badge_color = ACCENT if is_best else "#00A040"
            badge_text  = "⭐ Best Seller" if is_best else "✅ Verified"
            c.create_rectangle(0, 0, 82, 20, fill=badge_color, outline="")
            c.create_text(41, 10, text=badge_text, font=(FONT_FAMILY, 7, "bold"), fill="#FFFFFF")
        ic.bind("<Configure>", _draw)

        body = tk.Frame(card, bg=BG_CARD, padx=10, pady=8)
        body.pack(fill="x")
        tk.Label(body, text=(title if len(title) <= 20 else title[:18] + "…"),
                 font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(body, text=vendor, font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")
        tk.Label(body, text=price_string, font=(FONT_FAMILY, 12, "bold"),
                 bg=BG_CARD, fg=PRIMARY).pack(anchor="w", pady=(4, 6))
        tk.Button(body, text="Product Details", font=(FONT_FAMILY, 8, "bold"),
                  bg=BG_CARD_ALT, fg=TEXT_WHITE, activebackground=PRIMARY,
                  activeforeground="#FFFFFF", relief="flat", bd=0,
                  padx=8, pady=5, cursor="hand2",
                  command=lambda: self._open_product_detail(
                      title, vendor, unit_price, unit, seller_data)
                  ).pack(fill="x")

    # ── Seller Profile Popup ──────────────────────────────────────────
    def _open_seller_profile(self, seller_name: str, seller_data: dict):
        sd       = seller_data or {}
        products = sd.get("products", {})
        rating   = sd.get("rating", 4.5)
        orders   = sd.get("order_count", 0)
        location = sd.get("location", "Mile 12 Market, Lagos")
        resp     = sd.get("response_time", "Unknown")
        phone    = sd.get("phone", "N/A")
        online   = resp.lower() == "online now"

        popup = tk.Toplevel()
        popup.title(seller_name)
        popup.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        popup.resizable(False, False)
        popup.configure(bg=BG_DARK)
        popup.grab_set()

        # ── Header: "Seller's Page" + cart & account icons ───────────
        hdr = tk.Frame(popup, bg=BG_HEADER, padx=16, pady=12,
                       highlightbackground=BORDER, highlightthickness=1)
        hdr.pack(fill="x")
        tk.Button(hdr, text="←", font=(FONT_FAMILY, 16), bg=BG_HEADER, fg=TEXT_WHITE,
                  relief="flat", bd=0, cursor="hand2",
                  command=popup.destroy).pack(side="left")
        tk.Label(hdr, text="Seller's Page", font=(FONT_FAMILY, 13, "bold"),
                 bg=BG_HEADER, fg=TEXT_WHITE).pack(side="left", padx=(10, 0))

        # ── Scrollable body ───────────────────────────────────────────
        wrap = tk.Frame(popup, bg=BG_DARK)
        wrap.pack(fill="both", expand=True)
        canvas = tk.Canvas(wrap, bg=BG_DARK, highlightthickness=0)
        sb = tk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(canvas, bg=BG_DARK)
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * e.delta / 120), "units"))

        # ── Identity block ────────────────────────────────────────────
        identity = tk.Frame(inner, bg=BG_DARK, padx=16, pady=14)
        identity.pack(fill="x")

        tk.Label(identity, text=resp,
                 font=FONT_XS, bg=BG_DARK,
                 fg=SUCCESS if online else WARNING).pack(anchor="w")
        tk.Label(identity, text=seller_name,
                 font=(FONT_FAMILY, 17, "bold"), bg=BG_DARK, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(identity, text=location,
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_GRAY).pack(anchor="w")

        # Avatar + Call / Message row
        ar = tk.Frame(identity, bg=BG_DARK)
        ar.pack(fill="x", pady=(12, 0))

        av = tk.Canvas(ar, width=52, height=52, bg=BG_DARK, highlightthickness=0)
        av.pack(side="left")
        av.create_oval(2, 2, 50, 50, fill=SUCCESS, outline="")
        av.create_text(26, 26, text="".join(w[0].upper() for w in seller_name.split()[:2]),
                       font=(FONT_FAMILY, 13, "bold"), fill="#FFFFFF")

        btns = tk.Frame(ar, bg=BG_DARK)
        btns.pack(side="right")
        tk.Button(btns, text="📞 Call", font=FONT_SM_BOLD, bg=BG_CARD, fg=SUCCESS,
                  relief="flat", bd=0, padx=14, pady=8, cursor="hand2",
                  command=lambda: messagebox.showinfo("Call", f"Calling {seller_name}…\n{phone}")
                  ).pack(side="left", padx=(0, 8))
        tk.Button(btns, text="💬 Message", font=FONT_SM_BOLD, bg=SUCCESS, fg="#FFFFFF",
                  activebackground=PRIMARY_DARK, activeforeground="#FFFFFF",
                  relief="flat", bd=0, padx=14, pady=8, cursor="hand2",
                  command=lambda: messagebox.showinfo("Message", f"Chat with {seller_name}…")
                  ).pack(side="left")

        # ── Stats bar: rating | bulk orders | products ────────────────
        tk.Frame(inner, bg=SUCCESS, height=2).pack(fill="x")
        srow = tk.Frame(inner, bg=BG_CARD, padx=16, pady=12)
        srow.pack(fill="x")

        def _stat(parent, value, label):
            col = tk.Frame(parent, bg=BG_CARD)
            col.pack(side="left", expand=True)
            vrow = tk.Frame(col, bg=BG_CARD)
            vrow.pack()
            if label == "rating":
                tk.Label(vrow, text="⭐", font=(FONT_FAMILY, 11),
                         bg=BG_CARD).pack(side="left")
            tk.Label(vrow, text=str(value),
                     font=(FONT_FAMILY, 15, "bold"), bg=BG_CARD, fg="#000000").pack(side="left")
            tk.Label(col, text=label, font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack()

        _stat(srow, f"{rating}/5", "rating")
        tk.Frame(srow, bg=BORDER_LIGHT, width=1).pack(side="left", fill="y", pady=4)
        _stat(srow, f"{orders:,}", "bulk orders")
        tk.Frame(srow, bg=BORDER_LIGHT, width=1).pack(side="left", fill="y", pady=4)
        _stat(srow, len(products), "products")

        # ── Stock / Reviews tab bar ───────────────────────────────────
        tk.Frame(inner, bg=BORDER_LIGHT, height=1).pack(fill="x")
        tab_bar = tk.Frame(inner, bg=BG_DARK)
        tab_bar.pack(fill="x")

        # Green underline indicator — moves between tabs
        tab_indicator = tk.Frame(inner, bg=SUCCESS, height=3)
        tab_indicator.pack(fill="x")

        content_host  = tk.Frame(inner, bg=BG_DARK)
        content_host.pack(fill="both", expand=True)
        stock_frame   = tk.Frame(content_host, bg=BG_DARK)
        reviews_frame = tk.Frame(content_host, bg=BG_DARK)

        def _show_tab(tab):
            if tab == "stock":
                reviews_frame.pack_forget()
                stock_frame.pack(fill="both", expand=True)
                stock_btn.config(font=(FONT_FAMILY, 11, "bold"), fg=SUCCESS, bg=BG_CARD)
                reviews_btn.config(font=(FONT_FAMILY, 11), fg=TEXT_GRAY, bg=BG_DARK)
            else:
                stock_frame.pack_forget()
                reviews_frame.pack(fill="both", expand=True)
                reviews_btn.config(font=(FONT_FAMILY, 11, "bold"), fg=SUCCESS, bg=BG_CARD)
                stock_btn.config(font=(FONT_FAMILY, 11), fg=TEXT_GRAY, bg=BG_DARK)

        stock_btn = tk.Button(tab_bar, text="Stock",
                              font=(FONT_FAMILY, 11, "bold"), bg=BG_CARD, fg=SUCCESS,
                              relief="flat", bd=0, padx=0, pady=10, cursor="hand2",
                              command=lambda: _show_tab("stock"))
        stock_btn.pack(side="left", expand=True, fill="x")

        reviews_btn = tk.Button(tab_bar, text="Reviews",
                                font=(FONT_FAMILY, 11), bg=BG_DARK, fg=TEXT_GRAY,
                                relief="flat", bd=0, padx=0, pady=10, cursor="hand2",
                                command=lambda: _show_tab("reviews"))
        reviews_btn.pack(side="left", expand=True, fill="x")

        # ── Stock tab: product list rows (BG_CARD, same as reviews) ──
        for pname in products:
            row = tk.Frame(stock_frame, bg="#F3F3F3", padx=16, pady=10)
            row.pack(fill="x", padx=12, pady=(0, 8))
            thumb = tk.Canvas(row, width=68, height=52, bg=BG_INPUT, highlightthickness=0)
            thumb.pack(side="left")
            thumb.create_text(34, 26, text=self._product_icon(pname), font=(FONT_FAMILY, 20))
            tk.Label(row, text=pname, font=FONT_SM_BOLD,
                     bg="#F3F3F3", fg=TEXT_WHITE).pack(side="left", padx=(12, 0))

        # ── Reviews tab: top reviews cards ───────────────────────────
        tk.Label(reviews_frame, text="Top reviews",
                 font=FONT_SM_BOLD, bg=BG_DARK, fg=TEXT_WHITE,
                 padx=16).pack(anchor="w", pady=(12, 6))

        for rname, stars, comment in MOCK_REVIEWS.get(seller_name, _DEFAULT_REVIEWS):
            rc = tk.Frame(reviews_frame, bg="#F3F3F3", padx=14, pady=12)
            rc.pack(fill="x", padx=12, pady=(0, 8))
            tk.Label(rc, text=stars, font=(FONT_FAMILY, 12),
                     bg="#F3F3F3", fg=GOLD).pack(anchor="w")
            tk.Label(rc, text=f'"{comment}"',
                     font=FONT_SM_BOLD, bg="#F3F3F3", fg=TEXT_WHITE,
                     wraplength=300, justify="left").pack(anchor="w", pady=(4, 2))
            tk.Label(rc, text=f"— {rname}",
                     font=(FONT_FAMILY, 9, "italic"), bg="#F3F3F3",
                     fg=TEXT_GRAY).pack(anchor="w")

        _show_tab("stock")

    # ── Product Detail Popup ──────────────────────────────────────────
    def _open_product_detail(self, title: str, vendor: str,
                             unit_price: float, unit: str, seller_data: dict = None):
        sd = seller_data or {}
        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        popup.resizable(False, False)
        popup.configure(bg=BG_DARK)
        popup.grab_set()

        hero = tk.Canvas(popup, width=APP_WIDTH, height=200, bg="#D8EEE0", highlightthickness=0)
        hero.pack(fill="x")
        hero.create_text(APP_WIDTH // 2, 100, text=self._product_icon(title), font=(FONT_FAMILY, 64))
        back = tk.Button(hero, text="← Back", font=(FONT_FAMILY, 9, "bold"),
                         bg="#C8E4D0", fg=TEXT_GRAY, relief="flat", bd=0,
                         padx=10, pady=6, cursor="hand2", command=popup.destroy)
        hero.create_window(12, 12, window=back, anchor="nw")

        bc = tk.Canvas(popup, bg=BG_DARK, highlightthickness=0)
        bsb = tk.Scrollbar(popup, orient="vertical", command=bc.yview)
        bc.configure(yscrollcommand=bsb.set)
        bsb.pack(side="right", fill="y")
        bc.pack(side="left", fill="both", expand=True)
        body = tk.Frame(bc, bg=BG_DARK)
        bwin = bc.create_window((0, 0), window=body, anchor="nw")
        body.bind("<Configure>", lambda e: bc.configure(scrollregion=bc.bbox("all")))
        bc.bind("<Configure>", lambda e: bc.itemconfig(bwin, width=e.width))
        bc.bind("<MouseWheel>", lambda e: bc.yview_scroll(int(-1 * e.delta / 120), "units"))

        ic = tk.Frame(body, bg=BG_CARD, padx=20, pady=18,
                      highlightbackground=BORDER, highlightthickness=1)
        ic.pack(fill="x", padx=14, pady=(14, 0))

        tk.Label(ic, text=title, font=(FONT_FAMILY, 20, "bold"),
                 bg=BG_CARD, fg=TEXT_WHITE, wraplength=360, justify="left").pack(anchor="w")

        pr = tk.Frame(ic, bg=BG_CARD)
        pr.pack(anchor="w", pady=(6, 0))
        tk.Label(pr, text=f"N{unit_price:,.0f}", font=(FONT_FAMILY, 18, "bold"),
                 bg=BG_CARD, fg=PRIMARY).pack(side="left")
        tk.Label(pr, text=f"  per {unit}", font=(FONT_FAMILY, 11),
                 bg=BG_CARD, fg=TEXT_GRAY).pack(side="left")

        rating = sd.get("rating", 4.5)
        orders = sd.get("order_count", 0)
        tk.Label(ic, text=f"⭐ {rating}/5  ({orders:,} orders)",
                 font=FONT_SM, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(6, 10))
        tk.Frame(ic, bg=BORDER_LIGHT, height=1).pack(fill="x", pady=(0, 14))

        tk.Label(ic, text="Select quantity", font=FONT_SM_BOLD,
                 bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")
        qr = tk.Frame(ic, bg=BG_CARD)
        qr.pack(fill="x", pady=(10, 0))

        qty = [10]
        qty_sv   = tk.StringVar(value="10")
        total_sv = tk.StringVar(value=f"N{unit_price * 10:,.0f}")

        def _refresh():
            qty_sv.set(str(qty[0]))
            total_sv.set(f"N{unit_price * qty[0]:,.0f}")

        ctrl = tk.Frame(qr, bg=BG_INPUT, highlightbackground=BORDER, highlightthickness=1)
        ctrl.pack(side="left")
        tk.Button(ctrl, text="-", font=(FONT_FAMILY, 14, "bold"), bg=BG_INPUT, fg=TEXT_WHITE,
                  relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
                  command=lambda: (qty.__setitem__(0, max(10, qty[0]-1)), _refresh())
                  ).pack(side="left")
        tk.Label(ctrl, textvariable=qty_sv, font=(FONT_FAMILY, 13, "bold"),
                 bg=BG_INPUT, fg=TEXT_WHITE, width=4, anchor="center").pack(side="left")
        tk.Button(ctrl, text="+", font=(FONT_FAMILY, 14, "bold"), bg=BG_INPUT, fg=TEXT_WHITE,
                  relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
                  command=lambda: (qty.__setitem__(0, qty[0]+1), _refresh())
                  ).pack(side="left")

        tb = tk.Frame(qr, bg=BG_CARD)
        tb.pack(side="right")
        tk.Label(tb, text="Total cost:", font=FONT_SM, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="e")
        tk.Label(tb, textvariable=total_sv, font=(FONT_FAMILY, 17, "bold"),
                 bg=BG_CARD, fg=PRIMARY).pack(anchor="e")

        tk.Label(ic, text=f"Min. order: 10 {unit}s", font=FONT_XS,
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(10, 0))

        def _add_to_cart():
            cart.add_item(
                product_name=title,
                vendor=vendor,
                unit_price=unit_price,
                unit=unit,
                qty=qty[0],
                seller_data=sd,
            )
            messagebox.showinfo(
                "Added to Cart ✅",
                f"Product : {title}\nQty     : {qty[0]} {unit}s\nTotal   : {total_sv.get()}"
            )

        tk.Button(ic, text="Add to Cart", font=(FONT_FAMILY, 11, "bold"),
                  bg=PRIMARY, fg="#FFFFFF", activebackground=PRIMARY_DARK,
                  activeforeground="#FFFFFF", relief="flat", bd=0, pady=14, cursor="hand2",
                  command=_add_to_cart
                  ).pack(fill="x", pady=(16, 0))

        tk.Label(body, text="Seller", font=(FONT_FAMILY, 13, "bold"),
                 bg=BG_DARK, fg=TEXT_WHITE).pack(anchor="w", padx=14, pady=(18, 6))

        sc2 = tk.Frame(body, bg=BG_CARD, padx=16, pady=16,
                       highlightbackground=BORDER, highlightthickness=1)
        sc2.pack(fill="x", padx=14, pady=(0, 20))
        top = tk.Frame(sc2, bg=BG_CARD)
        top.pack(fill="x")
        av2 = tk.Canvas(top, width=46, height=46, bg=BG_CARD, highlightthickness=0)
        av2.pack(side="left", padx=(0, 14))
        av2.create_oval(2, 2, 44, 44, fill=PRIMARY, outline=PRIMARY_DARK, width=2)
        av2.create_text(23, 23, text="".join(w[0].upper() for w in vendor.split()[:2]),
                        font=(FONT_FAMILY, 13, "bold"), fill="#FFFFFF")
        si = tk.Frame(top, bg=BG_CARD)
        si.pack(side="left", fill="both", expand=True)
        tk.Label(si, text=vendor[:26], font=FONT_MD_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(si, text=sd.get("location", "Mile 12 Market, Lagos"),
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")
        tk.Label(si, text=f"⭐ {rating}  |  {orders:,} bulk orders",
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(2, 0))

        # Green arrow button — top right of seller card
        arrow_btn = tk.Canvas(top, width=36, height=36, bg=PRIMARY,
                              highlightthickness=0, cursor="hand2")
        arrow_btn.pack(side="right")
        arrow_btn.create_text(18, 18, text="↗", font=(FONT_FAMILY, 16, "bold"), fill="#FFFFFF")
        arrow_btn.bind("<Button-1>", lambda e: self._open_seller_profile(vendor, sd))
        arrow_btn.bind("<Enter>", lambda e: arrow_btn.config(bg=PRIMARY_DARK))
        arrow_btn.bind("<Leave>", lambda e: arrow_btn.config(bg=PRIMARY))

        tk.Frame(sc2, bg=BORDER, height=1).pack(fill="x", pady=(14, 12))
        phone = sd.get("phone", "N/A")
        br2 = tk.Frame(sc2, bg=BG_CARD)
        br2.pack(fill="x")
        tk.Button(br2, text="📞  Call", font=FONT_MD_BOLD, bg=BG_CARD_ALT, fg=TEXT_WHITE,
                  activebackground=PRIMARY, activeforeground="#FFFFFF",
                  relief="flat", bd=0, padx=16, pady=12, cursor="hand2",
                  command=lambda: messagebox.showinfo("Call Seller", f"Calling {vendor}…\n{phone}")
                  ).pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Button(br2, text="💬  Message", font=FONT_MD_BOLD, bg=BG_CARD_ALT, fg=TEXT_WHITE,
                  activebackground=INFO, activeforeground="#FFFFFF",
                  relief="flat", bd=0, padx=16, pady=12, cursor="hand2",
                  command=lambda: messagebox.showinfo("Message", f"Opening chat with {vendor}…")
                  ).pack(side="left", fill="x", expand=True)

    @staticmethod
    def _product_icon(title: str) -> str:
        t = title.lower()
        if any(k in t for k in ["fish", "tilapia", "catfish", "croaker", "sardine", "mackar"]): return "🐟"
        if any(k in t for k in ["beef", "goat", "meat", "ponmo", "shaki", "cow"]):  return "🥩"
        if any(k in t for k in ["yam", "cocoyam", "tuber", "cassava", "potato"]):   return "🥔"
        if any(k in t for k in ["leaf", "ugu", "waterleaf", "bitter", "scent", "tomato"]): return "🌿"
        if any(k in t for k in ["crayfish", "ogiri", "uziza", "ginger", "garlic", "turmeric"]): return "🌶️"
        return "🛒"
