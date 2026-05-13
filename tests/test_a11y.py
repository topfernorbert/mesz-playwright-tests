import pytest
from playwright.sync_api import expect


def test_slider_buttons_have_aria_label(homepage):
    """
    A slider chevron gombjain van aria-label.
    WCAG 2.1 — 1.1.1 Non-text Content (Level A)
    """
    icon_buttons = homepage.locator(
        "button:has(.material-icons:text('chevron_right')), "
        "button:has(.material-icons:text('chevron_left'))"
    )
    count = icon_buttons.count()
    assert count > 0, "Slider gombok nem találhatók az oldalon!"

    for i in range(count):
        btn = icon_buttons.nth(i)
        aria_label = btn.get_attribute("aria-label")
        aria_labelledby = btn.get_attribute("aria-labelledby")
        assert aria_label or aria_labelledby, (
            f"A {i+1}. slider gombnak nincs aria-label! "
            f"HTML: {btn.evaluate('el => el.outerHTML')}"
        )


def test_images_have_alt_text(homepage):
    """
    Minden képnek van alt attribútuma.
    WCAG 2.1 — 1.1.1 Non-text Content (Level A)
    """
    images = homepage.locator("img")
    count = images.count()
    assert count > 0, "Nem található kép az oldalon!"

    missing_alt = []
    for i in range(count):
        img = images.nth(i)
        alt = img.get_attribute("alt")
        src = img.get_attribute("src") or "(ismeretlen)"
        if alt is None:
            missing_alt.append(f"  - Hiányzó alt: {src}")

    assert not missing_alt, (
        f"Hiányzó alt attribútum ({len(missing_alt)} kép):\n"
        + "\n".join(missing_alt)
    )


def test_nav_links_keyboard_accessible(homepage):
    """
    A menü linkek Tab billentyűvel bejárhatók.
    WCAG 2.1 — 2.1.1 Keyboard (Level A)
    """
    homepage.keyboard.press("Tab")

    focused = homepage.evaluate("document.activeElement.tagName")
    assert focused in ("A", "BUTTON", "INPUT"), (
        f"Az első Tab után nem fókuszálható elemre ugrott: {focused}"
    )

    focused_elements = set()
    for _ in range(10):
        homepage.keyboard.press("Tab")
        tag = homepage.evaluate("document.activeElement.tagName")
        focused_elements.add(tag)

    assert "A" in focused_elements or "BUTTON" in focused_elements, (
        "Tab navigáció során nem kerültek fókuszba navigációs elemek!"
    )


def test_hero_image_has_alt(homepage):
    """A hero szekció képének van alt szövege."""
    images = homepage.locator(
        "[class*='hero'] img, [class*='slider'] img, [class*='carousel'] img"
    )
    count = images.count()
    assert count > 0, "Hero kép nem található!"

    for i in range(count):
        img = images.nth(i)
        alt = img.get_attribute("alt")
        assert alt is not None, "Hiányzó alt attribútum!"
        assert alt.strip() != "", "Üres alt szöveg!"


def test_page_loads_within_3_seconds(page):
    """Az oldal 3 másodpercen belül interaktív állapotba kerül."""
    import time
    start = time.time()

    page.goto("https://mesz.nive.hu")
    page.wait_for_function(
        "document.querySelector('app-root').children.length > 0"
    )

    elapsed = time.time() - start
    assert elapsed < 3.0, (
        f"Az oldal {elapsed:.1f}mp alatt töltött be — "
        f"ez meghaladja a 3mp határt!"
    )


def test_hero_images_load_successfully(homepage):
    """A hero szekció képei sikeresen betöltöttek."""
    images = homepage.locator(
        "[class*='hero'] img, [class*='slider'] img, [class*='carousel'] img"
    )
    count = images.count()
    assert count > 0, "Hero szekció képei nem találhatók!"

    broken = []
    for i in range(count):
        img = images.nth(i)
        loaded = img.evaluate(
            "el => el.complete && el.naturalWidth > 0"
        )
        if not loaded:
            src = img.get_attribute("src") or "(ismeretlen)"
            broken.append(src)

    assert not broken, (
        f"Törött képek ({len(broken)} db):\n" + "\n".join(broken)
    )
