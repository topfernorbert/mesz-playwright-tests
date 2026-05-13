# -*- coding: utf-8 -*-
import pytest
from playwright.sync_api import sync_playwright, Page

BASE_URL = "https://mesz.nive.hu"


def wait_for_angular(page: Page):
    """Megvárja, hogy az Angular app-root tartalommal töltődjön be."""
    try:
        page.wait_for_function(
            "document.querySelector('app-root') && "
            "document.querySelector('app-root').children.length > 0",
            timeout=15000
        )
    except Exception:
        pass


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
        viewport={"width": 1280, "height": 800},
        locale="hu-HU",
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def homepage(page):
    """Megnyitja a főoldalt és megvárja az Angular betöltését."""
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
    wait_for_angular(page)
    return page
