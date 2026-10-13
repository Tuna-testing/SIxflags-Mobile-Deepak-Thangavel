import re

# Read current html_hooks.py
with open("/Users/thangaveltuna/Ready to run /Antigravity/hooks/html_hooks.py", "r") as f:
    current_content = f.read()

# Read SFMOB's pytest_html_report.py
with open("/Users/thangaveltuna/.gemini/antigravity/brain/4970b165-3fb1-4298-a8eb-532d4fe677a3/scratch/SFMOB_AUTO/core/reporting/pytest_html_report.py", "r") as f:
    sfmob_content = f.read()

# Extract the full pytest_html_results_summary from SFMOB
sfmob_summary_match = re.search(r'(def pytest_html_results_summary\(prefix, summary, postfix\):.*?)\n\n\n@', sfmob_content, re.DOTALL)
if not sfmob_summary_match:
    print("Could not find sfmob summary")
    exit(1)
sfmob_summary_code = sfmob_summary_match.group(1)

# Modify the SFMOB summary to include the user's custom title at the top
sfmob_summary_code = sfmob_summary_code.replace(
    'prefix.extend(',
    'prefix.extend([f"<h2>Test Execution Summary - {datetime.now().strftime(\'%Y-%m-%d %H:%M:%S\')}</h2>"])\n    prefix.extend(',
    1
)

# Replace the pytest_html_results_summary in html_hooks.py
current_summary_match = re.search(r'def pytest_html_results_summary\(prefix, summary, postfix\):.*?(?=\n\ndef pytest_html_results_table_header)', current_content, re.DOTALL)
if not current_summary_match:
    print("Could not find current summary")
    exit(1)

new_content = current_content.replace(current_summary_match.group(0), sfmob_summary_code)

# Add pytest_html import for extras if missing
if "from pytest_html import extras" not in new_content:
    new_content = new_content.replace("import pytest", "import pytest\nfrom pytest_html import extras\nimport base64")

# Update pytest_runtest_makereport to append the image to extras for the JS modal to pick up
image_extra_code = """
        if report.failed and getattr(item, 'failed_step_png', None):
            try:
                import base64
                encoded = base64.b64encode(item.failed_step_png).decode("ascii")
                report.extras = getattr(report, "extras", [])
                report.extras.append(extras.image(f"data:image/png;base64,{encoded}", name="Failure screenshot"))
            except Exception:
                pass
"""

# Inject before embed_screenshot_in_html
new_content = new_content.replace("embed_screenshot_in_html(report, item, pytest_html)", "embed_screenshot_in_html(report, item, pytest_html)\n" + image_extra_code)

with open("/Users/thangaveltuna/Ready to run /Antigravity/hooks/html_hooks.py", "w") as f:
    f.write(new_content)

print("Successfully patched html_hooks.py")
