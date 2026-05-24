# ╔══════════════════════════════════════════════════════════════════╗
# ║  MEMBER 4 — GRID CARD COMPONENT BUILDER                          ║
# ║  Module : modules/catalog_components.py                          ║
# ╚══════════════════════════════════════════════════════════════════╝

import tkinter as tk
from tkinter import messagebox
import modules.cart_manager as cart
from modules.constants import *

MOCK_REVIEWS = [
    ("Adeola R.",    "★★★★★", "Very fresh produce, delivered on time. Will order again!"),
    ("Chibuzor M.",  "★★★★",  "Good quality but packaging could be better."),
    ("Fatimah A.",   "★★★★★", "Best bulk supplier in Mile 12. Honest seller."),
    ("Mr. Temi O.",  "★★★★",  "Price is fair for the quantity. Highly recommend."),
    ("Mrs. Ngozi P.","★★★★★", "Consistent quality every order. My go-to supplier."),
]


class CatalogComponents:
    """Builds seller cards, product cards, and full detail/profile popups."""

    def __init__(self):
        self._current_row = None

    # ── Seller card ───────────────────────────────────────────────────
    def render_seller_card(self, parent, seller_name: str, rating: float,
                           order_count: int, on_view_stock=None,
                           seller_data: dict = None):
        card = tk.Frame(parent, bg=BG_CARD, padx=14, pady=14, relief="flat", bd=0, cursor="hand2")
        card.pack(fill="x", pady=5)

        av = tk.Canvas(card, width=52, height=52, bg=BG_CARD, highlightthickness=0)
        av.pack(side="left", padx=(0, 12))
        av.create_oval(2, 2, 50, 50, fill=PRIMARY_DARK, outline=PRIMARY, width=2)
        av.create_text(26, 26, text="".join(w[0].upper() for w in seller_name.split()[:2]),
                       font=(FONT_FAMILY, 14, "bold"), fill=TEXT_WHITE)

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
                  bg=PRIMARY, fg=BG_DARK, activebackground=PRIMARY_DARK,
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
        if col_index % 4 == 0:
            self._current_row = tk.Frame(parent, bg=BG_DARK)
            self._current_row.pack(fill="x", pady=4)

        card = tk.Frame(self._current_row, bg=BG_CARD, relief="flat", bd=0, cursor="hand2")
        card.pack(side="left", padx=(0, 16) if col_index % 4 != 3 else (0, 0))

        ic = tk.Canvas(card, width=195, height=110, bg="#162130", highlightthickness=0)
        ic.pack()
        ic.create_text(97, 55, text=self._product_icon(title), font=(FONT_FAMILY, 32))
        ic.create_rectangle(0, 0, 80, 20, fill=ACCENT, outline="")
        ic.create_text(40, 10, text="⭐ Best Seller", font=(FONT_FAMILY, 7, "bold"), fill=TEXT_WHITE)

        body = tk.Frame(card, bg=BG_CARD, padx=10, pady=8)
        body.pack(fill="x")
        tk.Label(body, text=(title if len(title) <= 20 else title[:18] + "…"),
                 font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(body, text=vendor, font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")
        tk.Label(body, text=price_string, font=(FONT_FAMILY, 12, "bold"),
                 bg=BG_CARD, fg=PRIMARY).pack(anchor="w", pady=(4, 6))
        tk.Button(body, text="Product Details", font=(FONT_FAMILY, 8, "bold"),
                  bg=BG_CARD_ALT, fg=TEXT_LIGHT, activebackground=PRIMARY,
                  activeforeground=BG_DARK, relief="flat", bd=0,
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

        # ── Header ────────────────────────────────────────────────
        hdr = tk.Frame(popup, bg=BG_HEADER, padx=16, pady=14)
        hdr.pack(fill="x")

        tk.Button(hdr, text="← Back", font=(FONT_FAMILY, 9, "bold"),
                  bg=BG_HEADER, fg=TEXT_GRAY, relief="flat", bd=0,
                  cursor="hand2", command=popup.destroy).pack(anchor="w")

        tk.Label(hdr, text="● Online now" if online else f"● {resp}",
                 font=(FONT_FAMILY, 9, "bold"), bg=BG_HEADER,
                 fg=SUCCESS if online else WARNING).pack(anchor="w", pady=(4, 0))
        tk.Label(hdr, text=seller_name, font=(FONT_FAMILY, 20, "bold"),
                 bg=BG_HEADER, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(hdr, text=location, font=FONT_SM,
                 bg=BG_HEADER, fg=TEXT_GRAY).pack(anchor="w")

        # Avatar + buttons row
        ar = tk.Frame(hdr, bg=BG_HEADER)
        ar.pack(fill="x", pady=(14, 0))

        av = tk.Canvas(ar, width=52, height=52, bg=BG_HEADER, highlightthickness=0)
        av.pack(side="left", padx=(0, 14))
        av.create_oval(2, 2, 50, 50, fill=PRIMARY_DARK, outline=PRIMARY, width=2)
        av.create_text(26, 26, text="".join(w[0].upper() for w in seller_name.split()[:2]),
                       font=(FONT_FAMILY, 15, "bold"), fill=TEXT_WHITE)

        btns = tk.Frame(ar, bg=BG_HEADER)
        btns.pack(side="right")
        tk.Button(btns, text="📞  Call", font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE,
                  relief="flat", bd=0, padx=18, pady=10, cursor="hand2",
                  command=lambda: messagebox.showinfo(
                      "Call Seller", f"Calling {seller_name}…\nPhone: {phone}")
                  ).pack(side="left", padx=(0, 8))
        tk.Button(btns, text="💬  Message", font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE,
                  relief="flat", bd=0, padx=18, pady=10, cursor="hand2",
                  command=lambda: messagebox.showinfo(
                      "Message Seller", f"Opening chat with {seller_name}…")
                  ).pack(side="left")

        # ── Stats bar ─────────────────────────────────────────────
        stats_bar = tk.Frame(popup, bg=BG_CARD, pady=14)
        stats_bar.pack(fill="x")
        for i, (val, lbl) in enumerate([
            (f"⭐ {rating}/5", "rating"),
            (f"{orders:,}", "bulk orders"),
            (str(len(products)), "products"),
        ]):
            if i:
                tk.Frame(stats_bar, bg=BORDER_LIGHT, width=1).pack(side="left", fill="y", pady=4)
            col = tk.Frame(stats_bar, bg=BG_CARD)
            col.pack(side="left", expand=True)
            tk.Label(col, text=val, font=(FONT_FAMILY, 15, "bold"),
                     bg=BG_CARD, fg=TEXT_WHITE).pack()
            tk.Label(col, text=lbl, font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack()

        # ── Tab bar ───────────────────────────────────────────────
        tab_bar = tk.Frame(popup, bg=BG_CARD)
        tab_bar.pack(fill="x")

        stock_frame   = tk.Frame(popup, bg=BG_DARK)
        reviews_frame = tk.Frame(popup, bg=BG_DARK)
        stock_frame.pack(fill="both", expand=True)

        def show_stock():
            reviews_frame.pack_forget()
            stock_frame.pack(fill="both", expand=True)
            s_btn.config(bg=BG_DARK, fg=TEXT_WHITE)
            r_btn.config(bg=BG_CARD, fg=TEXT_GRAY)
            ind.config(bg=PRIMARY)

        def show_reviews():
            stock_frame.pack_forget()
            reviews_frame.pack(fill="both", expand=True)
            r_btn.config(bg=BG_DARK, fg=TEXT_WHITE)
            s_btn.config(bg=BG_CARD, fg=TEXT_GRAY)
            ind.config(bg=ACCENT)

        s_btn = tk.Button(tab_bar, text="Stock", font=FONT_MD_BOLD,
                          bg=BG_DARK, fg=TEXT_WHITE, relief="flat", bd=0,
                          padx=30, pady=12, cursor="hand2", command=show_stock)
        s_btn.pack(side="left", fill="x", expand=True)
        r_btn = tk.Button(tab_bar, text="Reviews", font=FONT_MD_BOLD,
                          bg=BG_CARD, fg=TEXT_GRAY, relief="flat", bd=0,
                          padx=30, pady=12, cursor="hand2", command=show_reviews)
        r_btn.pack(side="left", fill="x", expand=True)
        ind = tk.Frame(tab_bar, bg=PRIMARY, height=3)
        ind.pack(fill="x")

        # ── Stock tab ─────────────────────────────────────────────
        sc = tk.Canvas(stock_frame, bg=BG_DARK, highlightthickness=0)
        sc_sb = tk.Scrollbar(stock_frame, orient="vertical", command=sc.yview)
        sc.configure(yscrollcommand=sc_sb.set)
        sc_sb.pack(side="right", fill="y")
        sc.pack(side="left", fill="both", expand=True)

        sc_inner = tk.Frame(sc, bg=BG_DARK)
        sc_win = sc.create_window((0, 0), window=sc_inner, anchor="nw")
        sc_inner.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))
        sc.bind("<Configure>", lambda e: sc.itemconfig(sc_win, width=e.width))
        sc.bind("<MouseWheel>", lambda e: sc.yview_scroll(int(-1 * e.delta / 120), "units"))

        for idx, (pname, pdata) in enumerate(products.items()):
            rbg = BG_CARD if idx % 2 == 0 else BG_CARD_ALT
            row = tk.Frame(sc_inner, bg=rbg, pady=10, padx=14, cursor="hand2")
            row.pack(fill="x", pady=1)

            thumb = tk.Canvas(row, width=52, height=52, bg="#162130", highlightthickness=0)
            thumb.pack(side="left", padx=(0, 14))
            thumb.create_text(26, 26, text=self._product_icon(pname), font=(FONT_FAMILY, 22))

            pi = tk.Frame(row, bg=rbg)
            pi.pack(side="left", fill="both", expand=True)
            tk.Label(pi, text=pname, font=FONT_SM_BOLD, bg=rbg, fg=TEXT_WHITE).pack(anchor="w")
            tk.Label(pi, text=f"N{pdata['price']:,.0f} / {pdata.get('unit','unit')}",
                     font=FONT_XS, bg=rbg, fg=PRIMARY).pack(anchor="w")

            stk = pdata.get("stock", 0)
            tk.Label(row, text=f"{stk} left",
                     font=(FONT_FAMILY, 8, "bold"), bg=rbg,
                     fg=DANGER if stk <= 50 else TEXT_GRAY).pack(side="right")

            row.bind("<Enter>", lambda e, r=row: r.config(bg=BG_CARD_ALT))
            row.bind("<Leave>", lambda e, r=row, b=rbg: r.config(bg=b))

        # ── Reviews tab ───────────────────────────────────────────
        rv = tk.Canvas(reviews_frame, bg=BG_DARK, highlightthickness=0)
        rv_sb = tk.Scrollbar(reviews_frame, orient="vertical", command=rv.yview)
        rv.configure(yscrollcommand=rv_sb.set)
        rv_sb.pack(side="right", fill="y")
        rv.pack(side="left", fill="both", expand=True)

        rv_inner = tk.Frame(rv, bg=BG_DARK)
        rv_win = rv.create_window((0, 0), window=rv_inner, anchor="nw")
        rv_inner.bind("<Configure>", lambda e: rv.configure(scrollregion=rv.bbox("all")))
        rv.bind("<Configure>", lambda e: rv.itemconfig(rv_win, width=e.width))
        rv.bind("<MouseWheel>", lambda e: rv.yview_scroll(int(-1 * e.delta / 120), "units"))

        for rname, stars, comment in MOCK_REVIEWS:
            rc = tk.Frame(rv_inner, bg=BG_CARD, padx=14, pady=12)
            rc.pack(fill="x", padx=12, pady=(8, 0))
            top = tk.Frame(rc, bg=BG_CARD)
            top.pack(fill="x")
            tk.Label(top, text=rname, font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(side="left")
            tk.Label(top, text=stars, font=(FONT_FAMILY, 9), bg=BG_CARD, fg=GOLD).pack(side="right")
            tk.Label(rc, text=comment, font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY,
                     wraplength=360, justify="left").pack(anchor="w", pady=(6, 0))

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

        # Hero image
        hero = tk.Canvas(popup, width=APP_WIDTH, height=200, bg="#101E2C", highlightthickness=0)
        hero.pack(fill="x")
        hero.create_text(APP_WIDTH // 2, 100, text=self._product_icon(title),
                         font=(FONT_FAMILY, 64))
        back = tk.Button(hero, text="← Back", font=(FONT_FAMILY, 9, "bold"),
                         bg="#0A1219", fg=TEXT_GRAY, relief="flat", bd=0,
                         padx=10, pady=6, cursor="hand2", command=popup.destroy)
        hero.create_window(12, 12, window=back, anchor="nw")

        # Scrollable body
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

        # Product info card
        ic = tk.Frame(body, bg=BG_CARD, padx=20, pady=18)
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

        # Quantity selector
        tk.Label(ic, text="Select quantity", font=FONT_SM_BOLD,
                 bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")
        qr = tk.Frame(ic, bg=BG_CARD)
        qr.pack(fill="x", pady=(10, 0))

        qty = [10]
        qty_sv  = tk.StringVar(value="10")
        total_sv = tk.StringVar(value=f"N{unit_price * 10:,.0f}")

        def _refresh():
            qty_sv.set(str(qty[0]))
            total_sv.set(f"N{unit_price * qty[0]:,.0f}")

        ctrl = tk.Frame(qr, bg=BG_INPUT)
        ctrl.pack(side="left")
        tk.Button(ctrl, text="-", font=(FONT_FAMILY, 14, "bold"), bg=BG_INPUT, fg=TEXT_WHITE,
                  relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
                  command=lambda: (qty.__setitem__(0, max(1, qty[0]-1)), _refresh())
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
        tk.Button(ic, text="Add to Cart", font=(FONT_FAMILY, 11, "bold"),
                  bg=BG_CARD_ALT, fg=TEXT_WHITE, activebackground=PRIMARY,
                  activeforeground=BG_DARK, relief="flat", bd=0, pady=14, cursor="hand2",
                  command=lambda: messagebox.showinfo(
                      "Added to Cart ✅",
                      f"Product : {title}\nQty     : {qty[0]} {unit}s\nTotal   : {total_sv.get()}")
                  ).pack(fill="x", pady=(16, 0))

        # Seller mini-card
        tk.Label(body, text="Seller", font=(FONT_FAMILY, 13, "bold"),
                 bg=BG_DARK, fg=TEXT_WHITE).pack(anchor="w", padx=14, pady=(18, 6))

        sc2 = tk.Frame(body, bg=BG_CARD, padx=16, pady=16)
        sc2.pack(fill="x", padx=14, pady=(0, 20))
        top = tk.Frame(sc2, bg=BG_CARD)
        top.pack(fill="x")

        av2 = tk.Canvas(top, width=46, height=46, bg=BG_CARD, highlightthickness=0)
        av2.pack(side="left", padx=(0, 14))
        av2.create_oval(2, 2, 44, 44, fill=PRIMARY_DARK, outline=PRIMARY, width=2)
        av2.create_text(23, 23, text="".join(w[0].upper() for w in vendor.split()[:2]),
                        font=(FONT_FAMILY, 13, "bold"), fill=TEXT_WHITE)

        si = tk.Frame(top, bg=BG_CARD)
        si.pack(side="left", fill="both", expand=True)
        tk.Label(si, text=vendor[:26], font=FONT_MD_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(si, text=sd.get("location", "Mile 12 Market, Lagos"),
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")
        tk.Label(si, text=f"⭐ {rating}  |  {orders:,} bulk orders",
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(2, 0))

        tk.Frame(sc2, bg=BORDER, height=1).pack(fill="x", pady=(14, 12))

        phone = sd.get("phone", "N/A")
        br2 = tk.Frame(sc2, bg=BG_CARD)
        br2.pack(fill="x")
        tk.Button(br2, text="📞  Call", font=FONT_MD_BOLD, bg=BG_CARD_ALT, fg=TEXT_WHITE,
                  activebackground=PRIMARY, activeforeground=BG_DARK,
                  relief="flat", bd=0, padx=16, pady=12, cursor="hand2",
                  command=lambda: messagebox.showinfo("Call Seller", f"Calling {vendor}…\n{phone}")
                  ).pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Button(br2, text="💬  Message", font=FONT_MD_BOLD, bg=BG_CARD_ALT, fg=TEXT_WHITE,
                  activebackground=INFO, activeforeground=BG_DARK,
                  relief="flat", bd=0, padx=16, pady=12, cursor="hand2",
                  command=lambda: messagebox.showinfo("Message", f"Opening chat with {vendor}…")
                  ).pack(side="left", fill="x", expand=True)

    # ── Static helper ─────────────────────────────────────────────────
    @staticmethod
    def _product_icon(title: str) -> str:
        t = title.lower()
        if any(k in t for k in ["fish", "tilapia", "catfish"]):        return "🐟"
        if any(k in t for k in ["chicken", "turkey", "frozen"]):       return "🍗"
        if any(k in t for k in ["beef", "goat", "meat", "assorted"]):  return "🥩"
        if any(k in t for k in ["yam", "cocoyam", "tuber"]):           return "🥔"
        if any(k in t for k in ["plantain"]):                          return "🍌"
        if any(k in t for k in ["tomato", "pepper"]):                  return "🍅"
        if any(k in t for k in ["onion", "carrot"]):                   return "🥕"
        if any(k in t for k in ["rice", "maize", "millet", "corn", "garri"]): return "🌾"
        if any(k in t for k in ["beans"]):                             return "🫘"
        if any(k in t for k in ["palm", "oil", "groundnut"]):          return "🫙"
        if any(k in t for k in ["leaf", "ugu", "waterleaf", "bitter", "scent", "uziza"]): return "🌿"
        if any(k in t for k in ["crayfish", "ogiri"]):                 return "🌶️"
        return "🛒"
