from pathlib import Path

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Target workflows configuration
CASES = {
    "quotes": {
        "url": "https://quotes.toscrape.com/scroll",
        "type": "api_interception"
    },
    "ecommerce": {
        "url": "https://scrapeme.live/shop/",
        "type": "html_dom"
    }
}


CURRENT_CASE = "quotes"

# Network and browser settings
TIMEOUT = 30000
HEADLESS = False

# Output formats configuration
OUTPUT_JSON = DATA_DIR / "extracted_data.json"
OUTPUT_CSV = DATA_DIR / "extracted_data.csv"
OUTPUT_XLSX = DATA_DIR / "extracted_data.xlsx"