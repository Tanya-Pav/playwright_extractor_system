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

# Текущий активный кейс
CURRENT_CASE = "quotes"

# Вместо property делаем функции, которые будут отдавать правильный Path по требованию
def get_output_json():
    return DATA_DIR / f"extracted_{CURRENT_CASE}.json"

def get_output_csv():
    return DATA_DIR / f"extracted_{CURRENT_CASE}.csv"

def get_output_xlsx():
    return DATA_DIR / f"extracted_{CURRENT_CASE}.xlsx"

# Network and browser settings
TIMEOUT = 30000
HEADLESS = False