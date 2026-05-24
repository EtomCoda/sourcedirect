# ╔══════════════════════════════════════════════════════════════════╗
# ║  MEMBER 6 — HANDPICKED SELLER CONSOLE                            ║
# ║  Module : modules/seller_dashboard.py                            ║
# ║  Role   : Generates the specialized vendor backend console       ║
# ║           seen only when an authenticated seller signs in        ║
# ╚══════════════════════════════════════════════════════════════════╝

import tkinter as tk
from tkinter import messagebox
from modules.constants import *


class SellerDashboard(tk.Frame):
    """
    Merchant-facing backend console for SourceDirect.
    Allows authenticated sellers to view and update their live inventory.
    """

    def __init__(self, root_window, seller_name: str,
                 data_manager, on_logout_callback):
        """
        Renders the vendor backend screen console.

        Args:
            root_window        : Parent tk.Tk application window.
            seller_name        : Authenticated seller's display name.
            data_manager       : DataManager instance for read/write.
            on_logout_callback : Callable fired when seller logs out.
        """
        super().__init__(root_window, bg=BG_DARK)
        self.seller_name    = seller_name
        self.data_manager   = data_manager
        self.on_logout      = on_logout_callback
        self._entry_refs    = {}   # {product_name: (price_var, stock_var)}

        self._build_layout()
        self.populate_inventory_editor()

    # ── Layout ────────────────────────────────────────────────────────
    def _build_layout(self):
        """Assembles the seller console header and scrollable editor area."""
        # ── Header ────────────────────────────────────────────────
        header = tk.Frame(self, bg="#0A1219", padx=16, pady=14)
        header.pack(fill="x")

        left = tk.Frame(header, bg="#0A1219")
        left.pack(side="left", fill="y")
        tk.Label(left, text="🌿 SourceDirect",
                 font=(FONT_FAMILY, 13, "bold"), bg="#0A1219", fg=PRIMARY).pack(anchor="w")
        tk.Label(left, text=f"Seller Console  ·  {self.seller_name}",
                 font=FONT_XS, bg="#0A1219", fg=ACCENT).pack(anchor="w")

        tk.Button(
            header, text="Log Out  ↩",
            font=(FONT_FAMILY, 9, "bold"),
            bg=DANGER, fg=TEXT_WHITE,
            activebackground="#CC0022", activeforeground=TEXT_WHITE,
            relief="flat", bd=0, padx=12, pady=6, cursor="hand2",
            command=self._confirm_logout,
        ).pack(side="right")

        # ── Stats strip ───────────────────────────────────────────
        stats = tk.Frame(self, bg=BG_CARD, padx=16, pady=12)
        stats.pack(fill="x", pady=(0, 2))

        products = self.data_manager.get_seller_products(self._resolve_seller_name())
        total_items = len(products)
        total_stock = sum(p["stock"] for p in products.values())
        low_stock   = sum(1 for p in products.values() if p["stock"] <= 50)

        for label, val, color in [
            ("📦  Products", str(total_items), TEXT_WHITE),
            ("🗃️  Total Stock", f"{total_stock:,} units", INFO),
            ("⚠️  Low Stock", str(low_stock), DANGER if low_stock else SUCCESS),
        ]:
            col = tk.Frame(stats, bg=BG_CARD)
            col.pack(side="left", expand=True)
            tk.Label(col, text=val, font=(FONT_FAMILY, 18, "bold"),
                     bg=BG_CARD, fg=color).pack()
            tk.Label(col, text=label, font=FONT_XS,
                     bg=BG_CARD, fg=TEXT_GRAY).pack()

        # ── Scroll area for inventory editor ──────────────────────
        wrap = tk.Frame(self, bg=BG_DARK)
        wrap.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(wrap, bg=BG_DARK, highlightthickness=0)
        sb = tk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)

        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.editor_frame = tk.Frame(self.canvas, bg=BG_DARK)
        self.editor_window = self.canvas.create_window((0, 0), window=self.editor_frame, anchor="nw")

        self.editor_frame.bind("<Configure>",
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self.editor_window, width=e.width))
        self.canvas.bind("<MouseWheel>",
                         lambda e: self.canvas.yview_scroll(int(-1 * e.delta / 120), "units"))

        # Save button at the bottom
        tk.Button(
            self, text="💾  Save All Changes",
            font=(FONT_FAMILY, 11, "bold"),
            bg=PRIMARY, fg=BG_DARK,
            activebackground=PRIMARY_DARK, activeforeground=TEXT_WHITE,
            relief="flat", bd=0, pady=14, cursor="hand2",
            command=self.save_inventory_changes,
        ).pack(fill="x", padx=0, pady=0)

    def populate_inventory_editor(self):
        """
        Creates editable Entry input tables mapping out the merchant's live items.
        Each product row shows name, current price, and stock count with Entry widgets.
        """
        for widget in self.editor_frame.winfo_children():
            widget.destroy()
        self._entry_refs.clear()

        seller_key = self._resolve_seller_name()
        products = self.data_manager.get_seller_products(seller_key)

        # Section header
        hdr = tk.Frame(self.editor_frame, bg=BG_DARK, padx=16, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📋  Your Live Inventory",
                 font=FONT_LG_BOLD, bg=BG_DARK, fg=TEXT_WHITE).pack(side="left")
        tk.Label(hdr, text="Edit prices & stock · then Save",
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_GRAY).pack(side="right")

        # Column headers
        col_bar = tk.Frame(self.editor_frame, bg=BG_HEADER, padx=16, pady=6)
        col_bar.pack(fill="x")
        for txt, w in [("Product", 160), ("Price (N)", 90), ("Stock", 70), ("Unit", 60)]:
            tk.Label(col_bar, text=txt, font=(FONT_FAMILY, 8, "bold"),
                     bg=BG_HEADER, fg=TEXT_GRAY, width=0, anchor="w").pack(side="left", padx=(0, 8))

        # Product rows
        for idx, (pname, pdata) in enumerate(products.items()):
            row_bg = BG_CARD if idx % 2 == 0 else BG_CARD_ALT
            row = tk.Frame(self.editor_frame, bg=row_bg, padx=16, pady=8)
            row.pack(fill="x")

            # Product name
            tk.Label(row, text=pname, font=FONT_SM_BOLD,
                     bg=row_bg, fg=TEXT_WHITE, width=20, anchor="w").pack(side="left")

            # Price entry
            price_var = tk.StringVar(value=str(int(pdata["price"])))
            price_entry = tk.Entry(
                row, textvariable=price_var, font=FONT_BASE,
                bg=BG_INPUT, fg=TEXT_WHITE, insertbackground=PRIMARY,
                relief="flat", bd=0, width=10,
            )
            price_entry.pack(side="left", padx=(0, 14), ipady=4)

            # Stock entry
            stock_var = tk.StringVar(value=str(pdata["stock"]))
            stock_entry = tk.Entry(
                row, textvariable=stock_var, font=FONT_BASE,
                bg=BG_INPUT, fg=TEXT_WHITE, insertbackground=PRIMARY,
                relief="flat", bd=0, width=8,
            )
            stock_entry.pack(side="left", padx=(0, 14), ipady=4)

            # Unit label
            tk.Label(row, text=pdata.get("unit", "—"),
                     font=FONT_XS, bg=row_bg, fg=TEXT_MUTED).pack(side="left")

            # Stock warning indicator
            if pdata["stock"] <= 50:
                tk.Label(row, text="⚠ Low", font=(FONT_FAMILY, 8, "bold"),
                         bg=row_bg, fg=DANGER).pack(side="right")

            self._entry_refs[pname] = (price_var, stock_var)

    def save_inventory_changes(self):
        """
        Collects all entry input values and pipes updates through DataManager.
        Validates numeric input before saving.
        """
        seller_key = self._resolve_seller_name()
        errors = []
        saved  = 0

        for pname, (price_var, _stock_var) in self._entry_refs.items():
            raw_price = price_var.get().strip()
            try:
                new_price = float(raw_price)
                success = self.data_manager.update_seller_product(seller_key, pname, new_price)
                if success:
                    saved += 1
                else:
                    errors.append(f"'{pname}' — save failed (check DataManager).")
            except ValueError:
                errors.append(f"'{pname}' — invalid price: '{raw_price}'")

        if errors:
            messagebox.showwarning(
                "Save Warnings",
                f"{saved} product(s) saved.\n\nIssues:\n" + "\n".join(errors),
            )
        else:
            messagebox.showinfo(
                "Saved Successfully ✅",
                f"All {saved} products updated successfully!\n"
                f"Changes written to market_data.json.",
            )
        # Refresh the editor to reflect saved values
        self.populate_inventory_editor()

    # ── Helpers ───────────────────────────────────────────────────────
    def _resolve_seller_name(self) -> str:
        """
        Attempts to match self.seller_name against data keys.
        Returns the exact key as stored in market_data.json.
        """
        all_data = self.data_manager.get_all_sellers()
        sellers  = all_data.get("sellers", {})
        # Direct match first
        if self.seller_name in sellers:
            return self.seller_name
        # Case-insensitive partial match
        lower = self.seller_name.lower()
        for key in sellers:
            if lower in key.lower() or key.lower().startswith(lower.split()[0]):
                return key
        return self.seller_name

    def _confirm_logout(self):
        """Prompts the seller to confirm before logging out."""
        if messagebox.askyesno("Logout", f"Log out of your seller account?\n({self.seller_name})"):
            print(f"[SellerDashboard] '{self.seller_name}' logged out.")
            self.on_logout()
