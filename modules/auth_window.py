import tkinter as tk
from tkinter import messagebox
from modules.constants import *


class AuthWindow(tk.Frame):
    VALID_BUYERS = {"simisola", "tunde", "bisi"}
    VALID_SELLERS = {
        "mama rashidat", "alhaja spices", "yam empire", "tuber house",
        "mama fish", "alhaji musa", "alhaji yakubu"
    }

    def __init__(self, parent_frame, on_login_success_callback, data_manager=None):
        super().__init__(parent_frame, bg=BG_DARK)
        self.on_login_success = on_login_success_callback
        self.data_manager = data_manager
        self.active_role = "Buyer"
        self._build_ui()

    def _build_ui(self):
        # ── Header banner ─────────────────────────────────────────
        banner = tk.Canvas(self, height=210, bg="#D0EAD8", highlightthickness=0)
        banner.pack(fill="x")
        banner.create_oval(-40, -40, 130, 130, fill="#B8DFC4", outline="")
        banner.create_oval(340, 100, 520, 280, fill="#B8DFC4", outline="")
        banner.create_oval(170, -70, 360, 120, fill="#C8E8D0", outline="")
        banner.create_text(225, 85,  text="🌿",          font=(FONT_FAMILY, 44), fill=PRIMARY)
        banner.create_text(225, 140, text="SourceDirect", font=(FONT_FAMILY, 24, "bold"), fill="#111111")
        banner.create_text(225, 168, text="Your number one source for farm produce",
                           font=(FONT_FAMILY, 9), fill="#555555")

        # ── Scrollable area for the form ──────────────────────────
        canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        inner = tk.Frame(canvas, bg=BG_DARK)
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * e.delta / 120), "units"))

        # ── Login card ────────────────────────────────────────────
        card = tk.Frame(inner, bg=BG_CARD, padx=28, pady=26,
                        relief="flat", bd=1, highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(fill="x", padx=22, pady=(20, 0))

        tk.Label(card, text="Welcome Back 👋",
                 font=(FONT_FAMILY, 17, "bold"), bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(card, text="Sign in to access the marketplace",
                 font=FONT_SM, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(2, 18))

        # Username
        tk.Label(card, text="USERNAME", font=(FONT_FAMILY, 8, "bold"),
                 bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")
        inp_wrap = tk.Frame(card, bg=BG_INPUT, padx=10, pady=8,
                            relief="solid", bd=1, highlightbackground=BORDER,
                            highlightthickness=1)
        inp_wrap.pack(fill="x", pady=(4, 14))
        tk.Label(inp_wrap, text="👤", bg=BG_INPUT, font=(FONT_FAMILY, 11)).pack(side="left", padx=(0, 8))
        self.username_entry = tk.Entry(
            inp_wrap, font=FONT_MD, bg=BG_INPUT, fg=TEXT_GRAY,
            insertbackground=PRIMARY, relief="flat", bd=0,
        )
        self.username_entry.pack(side="left", fill="x", expand=True)
        self.username_entry.insert(0, 'username')
        self.username_entry.bind("<FocusIn>",  self._clear_placeholder)
        self.username_entry.bind("<FocusOut>", self._restore_placeholder)
        self.username_entry.bind("<Return>",   lambda _e: self.password_entry.focus())

        # Password
        tk.Label(card, text="PASSWORD", font=(FONT_FAMILY, 8, "bold"),
                 bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(6, 0))
        pw_wrap = tk.Frame(card, bg=BG_INPUT, padx=10, pady=8,
                           relief="solid", bd=1, highlightbackground=BORDER,
                           highlightthickness=1)
        pw_wrap.pack(fill="x", pady=(4, 14))
        tk.Label(pw_wrap, text="🔒", bg=BG_INPUT, font=(FONT_FAMILY, 11)).pack(side="left", padx=(0, 8))
        self.password_entry = tk.Entry(
            pw_wrap, font=FONT_MD, bg=BG_INPUT, fg=TEXT_GRAY,
            insertbackground=PRIMARY, relief="flat", bd=0,
        )
        self.password_entry.pack(side="left", fill="x", expand=True)
        self.password_entry.insert(0, "password")
        self.password_entry.bind("<FocusIn>",  self._clear_pw_placeholder)
        self.password_entry.bind("<FocusOut>", self._restore_pw_placeholder)
        self.password_entry.bind("<Return>", lambda _e: self.validate_credentials())

        # Role toggle
        tk.Label(card, text="I AM A...", font=(FONT_FAMILY, 8, "bold"),
                 bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(2, 6))
        toggle_row = tk.Frame(card, bg=BG_CARD)
        toggle_row.pack(fill="x")
        self.buyer_btn = tk.Button(
            toggle_row, text="Buyer", font=FONT_MD_BOLD,
            relief="flat", bd=0, padx=10, pady=10, cursor="hand2",
            command=lambda: self.toggle_role("Buyer"),
        )
        self.buyer_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.seller_btn = tk.Button(
            toggle_row, text="Seller", font=FONT_MD_BOLD,
            relief="flat", bd=0, padx=10, pady=10, cursor="hand2",
            command=lambda: self.toggle_role("Seller"),
        )
        self.seller_btn.pack(side="left", fill="x", expand=True)
        self._refresh_toggle()

        # Sign-in button
        tk.Button(
            card, text="SIGN IN  →", font=(FONT_FAMILY, 11, "bold"),
            bg=PRIMARY, fg="#FFFFFF",
            activebackground=PRIMARY_DARK, activeforeground="#FFFFFF",
            relief="flat", bd=0, padx=20, pady=12, cursor="hand2",
            command=self.validate_credentials,
        ).pack(fill="x", pady=(20, 0))

        # ── Sign up link — between Sign In and demo hints ─────────
        signup_row = tk.Frame(card, bg=BG_CARD)
        signup_row.pack(pady=(14, 0))
        tk.Label(signup_row, text="Don't have an account? ",
                 font=FONT_SM, bg=BG_CARD, fg=TEXT_GRAY).pack(side="left")
        signup_lbl = tk.Label(signup_row, text="Sign up",
                              font=(FONT_FAMILY, 9, "bold"),
                              bg=BG_CARD, fg=PRIMARY, cursor="hand2")
        signup_lbl.pack(side="left")
        signup_lbl.bind("<Button-1>", lambda e: self._open_signup())

        # ── Demo hints ────────────────────────────────────────────
        hint = tk.Frame(inner, bg=BG_DARK)
        hint.pack(fill="x", padx=22, pady=(14, 14))
        tk.Label(hint, text="Demo logins:",
                 font=(FONT_FAMILY, 8, "bold"), bg=BG_DARK, fg=ACCENT).pack(anchor="w")
        tk.Label(hint, text='Buyers  :  "simisola" | "tunde" | "bisi"  ·  pw: buy123',
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_GRAY).pack(anchor="w")
        tk.Label(hint, text='Sellers :  "alhaja spices" | "mama rashidat"  ·  pw: sell123',
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_GRAY).pack(anchor="w")
        tk.Label(hint, text='           "mama fish"     | "alhaji yakubu" | "alhaji musa" ',
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_GRAY).pack(anchor="w")
        tk.Label(hint, text='           "yam empire"     | "tuber house" ',
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_GRAY).pack(anchor="w")

    def _open_signup(self):
        SignUpWindow(self, self.on_login_success, self.data_manager)

    def toggle_role(self, role: str = None):
        if role:
            self.active_role = role
        else:
            self.active_role = "Seller" if self.active_role == "Buyer" else "Buyer"
        self._refresh_toggle()

    def validate_credentials(self):
        raw = self.username_entry.get().strip().lower()
        password = self.password_entry.get().strip()
        if password == "password":
            password = ""
        placeholder = 'username'
        if not raw or raw == placeholder.lower():
            messagebox.showwarning("Missing Username", "Please enter your username to continue.")
            return
        if not password:
            messagebox.showwarning("Missing Password", "Please enter your password to continue.")
            return
        role = self.active_role

        # Password check
        expected_pw = "buy123" if role == "Buyer" else "sell123"
        if password != expected_pw:
            messagebox.showerror(
                "Wrong Password",
                f"Incorrect password for {role} account.\n\nHint: {role} password is '{expected_pw}'",
            )
            return

        # Check registered users first
        if self.data_manager and role == "Buyer":
            users = self.data_manager._data.get("_users", {})
            if raw in users:
                business = users[raw].get("business_name", raw.title())
                self.on_login_success(raw, "Buyer", business)
                return

        BUYER_BUSINESSES = {
            "simisola": "Simisola Catering Services",
            "bisi":     "Bisi's Food Canteen",
            "tunde":    "Tunde's Kitchen",
        }
        if role == "Buyer" and raw in self.VALID_BUYERS:
            business = BUYER_BUSINESSES.get(raw, raw.title())
            self.on_login_success(raw, "Buyer", business)
        elif role == "Seller":
            matched = next((s for s in self.VALID_SELLERS if s == raw), None)
            if not matched:
                matched = next((s for s in self.VALID_SELLERS if s.startswith(raw.split()[0])), None)
            if matched:
                display = matched.title()
                self.on_login_success(display, "Seller", display)
            else:
                messagebox.showerror(
                    "Access Denied",
                    f"'{raw}' is not a registered handpicked seller.\n\n"
                    "Try: mama rashidat, alhaja spices, yam empire…",
                )
        else:
            messagebox.showerror(
                "Invalid Credentials",
                f"Username '{raw}' not recognised for role '{role}'.\n\n"
                "Buyers: simisola | tunde | bisi\nOr sign up for a new account.",
            )

    def _refresh_toggle(self):
        if self.active_role == "Buyer":
            self.buyer_btn.config(bg=PRIMARY,  fg="#FFFFFF",   activebackground=PRIMARY_DARK)
            self.seller_btn.config(bg=BG_INPUT, fg=TEXT_GRAY, activebackground=BG_CARD_ALT)
        else:
            self.buyer_btn.config(bg=BG_INPUT, fg=TEXT_GRAY, activebackground=BG_CARD_ALT)
            self.seller_btn.config(bg=ACCENT,  fg="#FFFFFF",  activebackground="#CC5500")

    def _clear_placeholder(self, _event):
        if self.username_entry.get() == 'username':
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(fg=TEXT_WHITE)

    def _restore_placeholder(self, _event):
        if not self.username_entry.get().strip():
            self.username_entry.insert(0, 'username')
            self.username_entry.config(fg=TEXT_GRAY)

    def _clear_pw_placeholder(self, _event):
        if self.password_entry.get() == 'password':
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(fg=TEXT_WHITE, show="•")

    def _restore_pw_placeholder(self, _event):
        if not self.password_entry.get().strip():
            self.password_entry.config(show="")
            self.password_entry.insert(0, 'password')
            self.password_entry.config(fg=TEXT_GRAY)


class SignUpWindow:

    def __init__(self, parent, on_success_callback, data_manager):
        self.on_success = on_success_callback
        self.data_manager = data_manager

        self.popup = tk.Toplevel(parent)
        self.popup.title("Sign Up — SourceDirect")
        self.popup.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.popup.resizable(False, False)
        self.popup.configure(bg=BG_DARK)
        self.popup.grab_set()
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self.popup, bg="#D0EAD8", padx=16, pady=20)
        hdr.pack(fill="x")
        tk.Button(hdr, text="← Back", font=FONT_SM_BOLD,
                  bg="#D0EAD8", fg=TEXT_GRAY, relief="flat", bd=0,
                  cursor="hand2", command=self.popup.destroy).pack(anchor="w")
        tk.Label(hdr, text="🌿", font=(FONT_FAMILY, 32), bg="#D0EAD8").pack()
        tk.Label(hdr, text="Create Account",
                 font=(FONT_FAMILY, 20, "bold"), bg="#D0EAD8", fg="#111111").pack()
        tk.Label(hdr, text="Join SourceDirect as a buyer",
                 font=FONT_SM, bg="#D0EAD8", fg="#555555").pack(pady=(4, 0))

        # Form card
        card = tk.Frame(self.popup, bg=BG_CARD, padx=28, pady=26)
        card.pack(fill="x", padx=22, pady=(24, 0))

        self.fields = {}
        field_defs = [
            ("USERNAME", "username", False),
            ("BUSINESS NAME", "e.g. Adeola Catering Services", False),
            ("PASSWORD", "", True),
            ("CONFIRM PASSWORD", "", True),
        ]

        for label, placeholder, is_pw in field_defs:
            tk.Label(card, text=label, font=(FONT_FAMILY, 8, "bold"),
                     bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(8, 0))
            wrap = tk.Frame(card, bg=BG_INPUT, padx=10, pady=8,
                            relief="solid", bd=1, highlightbackground=BORDER,
                            highlightthickness=1)
            wrap.pack(fill="x", pady=(4, 0))
            show = "" if not is_pw else "•"
            entry = tk.Entry(wrap, font=FONT_MD, bg=BG_INPUT, fg=TEXT_GRAY,
                             insertbackground=PRIMARY, relief="flat", bd=0,
                             show=show)
            entry.pack(fill="x", expand=True)
            if placeholder:
                entry.insert(0, placeholder)
                entry.bind("<FocusIn>", lambda e, en=entry, ph=placeholder: (
                    en.delete(0, tk.END) if en.get() == ph else None,
                    en.config(fg=TEXT_WHITE)
                ))
                entry.bind("<FocusOut>", lambda e, en=entry, ph=placeholder: (
                    en.insert(0, ph) if not en.get().strip() else None,
                    en.config(fg=TEXT_GRAY if not en.get().strip() else TEXT_WHITE)
                ))
            self.fields[label] = (entry, placeholder)

        tk.Button(
            card, text="SIGN UP  →", font=(FONT_FAMILY, 11, "bold"),
            bg=PRIMARY, fg="#FFFFFF",
            activebackground=PRIMARY_DARK, activeforeground="#FFFFFF",
            relief="flat", bd=0, pady=13, cursor="hand2",
            command=self._do_signup,
        ).pack(fill="x", pady=(24, 0))

        # Info
        info = tk.Frame(self.popup, bg=BG_DARK)
        info.pack(padx=22, pady=(14, 0), fill="x")
        tk.Label(info, text="Your account will be active immediately.",
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_GRAY).pack(anchor="w")
        tk.Label(info, text="Data resets when the app closes.",
                 font=FONT_XS, bg=BG_DARK, fg=TEXT_MUTED).pack(anchor="w")

    def _get_val(self, label):
        entry, placeholder = self.fields[label]
        val = entry.get().strip()
        return "" if val == placeholder else val

    def _do_signup(self):
        username = self._get_val("USERNAME").lower()
        business = self._get_val("BUSINESS NAME")
        password = self._get_val("PASSWORD")
        confirm  = self._get_val("CONFIRM PASSWORD")

        if not username:
            messagebox.showwarning("Missing Field", "Please enter a username."); return
        if not business:
            messagebox.showwarning("Missing Field", "Please enter your business name."); return
        if not password:
            messagebox.showwarning("Missing Field", "Please enter a password."); return
        if password != confirm:
            messagebox.showerror("Password Mismatch", "Passwords do not match."); return
        if len(password) < 4:
            messagebox.showwarning("Weak Password", "Password must be at least 4 characters."); return

        if self.data_manager:
            ok = self.data_manager.add_user(username, password, business)
            if not ok:
                messagebox.showerror("Username Taken", f"'{username}' is already registered."); return

        self.popup.destroy()
        self.on_success(username, "Buyer", business)
