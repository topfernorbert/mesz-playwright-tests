from playwright.sync_api import expect


def test_home(page):
    """Oldal betöltése sikeres."""
    page.goto("https://practicesoftwaretesting.com",
              wait_until="domcontentloaded",
              timeout=60000)
    assert "Practice" in page.title()


def test_login_button(page):
    """Login gomb kattintható."""
    page.goto("https://practicesoftwaretesting.com",
              wait_until="domcontentloaded",
              timeout=60000)

    login_button = page.locator("[data-test='nav-sign-in']")
    expect(login_button).to_be_visible()
    login_button.click()
    expect(page).to_have_url("https://practicesoftwaretesting.com/auth/login")
