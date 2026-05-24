import tkinter as tk
from modules.constants import *


class ListRowComponents:
    def __init__(self):
        pass

    def render_low_cost_row(self, parent, product_name: str,
                            store_name: str, quantity_left: int):
        is_critical = quantity_left <= 50
        row = tk.Frame(parent, bg=BG_CARD, padx=14, pady=9, cursor="hand2",
                       highlightbackground=BORDER, highlightthickness=1)
        row.pack(fill="x", padx=12, pady=(0, 3))

        icon_bg = DANGER if is_critical else ACCENT
        tk.Label(row, text="🔥" if is_critical else "⚡",
                 font=(FONT_FAMILY, 14), bg=icon_bg,
                 padx=8, pady=2).pack(side="left", padx=(0, 10))

        info = tk.Frame(row, bg=BG_CARD)
        info.pack(side="left", fill="both", expand=True)
        tk.Label(info, text=product_name,
                 font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(info, text=f"from  {store_name}",
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")

        stock_frame = tk.Frame(row, bg=BG_CARD)
        stock_frame.pack(side="right")
        stock_text = f"Only {quantity_left} left!" if is_critical else f"{quantity_left} units"
        stock_color = DANGER if is_critical else WARNING
        tk.Label(stock_frame, text=stock_text,
                 font=(FONT_FAMILY, 9, "bold"), bg=BG_CARD, fg=stock_color).pack(anchor="e")
        tk.Label(stock_frame, text="Low cost · Selling fast",
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="e")

        row.bind("<Enter>", lambda e: row.config(bg=BG_CARD_ALT))
        row.bind("<Leave>", lambda e: row.config(bg=BG_CARD))

    def render_fast_response_row(self, parent, seller_name: str, status_time: str):
        is_online = status_time.lower() == "online now"
        row = tk.Frame(parent, bg=BG_CARD, padx=14, pady=8, cursor="hand2",
                       highlightbackground=BORDER, highlightthickness=1)
        row.pack(fill="x", padx=12, pady=(0, 3))

        dot_color = SUCCESS if is_online else WARNING
        dot = tk.Canvas(row, width=10, height=10, bg=BG_CARD, highlightthickness=0)
        dot.pack(side="left", padx=(0, 10), pady=5)
        dot.create_oval(0, 0, 10, 10, fill=dot_color, outline="")

        info = tk.Frame(row, bg=BG_CARD)
        info.pack(side="left", fill="both", expand=True)
        short_name = seller_name if len(seller_name) <= 24 else seller_name[:22] + "…"
        tk.Label(info, text=short_name,
                 font=FONT_SM_BOLD, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(info, text="Handpicked Seller · Mile 12 Market",
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")

        status_frame = tk.Frame(row, bg=BG_CARD)
        status_frame.pack(side="right")
        status_color = SUCCESS if is_online else WARNING
        tk.Label(status_frame, text=status_time,
                 font=(FONT_FAMILY, 9, "bold"), bg=BG_CARD, fg=status_color).pack(anchor="e")
        response_label = "Instant reply" if is_online else "Usually replies fast"
        tk.Label(status_frame, text=response_label,
                 font=FONT_XS, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="e")

        row.bind("<Enter>", lambda e: row.config(bg=BG_CARD_ALT))
        row.bind("<Leave>", lambda e: row.config(bg=BG_CARD))
