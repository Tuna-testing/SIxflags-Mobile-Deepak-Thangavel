# utils/report_helpers.py
import base64
import allure


def attach_step_screenshot(
    driver, name: str, node, cache_attr: str = "latest_step_png"
):
    """Captures screenshot, attaches it to Allure step, and caches PNG on Pytest node."""
    if not driver:
        return
    try:
        screenshot_png = driver.get_screenshot_as_png()

        # 1. Attach directly inside active Allure Gherkin step
        with allure.step(f"Visual Evidence: {name}"):
            allure.attach(
                screenshot_png,
                name=name,
                attachment_type=allure.attachment_type.PNG,
            )

        # 2. Cache on Pytest item node for HTML report rendering
        setattr(node, cache_attr, screenshot_png)
    except Exception as e:
        print(f"[WARNING] Screenshot capture failed for '{name}': {e}")


def embed_screenshot_in_html(report, item, pytest_html):
    """Retrieves cached screenshot bytes and embeds image snippet in pytest-html v4.2+."""
    try:
        # Grab cached PNG bytes (prioritize failure, fallback to step success)
        img_bytes: bytes | None = getattr(
            item,
            "failed_step_png",
            getattr(
                item,
                "failed_screenshot_png",
                getattr(
                    item,
                    "latest_step_png",
                    getattr(item, "success_screenshot_png", None),
                ),
            ),
        )

        if isinstance(img_bytes, bytes):
            b64_encoded = base64.b64encode(img_bytes).decode("utf-8")
            html_snippet = (
                f'<div style="margin-top:10px;">'
                f'<strong>Visual Evidence:</strong><br/>'
                f'<img src="data:image/png;base64,{b64_encoded}" '
                f'alt="screenshot" style="width:340px;height:auto;border:2px solid #333;border-radius:4px;margin-top:5px;cursor:pointer;" '
                f'onclick="window.open(this.src)"/></div>'
            )

            # pytest-html v4.2+ compatibility
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.html(html_snippet))
            report.extras = extras

    except Exception as e:
        print(f"[WARNING] Could not attach screenshot to HTML report: {e}")