import sys
import io
import tkinter as tk
from tkinter import messagebox

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
except AttributeError:
    pass

from modules.constants        import *
from modules.data_manager     import DataManager
from modules.auth_window      import AuthWindow
from modules.buyer_dashboard  import BuyerDashboard
from modules.seller_dashboard import SellerDashboard
from modules.detail_viewer    import DetailViewer


class SourceDirectApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SourceDirect")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self._center_window()

        # Shared services (in-memory; resets on close)
        self.data_manager  = DataManager()
        self.detail_viewer = DetailViewer()
        self._active_frame = None

        self.show_login()

    def show_login(self):
        self._clear_frame()
        frame = AuthWindow(self,
                           on_login_success_callback=self._on_login_success,
                           data_manager=self.data_manager)
        frame.pack(fill="both", expand=True)
        self._active_frame = frame

    def show_buyer_dashboard(self, username: str = "", business_name: str = ""):
        self._clear_frame()
        frame = BuyerDashboard(
            root_window=self,
            data_manager=self.data_manager,
            on_view_stock_callback=self._on_view_stock,
            business_name=business_name,
            username=username,
        )
        frame.pack(fill="both", expand=True)
        self._active_frame = frame

    def show_seller_dashboard(self, seller_name: str):
        self._clear_frame()
        frame = SellerDashboard(
            root_window=self,
            seller_name=seller_name,
            data_manager=self.data_manager,
            on_logout_callback=self.show_login,
        )
        frame.pack(fill="both", expand=True)
        self._active_frame = frame

    def _on_login_success(self, username: str, role: str, business_name: str = ""):
        if role == "Buyer":
            self.show_buyer_dashboard(username=username, business_name=business_name)
        elif role == "Seller":
            self.show_seller_dashboard(username)
        else:
            messagebox.showerror("Routing Error", f"Unknown role: '{role}'.")

    def _on_view_stock(self, seller_name: str, inventory_dict: dict):
        self.detail_viewer.launch_storefront_popup(self, seller_name, inventory_dict)

    def _clear_frame(self):
        if self._active_frame is not None:
            try:
                self._active_frame.destroy()
            except tk.TclError:
                pass
            self._active_frame = None

    def _center_window(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{(sw-APP_WIDTH)//2}+{(sh-APP_HEIGHT)//2}")


if __name__ == "__main__":
    app = SourceDirectApp()
    app.mainloop()
    print("[App] Application closed.")
