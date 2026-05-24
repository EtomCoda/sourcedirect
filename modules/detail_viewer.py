import tkinter as tk
from tkinter import messagebox
from modules.constants import *


class DetailViewer:
    def __init__(self):
        self._active_popup = None

    def launch_storefront_popup(self, parent_window, seller_name: str, inventory_dict: dict):
        if self._active_popup and self._active_popup.winfo_exists():
            self._active_popup.destroy()

        popup = tk.Toplevel(parent_window)
        popup.title(f"{seller_name} — Storefront")
        popup.geometry("460x620")
        popup.resizable(False, True)
        popup.configure(bg=BG_DARK)
        popup.grab_set()
        self._active_popup = popup

        hdr = tk.Frame(popup, bg=BG_HEADER, padx=16, pady=14,
                       highlightbackground=BORDER, highlightthickness=1)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏪  " + seller_name,
                 font=(FONT_FAMILY, 14, "bold"), bg=BG_HEADER, fg=TEXT_WHITE).pack(side="left")
        tk.Button(hdr, text="✕  Close", font=FONT_XS,
                  bg=BG_CARD, fg=TEXT_GRAY, relief="flat", bd=0,
                  padx=10, pady=6, cursor="hand2",
                  command=popup.destroy).pack(side="right")
        tk.Label(popup, text="Mile 12 Market, Lagos  ·  Bulk Supply Catalog",
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_GRAY, pady=6).pack()

        list_wrap = tk.Frame(popup, bg=BG_DARK)
        list_wrap.pack(fill="both", expand=True, padx=14)

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

        th = tk.Frame(inner, bg=BG_CARD_ALT, padx=12, pady=8,
                      highlightbackground=BORDER, highlightthickness=1)
        th.pack(fill="x", pady=(0, 2))
        for txt, w in [("Product", 16), ("Price (N)", 10), ("Stock", 7), ("Unit", 7), ("Qty", 6)]:
            tk.Label(th, text=txt, font=(FONT_FAMILY, 8, "bold"),
                     bg=BG_CARD_ALT, fg=TEXT_GRAY, width=w, anchor="w").pack(side="left")

        qty_vars = {}
        for idx, (pname, pdata) in enumerate(inventory_dict.items()):
            row_bg = BG_CARD if idx % 2 == 0 else BG_CARD_ALT
            row = tk.Frame(inner, bg=row_bg, padx=12, pady=8,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=1)

            tk.Label(row, text=pname, font=FONT_SM_BOLD,
                     bg=row_bg, fg=TEXT_WHITE, width=16, anchor="w").pack(side="left")
            tk.Label(row, text=f"N{pdata['price']:,.0f}", font=FONT_BASE,
                     bg=row_bg, fg=PRIMARY, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=str(pdata["stock"]), font=FONT_BASE,
                     bg=row_bg, fg=TEXT_GRAY, width=7, anchor="w").pack(side="left")
            tk.Label(row, text=pdata.get("unit", "-"), font=FONT_XS,
                     bg=row_bg, fg=TEXT_MUTED, width=7, anchor="w").pack(side="left")

            qty_var = tk.IntVar(value=0)
            qty_vars[pname] = (qty_var, float(pdata["price"]))
            tk.Spinbox(row, from_=0, to=9999, textvariable=qty_var, width=5,
                       font=FONT_SM, bg=BG_INPUT, fg=TEXT_WHITE,
                       buttonbackground=BG_CARD_ALT, relief="flat", bd=0,
                       insertbackground=PRIMARY).pack(side="left", ipady=4)

            row.bind("<Enter>", lambda e, r=row: r.config(bg=BG_CARD_ALT))
            row.bind("<Leave>", lambda e, r=row, b=row_bg: r.config(bg=b))

        calc = tk.Frame(popup, bg=BG_CARD, padx=16, pady=14,
                        highlightbackground=BORDER, highlightthickness=1)
        calc.pack(fill="x", padx=14, pady=(8, 14))
        tk.Label(calc, text="🧾  Bulk Invoice Calculator",
                 font=FONT_MD_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(calc, text="Set a quantity for each item you need, then tap Generate",
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(2, 8))

        result_var = tk.StringVar(value="Set quantities above, then generate invoice.")
        tk.Label(calc, textvariable=result_var,
                 font=(FONT_FAMILY, 9, "bold"), bg=BG_CARD, fg=PRIMARY,
                 wraplength=380, justify="left").pack(anchor="w", pady=(0, 8))

        tk.Button(calc, text="  Generate Bulk Invoice  →",
                  font=(FONT_FAMILY, 10, "bold"),
                  bg=ACCENT, fg="#FFFFFF",
                  activebackground="#AA4400", activeforeground="#FFFFFF",
                  relief="flat", bd=0, padx=16, pady=12, cursor="hand2",
                  command=lambda: self.calculate_bulk_invoice(qty_vars, result_var),
                  ).pack(fill="x")

    def calculate_bulk_invoice(self, qty_vars: dict, result_var=None):
        selected = {
            name: (var.get(), price)
            for name, (var, price) in qty_vars.items()
            if var.get() > 0
        }
        if not selected:
            messagebox.showwarning("No Items Selected",
                                   "Please set a quantity (> 0) for at least one product.")
            return None

        lines = []
        grand_total = grand_subtotal = grand_discount = 0.0

        for pname, (qty, unit_price) in selected.items():
            subtotal = qty * unit_price
            disc_pct = 12 if qty >= 500 else 8 if qty >= 200 else 5 if qty >= 100 else 0
            disc_amt   = subtotal * (disc_pct / 100)
            item_total = subtotal - disc_amt
            grand_subtotal += subtotal
            grand_discount += disc_amt
            grand_total    += item_total
            short    = (pname[:20] + "...") if len(pname) > 20 else pname
            disc_tag = f"  (-{disc_pct}%)" if disc_pct else ""
            lines.append(f"  {short:<22} x{qty:>4}   N{item_total:>10,.0f}{disc_tag}")

        summary = (
            "SOURCEDIRECT BULK INVOICE\n" + "=" * 44 + "\n"
            + "\n".join(lines) + "\n" + "-" * 44 + "\n"
            + f"  Subtotal            N{grand_subtotal:>12,.2f}\n"
            + f"  Total Discounts     N{grand_discount:>12,.2f}\n"
            + "=" * 44 + "\n"
            + f"  GRAND TOTAL         N{grand_total:>12,.2f}\n\n"
            + f"  {len(selected)} item type(s)  |  "
            + ("Bulk discounts applied!" if grand_discount > 0
               else "Order 100+ units per item for discounts.")
        )
        if result_var:
            saved_txt = f"  |  N{grand_discount:,.2f} saved" if grand_discount else ""
            result_var.set(f"N{grand_total:,.2f} total  —  {len(selected)} item type(s){saved_txt}")
        messagebox.showinfo("Bulk Invoice", summary)
        return grand_total
