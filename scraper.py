import asyncio
import logging
from playwright.async_api import async_playwright, Response
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)


class PlaywrightScraper:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.intercepted_data = []

    async def _handle_response(self, response: Response):
        """Asynchronous callback handler to capture explicit back-end AJAX requests"""
        if config.CURRENT_CASE == "quotes" and "api/quotes" in response.url:
            if response.status == 200:
                try:
                    data = await response.json()
                    logger.info(f"Network Interceptor caught API payload from: {response.url}")
                    self.intercepted_data.append(data)
                except Exception as e:
                    logger.error(f"Failed to read JSON network buffer: {e}")

    async def start(self):
        """Launches safe sandbox browser session and sets hooks infrastructure"""
        logger.info("Initializing Playwright subsystem...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=config.HEADLESS)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        self.page = await self.context.new_page()

        # Connect network events listener
        self.page.on("response", self._handle_response)

    async def navigate_and_extract(self):
        """Executes operational page behavioral flow dependent on case parameters"""
        case_config = config.CASES[config.CURRENT_CASE]
        url = case_config["url"]

        logger.info(f"Navigating to processing endpoint ({config.CURRENT_CASE}): {url}")
        await self.page.goto(url, wait_until="networkidle")

        if config.CURRENT_CASE == "quotes":
            # Trigger lazy load items via scrolling actions loop
            for i in range(5):
                logger.info(f"Scrolling view viewport down... Step {i + 1}/5")
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await self.page.wait_for_timeout(1500)
            return self.intercepted_data

        elif config.CURRENT_CASE == "ecommerce":
            logger.info("Waiting for data catalog containers markup to render...")
            await self.page.wait_for_selector(".products", timeout=config.TIMEOUT)
            return await self.page.content()

    async def close(self):
        """Gracefully tears down all browser engines and sessions contexts"""
        if self.browser:
            await self.browser.close()
            await self.playwright.stop()
            logger.info("Playwright active session finalized cleanly.")