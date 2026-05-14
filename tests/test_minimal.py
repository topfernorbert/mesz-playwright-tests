def test_oldal_betolt(page):
    """Az oldal betölt."""
    page.goto("https://practicesoftwaretesting.com",
              wait_until="domcontentloaded",
              timeout=60000)

    assert "Practice" in page.title()


def test_signin_link(page):
    """A Sign in link látható és kattintható."""
    from playwright.sync_api import expect

    page.goto("https://practicesoftwaretesting.com",
              wait_until="domcontentloaded",
              timeout=60000)

    signin_link = page.locator("[data-test='nav-sign-in']")

    # expect() automatikusan vár — ez a helyes Playwright módszer
    expect(signin_link).to_be_visible()

    signin_link.click()
    expect(page).to_have_url("https://practicesoftwaretesting.com/auth/login")
