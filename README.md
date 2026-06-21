# Asynchronous Web Automation & Data Extraction System

A production-ready, asynchronous data extraction pipeline built with **Python**, **Playwright**, and **BeautifulSoup4**, featuring an interactive executive delivery dashboard in **Streamlit**.

Built specifically to demonstrate robust handling of modern web architectures, including infinite scroll, dynamic JavaScript rendering, and background API network interception.

---

## 🚀 Key Features & Architecture

This repository demonstrates a unified architecture designed to handle two completely different web data harvesting scenarios in a single execution loop:

### ⚡ Core Case: Advanced Network Interception (`quotes`)
* **Target:** Dynamic JS-rendered application with infinite scroll (`https://quotes.toscrape.com/scroll`).
* **Methodology:** Asynchronously monitors the browser's network layer (`page.on("response")`), intercepts background AJAX/Fetch JSON packets, and extracts raw data without relying on heavy DOM parsing.
* **Benefit:** Maximum execution speed, immune to UI frontend layout updates.

### 🛒 Complementary Case: E-Commerce DOM Scraping (`ecommerce`)
* **Target:** Standard WooCommerce store layout (`https://scrapeme.live/shop/`).
* **Methodology:** Implements explicit smart waits (`wait_for_selector`) to guarantee full content hydration, extracts raw HTML, and compiles structured product fields (Titles, Prices, SKUs) via CSS selectors.

---

## 🛠️ Technical Stack

* **Core Engine:** Playwright (Async API)
* **HTML Parsing:** BeautifulSoup4 (LXML Engine)
* **Data Engineering:** Pandas, OpenPyxl
* **Visualization Layer:** Streamlit (Custom Aesthetic UI)

---

## 📦 Installation & Quick Start

1. **Clone the repository:**
```bash
git clone [https://github.com/Tanya-Pav/playwright_extractor_system.git](https://github.com/Tanya-Pav/playwright_extractor_system.git)
cd playwright_extractor_system
```

2. **Set up Virtual Environment & Install Dependencies:**
```bash
python -m venv .venv
```

* **On Windows:**
```bash
.venv\Scripts\activate
```

* **On macOS/Linux:**
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
playwright install
```

3. **Execute the Automated Pipeline & Launch the Dashboard:**
```bash
# Runs both extraction profiles sequentially without manual toggling
python main.py

# Launches the interactive visual control panel
streamlit run dashboard.py
```

---

## 📊 Data Pipeline Deliverables
The engine isolates profiles, cleanses data, and flattens datasets into concurrent formats stored securely inside the `/data` directory:
* `extracted_quotes.xlsx / .csv` — API intercepted data payload (Author, Quotes, Tags).
* `extracted_ecommerce.xlsx / .csv` — Type-casted and cleansed market product feeds.