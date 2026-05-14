def test_oldal_betolt(page):
    """Az oldal betölt."""
    page.goto("https://practicesoftwaretesting.com",
              wait_until="domcontentloaded",
              timeout=60000)

    assert "Practice" in page.title()


def test_signin_link(page):
    """A Sign in link látható és kattintható."""
    page.goto("https://practicesoftwaretesting.com",
              wait_until="domcontentloaded",
              timeout=60000)

    # DOM alapján: data-test="nav-sign-in"
    signin_link = page.locator("[data-test='nav-sign-in']")
    assert signin_link.is_visible()

    signin_link.click()
    assert "/auth/login" in page.url
