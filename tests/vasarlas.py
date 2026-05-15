from playwright.sync_api import expect

def test_vasarlas(page):
    """Vásárlás tesztelése"""
    page.goto("https://practicesoftwaretesting.com",
              wait_until="domcontentloaded",
              timeout=60000)
    page.locator('[class="card-img-top"]').click()
    expect(page.locator('[id="btn-add-to-cart"]')).to_be_visible()
    page.locator('[id="btn-add-to-cart"]').click()
    expect(page.locator('[id="toast-container"]')).to_be_visible()
    
