from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # обязательно False
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://school.mos.ru/")

    print("Войди в аккаунт вручную и открой дневник.")
    page.wait_for_url("**/diary/**", timeout=0)

    # сохраняем cookies + localStorage
    context.storage_state(path="auth.json")

    print("Сессия сохранена")
    browser.close()
