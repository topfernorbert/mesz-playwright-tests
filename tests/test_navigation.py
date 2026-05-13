import pytest
from playwright.sync_api import expect

MENU_ITEMS = ["HÍREK", "DOKUMENTUMTÁR", "GALÉRIA", "KAPCSOLAT", "GYIK"]


@pytest.mark.smoke
@pytest.mark.parametrize("menu_item", MENU_ITEMS)
def test_menu_link_navigates(homepage, menu_item):
    """Minden menüpont kattintható és nem 404-et ad."""
    homepage.get_by_role("link", name=menu_item).click()
    homepage.wait_for_load_state("networkidle")

    assert "404" not in homepage.title()
    assert "404" not in homepage.url


@pytest.mark.smoke
@pytest.mark.parametrize("dropdown_name", ["BEMUTATKOZÁS", "KOMPONENSEK"])
def test_dropdown_menu_opens(homepage, dropdown_name):
    """A nyíl ikont tartalmazó menüpontok legördülő panelt nyitnak."""
    homepage.get_by_role("button", name=dropdown_name).click()

    dropdown_panel = homepage.locator("[role='menu'], mat-menu, .mat-mdc-menu-panel")
    expect(dropdown_panel).to_be_visible()

    menu_items = homepage.locator("[role='menuitem']")
    expect(menu_items.first).to_be_visible()


@pytest.mark.smoke
def test_logo_navigates_to_homepage(page):
    """Aloldalról a logóra kattintva visszajutunk a főoldalra."""
    page.goto("https://mesz.nive.hu/hirek")
    page.wait_for_load_state("networkidle")

    page.locator("mat-toolbar img, .logo, header a img").first.click()
    page.wait_for_url("https://mesz.nive.hu/")

    assert page.url == "https://mesz.nive.hu/"


def test_page_title_contains_brand(homepage):
    """Az oldal title-je tartalmazza a márkanevet."""
    expect(homepage).to_have_title("Mérés Értékelés Szakképzés")


def test_no_horizontal_scroll_on_mobile(browser_instance):
    """375px szélességen nincs vízszintes túlcsordulás."""
    context = browser_instance.new_context(
        viewport={"width": 375, "height": 812}
    )
    page = context.new_page()
    page.goto("https://mesz.nive.hu")
    page.wait_for_load_state("networkidle")

    scroll_width = page.evaluate("document.documentElement.scrollWidth")
    viewport_width = page.evaluate("window.innerWidth")
    context.close()

    assert scroll_width <= viewport_width, (
        f"Vízszintes scroll jelenik meg: "
        f"scrollWidth={scroll_width}px > innerWidth={viewport_width}px"
    )
