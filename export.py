import json
import csv
import pandas as pd
import logging
import config

logger = logging.getLogger(__name__)

def export_data(data):
    """Saves standardized records to disk in JSON, CSV, and Excel formats"""
    if not data:
        logger.warning("Export pipeline aborted: dataset is empty.")
        return

    # 1. JSON Serialization
    try:
        with open(config.OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"JSON export completed successfully: {config.OUTPUT_JSON.name}")
    except Exception as e:
        logger.error(f"JSON writing failure: {e}")

    # 2. CSV Generation
    try:
        if data:
            keys = data[0].keys()
            with open(config.OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            logger.info(f"CSV export completed successfully: {config.OUTPUT_CSV.name}")
    except Exception as e:
        logger.error(f"CSV writing failure: {e}")

    # 3. Excel Report Building
    try:
        df = pd.DataFrame(data)
        # Apply structured corporate naming headers
        df.columns = ["Name / Title", "Content / Price", "Metadata / SKU"]
        df.to_excel(config.OUTPUT_XLSX, index=False, engine="openpyxl")
        logger.info(f"Excel export completed successfully: {config.OUTPUT_XLSX.name}")
    except Exception as e:
        logger.error(f"Excel writing failure: {e}")