import asyncio
import logging
import config
from scraper import PlaywrightScraper
import parser
import export

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)


async def run_pipeline_for_case(case_name):
    logger.info(f"--- RUNNING AUTOMATION ENGINE (Active Profile: {case_name}) ---")

    # Принудительно устанавливаем текущий кейс в конфигурации
    config.CURRENT_CASE = case_name

    scraper = PlaywrightScraper()
    raw_data = None

    try:
        # Phase 1: Initialize browser session and run crawler tasks
        await scraper.start()
        raw_data = await scraper.navigate_and_extract()
    except Exception as e:
        logger.critical(f"Crawler session crashed for {case_name}: {e}", exc_info=True)
    finally:
        await scraper.close()

    if not raw_data:
        logger.error(f"No raw payloads fetched for {case_name}. Execution stopped.")
        return

    # Phase 2: Structural processing based on data profile requirements
    parsed_data = []
    if case_name == "quotes":
        parsed_data = parser.parse_quotes_api(raw_data)
    elif case_name == "ecommerce":
        parsed_data = parser.parse_ecommerce_html(raw_data)

    # Phase 3: Deliverables formatting and export execution
    if parsed_data:
        # Модуль export внутри себя автоматически вызовет новые функции config.get_output_...()
        export.export_data(parsed_data)
        logger.info(f"--- PIPELINE EXECUTION FOR '{case_name.upper()}' COMPLETED SUCCESSFULLY ---")
    else:
        logger.error(f"Data pipeline empty for {case_name}. Deliverables omitted.")


async def main():
    # Запускаем сбор данных последовательно для каждого кейса
    for case in ["quotes", "ecommerce"]:
        await run_pipeline_for_case(case)
        print("\n" + "=" * 50 + "\n")  # Визуальный разделитель в логах


if __name__ == "__main__":
    asyncio.run(main())