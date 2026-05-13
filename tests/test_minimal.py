def test_oldal_betolt(page):
    """Az oldal betölt és a title helyes."""
    page.goto(
        "https://mesz.nive.hu",
        wait_until="domcontentloaded",
        timeout=60000
    )
    assert "Mérés" in page.title()


def test_hirek_link(page):
    """A Hírek link látható és kattintható."""
    page.goto(
        "https://mesz.nive.hu",
        wait_until="domcontentloaded",
        timeout=60000
    )

    # DOM alapján: <a class="nav-link" href="/hirek">Hírek</a>
    hirek_link = page.locator("a.nav-link[href='/hirek']")
    assert hirek_link.is_visible()

    hirek_link.click()
    page.wait_for_url("**/hirek**", timeout=30000)
    assert "hirek" in page.url
