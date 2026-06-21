from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def parse_quotes_api(raw_network_data):
    """Processes AJAX API JSON payloads for quotes data case profile"""
    standardized_data = []
    for response_packet in raw_network_data:
        quotes = response_packet.get("quotes", [])
        for q in quotes:
            standardized_data.append({
                "field_1": q.get("author", {}).get("name", "Unknown"),
                "field_2": q.get("text", "").replace("“", "").replace("”", ""),
                "field_3": ", ".join(q.get("tags", []))
            })
    logger.info(f"Parser pipeline: Extracted {len(standardized_data)} records from network storage.")
    return standardized_data


def parse_ecommerce_html(html_content):
    """Parses product grids structure out of the collected raw HTML markup"""
    standardized_data = []
    soup = BeautifulSoup(html_content, "html.parser")
    products = soup.select(".product")

    for product in products:
        title_el = product.select_one(".woocommerce-loop-product__title")
        price_el = product.select_one(".price")
        btn_el = product.select_one(".add_to_cart_button")

        title = title_el.text.strip() if title_el else "N/A"
        price = price_el.text.strip() if price_el else "N/A"
        sku = btn_el["data-product_sku"] if btn_el and btn_el.has_attr("data-product_sku") else "N/A"

        standardized_data.append({
            "field_1": title,
            "field_2": price,
            "field_3": f"SKU: {sku}"
        })
    logger.info(f"Parser pipeline: Compiled {len(standardized_data)} products from layout model structures.")
    return standardized_data