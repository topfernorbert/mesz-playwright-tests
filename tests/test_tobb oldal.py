from playwright.sync_api import expect

def test_tobb_gomb(page):
    """Oldalakon átívelő teszt"""
    page.goto("https://practicesoftwaretesting.com",
              wait_until="domcontentloaded",
              timeout=60000)
    contact_button = page.locator('[data-test="nav-contact"]')
    expect(contact_button).to_be_visible()
    contact_button.click()
    expect(page).to_have_url("https://practicesoftwaretesting.com/contact")
    first_name = page.locator('[data-test="first-name"]')
    first_name.fill("Kiss")
    last_name = page.locator('[data-test="last-name"]')
    last_name.fill("Elemér")
    email = page.locator('[data-test="email"]')
    email.fill("losblancosrm@gmail.com")
    subject = page.locator("[data-test='subject']")
    subject.select_option("webmaster")
    message = page.locator('[data-test="message"]')
    message.fill("Ez egy teszt üzenet, amelyet az automatikus teszt küld.")
    send_button = page.locator('[data-test="contact-submit"]')
    send_button.click()
    success = page.locator("[role='alert']")
    expect(success).to_be_visible()
    expect(success).to_contain_text("Thanks for your message")
