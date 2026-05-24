import tkinter as tk
from tkinter import messagebox
import modules.cart_manager as cart
from modules.constants import *


class CartPage:
    def __init__(self, parent, on_checkout_success=None,
                 data_manager=None, buyer_name: str = "Buyer"):
        self.parent = parent
        self.on_checkout_success = on_checkout_success
        self.data_manager = data_manager
        self.buyer_name = buyer_name
        self._popup = None

    def open(self):
        if self._popup and self._popup.winfo_exists():
            self._popup.lift()
            return
        self._build()

    def _build(self):
        popup = tk.Toplevel(self.parent)
        popup.title("Cart")
        popup.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        popup.resizable(False, False)
        popup.configure(bg=BG_DARK)
        popup.grab_set()
        self._popup = popup

        hdr = tk.Frame(popup, bg=BG_HEADER, padx=16, pady=14,
                       highlightbackground=BORDER, highlightthickness=1)
        hdr.pack(fill="x")
        tk.Button(hdr, text="←", font=(FONT_FAMILY, 16), bg=BG_HEADER, fg=TEXT_WHITE,
                  relief="flat", bd=0, cursor="hand2",
                  command=popup.destroy).pack(side="left")
        tk.Label(hdr, text="Cart", font=(FONT_FAMILY, 14, "bold"),
                 bg=BG_HEADER, fg=TEXT_WHITE).pack(side="left", padx=(12, 0))
        tk.Label(hdr, text="👤", font=(FONT_FAMILY, 14),
                 bg=BG_HEADER, fg=TEXT_GRAY).pack(side="right")

        items = cart.get_items()
        if not items:
            ef = tk.Frame(popup, bg=BG_DARK)
            ef.pack(fill="both", expand=True)
            tk.Label(ef, text="🛒", font=(FONT_FAMILY, 52), bg=BG_DARK).pack(pady=(120, 10))
            tk.Label(ef, text="Your cart is empty",
                     font=(FONT_FAMILY, 16, "bold"), bg=BG_DARK, fg=TEXT_WHITE).pack()
            tk.Label(ef, text="Go back and add items from the marketplace",
                     font=FONT_SM, bg=BG_DARK, fg=TEXT_GRAY).pack(pady=(4, 0))
            tk.Button(ef, text="← Continue Shopping",
                      font=FONT_MD_BOLD, bg=BG_CARD, fg=TEXT_WHITE,
                      relief="flat", bd=0, padx=20, pady=12, cursor="hand2",
                      command=popup.destroy).pack(pady=(30, 0))
            return

        list_wrap = tk.Frame(popup, bg=BG_DARK)
        list_wrap.pack(fill="both", expand=True, padx=14, pady=(14, 0))

        canvas = tk.Canvas(list_wrap, bg=BG_DARK, highlightthickness=0)
        sb = tk.Scrollbar(list_wrap, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=BG_DARK)
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * e.delta / 120), "units"))

        def _reload():
            popup.destroy()
            self._build()

        for pname, pdata in items.items():
            self._render_item(inner, pname, pdata, _reload)

        bottom = tk.Frame(popup, bg=BG_DARK, padx=14, pady=14)
        bottom.pack(fill="x", side="bottom")
        total = cart.get_total()
        tk.Label(bottom, text=f"Grand Total:  N{total:,.0f}",
                 font=(FONT_FAMILY, 13, "bold"), bg=BG_DARK, fg=PRIMARY).pack(anchor="w", pady=(0, 10))
        tk.Button(
            bottom, text="Proceed to Checkout",
            font=(FONT_FAMILY, 12, "bold"),
            bg=PRIMARY, fg="#FFFFFF",
            activebackground=PRIMARY_DARK, activeforeground="#FFFFFF",
            relief="flat", bd=0, pady=14, cursor="hand2",
            command=lambda: self._proceed(popup),
        ).pack(fill="x")

    def _render_item(self, parent, pname: str, pdata: dict, on_remove):
        from modules.catalog_components import CatalogComponents

        card = tk.Frame(parent, bg=BG_CARD, padx=14, pady=14,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", pady=(0, 8))

        thumb = tk.Canvas(card, width=60, height=60, bg="#D8EEE0", highlightthickness=0)
        thumb.pack(side="left", padx=(0, 14))
        thumb.create_text(30, 30, text=CatalogComponents._product_icon(pname),
                          font=(FONT_FAMILY, 24))

        mid = tk.Frame(card, bg=BG_CARD)
        mid.pack(side="left", fill="both", expand=True)

        nr = tk.Frame(mid, bg=BG_CARD)
        nr.pack(fill="x")
        tk.Label(nr, text=(pname if len(pname) <= 22 else pname[:20] + "…"),
                 font=FONT_MD_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(side="left")
        tk.Button(nr, text="✕", font=(FONT_FAMILY, 10, "bold"),
                  bg=BG_CARD, fg=DANGER, relief="flat", bd=0, cursor="hand2",
                  command=lambda p=pname: (cart.remove_item(p), on_remove())
                  ).pack(side="right")

        vendor = pdata.get("vendor", "")
        tk.Label(mid, text=f"{vendor}  ·  N{pdata['unit_price']:,.0f} / {pdata['unit']}",
                 font=FONT_XS, bg=BG_CARD, fg=PRIMARY).pack(anchor="w")

        tk.Label(mid, text="Select quantity", font=(FONT_FAMILY, 8),
                 bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(8, 2))

        qr = tk.Frame(mid, bg=BG_CARD)
        qr.pack(anchor="w")

        qty = [pdata["qty"]]
        qty_sv = tk.StringVar(value=str(qty[0]))

        def _refresh(p=pname):
            qty_sv.set(str(qty[0]))
            cart.update_qty(p, qty[0])
            sub_var.set(f"N{pdata['unit_price'] * qty[0]:,.0f}")
            on_remove()

        ctrl = tk.Frame(qr, bg=BG_INPUT, highlightbackground=BORDER, highlightthickness=1)
        ctrl.pack(side="left")
        # Min qty in cart is 1 (already purchased at minimum 10 from detail)
        tk.Button(ctrl, text="-", font=(FONT_FAMILY, 11, "bold"), bg=BG_INPUT, fg=TEXT_WHITE,
                  relief="flat", bd=0, padx=12, pady=6, cursor="hand2",
                  command=lambda: (qty.__setitem__(0, max(1, qty[0]-1)), _refresh())
                  ).pack(side="left")
        tk.Label(ctrl, textvariable=qty_sv, font=(FONT_FAMILY, 11, "bold"),
                 bg=BG_INPUT, fg=TEXT_WHITE, width=3, anchor="center").pack(side="left")
        tk.Button(ctrl, text="+", font=(FONT_FAMILY, 11, "bold"), bg=BG_INPUT, fg=TEXT_WHITE,
                  relief="flat", bd=0, padx=12, pady=6, cursor="hand2",
                  command=lambda: (qty.__setitem__(0, qty[0]+1), _refresh())
                  ).pack(side="left")

        sub_var = tk.StringVar(value=f"N{pdata['unit_price'] * qty[0]:,.0f}")
        tk.Label(qr, textvariable=sub_var, font=(FONT_FAMILY, 11, "bold"),
                 bg=BG_CARD, fg=TEXT_WHITE).pack(side="left", padx=(16, 0))

    def _proceed(self, cart_popup):
        cart_popup.destroy()
        page = CheckoutPage(self.parent, self.on_checkout_success,
                            data_manager=self.data_manager,
                            buyer_name=self.buyer_name)
        page.open()


class CheckoutPage:
    def __init__(self, parent, on_return_home=None,
                 data_manager=None, buyer_name: str = "Buyer"):
        self.parent = parent
        self.on_return_home = on_return_home
        self.data_manager = data_manager
        self.buyer_name = buyer_name

    def open(self):
        popup = tk.Toplevel(self.parent)
        popup.title("Checkout")
        popup.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        popup.resizable(False, False)
        popup.configure(bg=BG_DARK)
        popup.grab_set()

        hdr = tk.Frame(popup, bg=BG_HEADER, padx=16, pady=14,
                       highlightbackground=BORDER, highlightthickness=1)
        hdr.pack(fill="x")
        tk.Button(hdr, text="←", font=(FONT_FAMILY, 16), bg=BG_HEADER, fg=TEXT_WHITE,
                  relief="flat", bd=0, cursor="hand2",
                  command=popup.destroy).pack(side="left")
        tk.Label(hdr, text="Checkout", font=(FONT_FAMILY, 14, "bold"),
                 bg=BG_HEADER, fg=TEXT_WHITE).pack(side="left", padx=(12, 0))

        items = cart.get_items()
        total = cart.get_total()
        summary_frame = tk.Frame(popup, bg=BG_CARD, padx=16, pady=10,
                                 highlightbackground=BORDER, highlightthickness=1)
        summary_frame.pack(fill="x", padx=14, pady=(14, 0))
        tk.Label(summary_frame,
                 text=f"{len(items)} item type(s) ordered  ·  Total: N{total:,.0f}",
                 font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")

        main = tk.Frame(popup, bg=BG_DARK)
        main.pack(fill="both", expand=True)

        success_card = tk.Frame(main, bg=BG_CARD, padx=30, pady=40,
                                highlightbackground=PRIMARY, highlightthickness=2)
        success_card.pack(fill="x", padx=24, pady=(60, 0))
        tk.Label(success_card, text="Order Placed!",
                 font=(FONT_FAMILY, 26, "bold"), bg=BG_CARD, fg=PRIMARY).pack()
        tk.Label(success_card, text="Your bulk order has been submitted\nsuccessfully to the seller.",
                 font=FONT_MD, bg=BG_CARD, fg=TEXT_GRAY, justify="center").pack(pady=(10, 20))
        tk.Frame(success_card, bg=BORDER_LIGHT, height=1).pack(fill="x")
        tk.Label(success_card,
                 text=f"{len(items)} item type(s)   |   Grand Total: N{total:,.0f}",
                 font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(pady=(14, 0))

        note = tk.Frame(main, bg=BG_DARK, padx=24, pady=14)
        note.pack(fill="x")
        tk.Label(note, text="The seller will contact you within 1 business hour\nto confirm delivery details.",
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_MUTED, justify="center").pack()

        bottom = tk.Frame(popup, bg=BG_DARK, padx=14, pady=14)
        bottom.pack(fill="x", side="bottom")

        def _return_home():
            if self.data_manager:
                self.data_manager.place_order(self.buyer_name, cart.get_items())
            cart.clear()
            popup.destroy()
            if self.on_return_home:
                self.on_return_home()

        tk.Button(
            bottom, text="Return to Home Page",
            font=(FONT_FAMILY, 12, "bold"),
            bg=PRIMARY, fg="#FFFFFF",
            activebackground=PRIMARY_DARK, activeforeground="#FFFFFF",
            relief="flat", bd=0, pady=14, cursor="hand2",
            command=_return_home,
        ).pack(fill="x")
