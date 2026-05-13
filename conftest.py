import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://mesz.nive.hu"


def wait_for_angular(page):
    """Megvárja, hogy az Angular app-root tartalommal töltődjön be."""
    page.wait_for_function(
        "document.querySelector('app-root') && "
        "document.querySelector('app-root').children.length > 0"
    )


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance):
    context = browser_instance.new_context(
        viewport={"width": 1280, "height": 800},
        locale="hu-HU",
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def homepage(page):
    """Megnyitja a főoldalt és megvárja az Angular betöltését."""
    page.goto(BASE_URL)
    wait_for_angular(page)
    return page
