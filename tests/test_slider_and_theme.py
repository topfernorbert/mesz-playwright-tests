import pytest
from playwright.sync_api import expect


def _get_visible_slide_text(page) -> str:
    """Visszaadja az éppen látható slider kártya h2 szövegét."""
    candidates = page.locator(
        "[class*='slide'] h2, [class*='carousel'] h2, [class*='hero'] h2"
    )
    for i in range(candidates.count()):
        el = candidates.nth(i)
        if el.is_visible():
            return el.inner_text()
    return ""


def _click_next(page):
    page.locator(
        "button[aria-label*='next'], "
        "button[aria-label*='következő'], "
        "button:has(.material-icons:text('chevron_right'))"
    ).first.click()
    page.wait_for_timeout(600)


def _click_prev(page):
    page.locator(
        "button[aria-label*='prev'], "
        "button[aria-label*='előző'], "
        "button:has(.material-icons:text('chevron_left'))"
    ).first.click()
    page.wait_for_timeout(600)


@pytest.mark.smoke
def test_slider_next_changes_slide(homepage):
    """A jobb nyíl gomb a következő diára vált."""
    initial = _get_visible_slide_text(homepage)
    _click_next(homepage)
    current = _get_visible_slide_text(homepage)
    assert current != initial, (
        f"A slider nem lépett előre. Mindkét dia szövege: '{initial}'"
    )


def test_slider_prev_changes_slide(homepage):
    """A bal nyíl gomb az előző diára vált."""
    _click_next(homepage)
    after_next = _get_visible_slide_text(homepage)
    _click_prev(homepage)
    after_prev = _get_visible_slide_text(homepage)
    assert after_prev != after_next, "A bal nyíl nem lépett vissza!"


def test_slider_full_cycle(homepage):
    """Előre majd vissza → visszakerülünk az eredeti diára."""
    initial = _get_visible_slide_text(homepage)
    _click_next(homepage)
    _click_prev(homepage)
    returned = _get_visible_slide_text(homepage)
    assert returned == initial, (
        f"Nem tértünk vissza az eredeti diára. "
        f"Várt: '{initial}', kapott: '{returned}'"
    )


def test_slider_buttons_visible(homepage):
    """Mindkét slider nyíl gomb látható az oldalon."""
    next_btn = homepage.locator(
        "button:has(.material-icons:text('chevron_right'))"
    ).first
    prev_btn = homepage.locator(
        "button:has(.material-icons:text('chevron_left'))"
    ).first
    expect(next_btn).to_be_visible()
    expect(prev_btn).to_be_visible()


@pytest.mark.smoke
def test_dark_mode_toggle_activates(homepage):
    """A témaváltó gomb dark mode-ba kapcsolja az oldalt."""
    homepage.locator(
        "button:has(.material-icons:text('dark_mode')), "
        "button:has(.material-icons:text('nightlight'))"
    ).first.click()
    homepage.wait_for_timeout(400)

    is_dark = homepage.evaluate("""
        document.documentElement.classList.contains('dark') ||
        document.body.classList.contains('dark') ||
        document.documentElement.getAttribute('data-theme') === 'dark' ||
        getComputedStyle(document.documentElement)
            .getPropertyValue('color-scheme').trim() === 'dark'
    """)
    assert is_dark, "Dark mode nem aktiválódott!"


def test_dark_mode_persists_after_reload(homepage):
    """Dark mode megmarad oldal újratöltés után."""
    homepage.locator(
        "button:has(.material-icons:text('dark_mode')), "
        "button:has(.material-icons:text('nightlight'))"
    ).first.click()
    homepage.wait_for_timeout(400)
    homepage.reload()
    homepage.wait_for_function(
        "document.querySelector('app-root').children.length > 0"
    )
    is_dark = homepage.evaluate("""
        document.documentElement.classList.contains('dark') ||
        document.body.classList.contains('dark') ||
        localStorage.getItem('theme') === 'dark' ||
        localStorage.getItem('darkMode') === 'true'
    """)
    assert is_dark, "Dark mode nem maradt meg újratöltés után!"
