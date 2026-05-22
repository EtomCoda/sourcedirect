# SourceDirect 🌿

> **Bulk market supply platform linking 11 handpicked sellers  with large-scale food stakeholders.**

---

## 🚀 Quick Start

```bash
# No pip installs needed — pure Python stdlib
python main.py
```

### Demo Login Credentials

| Role   | Username Examples                                  |
|--------|----------------------------------------------------|
| Buyer  | `buyer`, `restaurant`, `school`, `cafeteria`       |
| Seller | `mama chioma`, `uncle emeka`, `aunty bola`, `chief okorie`, `mr. tunde` … |

---

## 📁 Project Structure

```
sourcedirect/
├── main.py                      ← Master orchestrator (SourceDirectApp)
├── market_data.json             ← Auto-generated on first run
├── requirements.txt
└── modules/
    ├── constants.py             ← Design system (colors, fonts)
    ├── data_manager.py          ← Member 1: JSON persistence (11 sellers)
    ├── auth_window.py           ← Member 2: Login + role toggle
    ├── buyer_dashboard.py       ← Member 3: Buyer viewport + canvas
    ├── catalog_components.py    ← Member 4: Grid card builder
    ├── list_row_components.py   ← Member 5: Row list builder
    ├── seller_dashboard.py      ← Member 6: Seller inventory console
    └── detail_viewer.py         ← Member 7: Popup + invoice calculator
```

---

## 👥 Team Module Assignments

| Member | Module File              | Class                | Responsibility                   |
|--------|--------------------------|----------------------|----------------------------------|
| 1      | `data_manager.py`        | `DataManager`        | JSON persistence for 11 sellers  |
| 2      | `auth_window.py`         | `AuthWindow`         | Login screen + role toggle       |
| 3      | `buyer_dashboard.py`     | `BuyerDashboard`     | Buyer UI + scrollable canvas     |
| 4      | `catalog_components.py`  | `CatalogComponents`  | Seller & product card builder    |
| 5      | `list_row_components.py` | `ListRowComponents`  | Low-cost & availability rows     |
| 6      | `seller_dashboard.py`    | `SellerDashboard`    | Inventory editor console         |
| 7      | `detail_viewer.py`       | `DetailViewer`       | Storefront popup + bulk invoice  |

---

## ✨ Features

- 🔐 **Authentication** — Buyer / Seller role toggle with credential validation
- 🛒 **Buyer Dashboard** — Scrollable seller cards, product grid, category filter
- 📋 **Seller Console** — Edit live prices and stock counts, saved to JSON
- 🏪 **Storefront Popup** — Full product catalog view in a modal window
- 🧾 **Bulk Invoice Calculator** — Auto-applies 5–12% bulk discounts for schools/cafeterias
- ⚡ **Low-Cost Alerts** — Critical stock indicators with red danger badges
- 🟢 **Availability Rows** — Real-time seller online status indicators
- 💾 **JSON Persistence** — All data stored in `market_data.json` (auto-seeded)

---

## 🛠 Technical Stack

- **Language**: Python 3.x (pure stdlib)
- **GUI**: `tkinter` + `ttk` (standard library only)
- **Paradigm**: Strictly OOP — each module is a class with `__init__` + methods
- **Persistence**: Local JSON file (`market_data.json`)
- **Architecture**: 7-member modular block layout

---

## 📍 Market Context

All 11 sellers are based at **Mile 12 Market, Lagos, Nigeria** — one of West Africa's largest fresh produce markets. SourceDirect acts as a smart middleman securing bulk pricing for:

- 🏫 Boarding schools
- 🍽️ Restaurants  
- 🏢 Corporate cafeterias
- 🍲 Catering businesses
