import pandas as pd
import config
import logging

logger = logging.getLogger(__name__)

def export_data(parsed_data):
    """
    Форматирует собранные данные в DataFrame и экспортирует их
    в изолированные файлы в зависимости от активного CURRENT_CASE.
    """
    if not parsed_data:
        logger.warning("No data passed to export pipeline.")
        return

    # Создаем DataFrame из спарсенного списка словарей
    df = pd.DataFrame(parsed_data)

    try:
        # 1. Экспорт в CSV (Вызываем динамическую функцию со скобками)
        csv_path = config.get_output_csv()
        df.to_csv(csv_path, index=False, encoding="utf-8")
        logger.info(f"Successfully exported CSV deliverable to: {csv_path.name}")

        # 2. Экспорт в Excel (Вызываем динамическую функцию со скобками)
        xlsx_path = config.get_output_xlsx()
        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Raw Data")
        logger.info(f"Successfully exported XLSX deliverable to: {xlsx_path.name}")

        # 3. Экспорт в JSON (при необходимости)
        json_path = config.get_output_json()
        df.to_json(json_path, orient="records", indent=4, force_ascii=False)
        logger.info(f"Successfully exported JSON deliverable to: {json_path.name}")

    except Exception as e:
        logger.error(f"Failed to write deliverables to disk: {e}", exc_info=True)