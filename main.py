import asyncio
import logging
import config
from scraper import PlaywrightScraper
import parser
import export

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)


async def main():
    logger.info(f"--- RUNNING AUTOMATION ENGINE (Active Profile: {config.CURRENT_CASE}) ---")

    scraper = PlaywrightScraper()
    raw_data = None

    try:
        # Phase 1: Initialize browser session and run crawler tasks
        await scraper.start()
        raw_data = await scraper.navigate_and_extract()
    except Exception as e:
        logger.critical(f"Crawler session crashed: {e}", exc_info=True)
    finally:
        await scraper.close()

    if not raw_data:
        logger.error("No raw payloads fetched. Execution stopped.")
        return

    # Phase 2: Structural processing based on data profile requirements
    parsed_data = []
    if config.CURRENT_CASE == "quotes":
        parsed_data = parser.parse_quotes_api(raw_data)
    elif config.CURRENT_CASE == "ecommerce":
        parsed_data = parser.parse_ecommerce_html(raw_data)

    # Phase 3: Deliverables formatting and export execution
    if parsed_data:
        export.export_data(parsed_data)
        logger.info("--- PIPELINE EXECUTION COMPLETED SUCCESSFULLY ---")
    else:
        logger.error("Data pipeline empty. Deliverables omitted.")


if __name__ == "__main__":
    asyncio.run(main())