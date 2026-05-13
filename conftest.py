import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://practicesoftwaretesting.com"


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance):
    context = browser_instance.new_context(
        viewport={"width": 1280, "height": 800}
    )
    page = context.new_page()
    yield page
    context.close()
