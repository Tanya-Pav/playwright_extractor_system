# Asynchronous Web Automation & Data Extraction System

A production-ready, asynchronous data extraction pipeline built with **Python**, **Playwright**, and **BeautifulSoup4**, featuring an interactive executive delivery dashboard in **Streamlit**.

Built specifically to demonstrate robust handling of modern web architectures, including infinite scroll, dynamic JavaScript rendering, and background API network interception.

---

## 🚀 Key Features & Architecture

This repository demonstrates a **2-in-1 architecture** designed to handle two completely different web data harvesting scenarios using a unified core configuration:

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
git clone [https://github.com/yourusername/playwright_extractor_system.git](https://github.com/yourusername/playwright_extractor_system.git)
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

3. **Configure the Extraction Mode:**
Open `config.py` and toggle between modes:
```python
CURRENT_CASE = "quotes"  # or "ecommerce"
```

4. **Execute the Pipeline & Launch the Dashboard:**
```bash
```bash
python main.py
streamlit run dashboard.py
```

---

## 📊 Data Pipeline Deliverables
The system cleanses, normalizes, and automatically flattens data into three concurrent formats saved into the `/data` directory:
* `extracted_data.json` — Pre-formatted for NoSQL database ingestion.
* `extracted_data.csv` — Optimized for automated ETL pipeline data ingestion.
* `extracted_data.xlsx` — Formatted executive summaries with customized columns.