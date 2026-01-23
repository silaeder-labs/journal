from playwright.sync_api import sync_playwright
import json
from pathlib import Path
import config

lessons_id = config.LESSONS_ID
lessons_name = config.LESSONS_NAME

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()
    
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent

    page.route(
        "**/*",
        lambda route, request:
            route.abort()
            if request.resource_type in ["image", "font", "stylesheet"]
            else route.continue_()
    )

    def is_needed(response):
        return (
            "api/ej/rating/v1/rank/class" in response.url
            and response.status == 200
        )

    for i in range(len(lessons_id)):
        print(lessons_name[i] + "(" + str(i+1) + "/" + str(len(lessons_id)) + ")")
        final_path = script_dir / "data" / (str(lessons_name[i]) + ".json")
        with page.expect_response(is_needed) as resp_info:
            page.goto("https://school.mos.ru/diary/marks/current-marks/?view=by_subject&subject_id=" + str(lessons_id[i]))

        response = resp_info.value
        data = response.json()

        with open(final_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    browser.close()
