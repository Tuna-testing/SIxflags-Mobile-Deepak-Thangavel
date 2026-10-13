# hooks/html_hooks.py
import pytest
from pytest_html import extras
import base64
from datetime import datetime
from utils.report_helpers import embed_screenshot_in_html


def pytest_html_report_title(report):
    """Sets the title of the HTML report."""
    report.title = "Enhanced Mobile Automation Test Report"


def pytest_configure(config):
    """Adds metadata to the Environment section of the HTML report."""
    if hasattr(config, "stash"):
        from pytest_metadata.plugin import metadata_key
        config.stash[metadata_key]["Project Name"] = "Mobile Automation"
        config.stash[metadata_key]["Tester"] = "QA Automation Team"
        config.stash[metadata_key]["Framework"] = "Pytest-BDD & Appium"
        config.stash[metadata_key]["Report Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif hasattr(config, "_metadata"):
        config._metadata["Project Name"] = "Mobile Automation"
        config._metadata["Tester"] = "QA Automation Team"
        config._metadata["Framework"] = "Pytest-BDD & Appium"
        config._metadata["Report Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def pytest_html_results_summary(prefix, summary, postfix):
    """
    Makes pytest-html look closer to a QA execution report.

    The report stays PO/QA-readable.
    Detailed technical debugging remains in execution/appium logs.
    """
    prefix.extend([f"<h2>Test Execution Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2>"])
    prefix.extend(
        [
            """
            <style>
                body {
                    background: #f8fafc;
                    color: #1f2937;
                }

                #title {
                    color: #111827;
                    font-size: 24px;
                    font-weight: 700;
                    margin-bottom: 4px;
                }

                #environment-header h2 {
                    color: #111827;
                    font-size: 17px;
                    margin-top: 18px;
                    margin-bottom: 8px;
                }

                #environment {
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 0;
                    border: 1px solid #d7e3f8;
                    border-radius: 10px;
                    overflow: hidden;
                    background: #ffffff;
                    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
                    margin-bottom: 18px;
                }

                #environment td {
                    padding: 9px 12px;
                    border-bottom: 1px solid #e5eefb;
                    color: #1f2937;
                    font-size: 12px;
                    vertical-align: top;
                }

                #environment tr:last-child td {
                    border-bottom: none;
                }

                #environment td:first-child {
                    width: 240px;
                    background: #eef6ff;
                    color: #0d47a1;
                    font-weight: 700;
                    white-space: nowrap;
                }

                #environment tr:nth-child(odd) {
                    background: #ffffff;
                }

                .summary__data > h2,
                .summary .run-count,
                .summary .filter,
                .summary .filters,
                .summary__spacer,
                .summary__reload {
                    display: none !important;
                }

                .summary {
                    margin: 0;
                    padding: 0;
                    display: block;
                }

                .summary__data {
                    flex: unset !important;
                    width: 100%;
                }

                .controls {
                    justify-content: flex-end;
                    margin-bottom: 8px;
                }

                .collapse button {
                    background: #ffffff;
                    border: 1px solid #cbd5e1;
                    border-radius: 6px;
                    color: #1866CF;
                    padding: 5px 8px;
                    text-decoration: none;
                    font-weight: 600;
                }

                .qa-tests-heading {
                    font-size: 18px;
                    font-weight: 700;
                    color: #111827;
                    margin: 18px 0 8px 0;
                }

                #results-table {
                    border-collapse: separate;
                    border-spacing: 0;
                    width: 100%;
                    border: 1px solid #d7e3f8;
                    border-radius: 10px;
                    overflow: hidden;
                    background: #ffffff;
                    color: #1f2937;
                    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
                }

                #results-table th {
                    background: #1f2937;
                    color: #ffffff;
                    font-weight: 700;
                    padding: 9px 10px;
                    border: 1px solid #374151;
                    white-space: nowrap;
                }

                #results-table td {
                    padding: 9px 10px;
                    border-bottom: 1px solid #e5e7eb;
                    border-right: 1px solid #e5e7eb;
                    color: #1f2937;
                    vertical-align: top;
                }

                #results-table tbody:nth-child(even) tr.collapsible {
                    background: #f9fbff;
                }

                #results-table tbody:nth-child(odd) tr.collapsible {
                    background: #ffffff;
                }

                #results-table td.qa-result-passed {
                    background: #e8f5e9;
                    color: #1b5e20;
                    font-weight: 700;
                    text-align: center;
                }

                #results-table td.qa-result-failed {
                    background: #ffebee;
                    color: #b71c1c;
                    font-weight: 700;
                    text-align: center;
                }

                #results-table td.qa-result-skipped {
                    background: #fff3e0;
                    color: #e65100;
                    font-weight: 700;
                    text-align: center;
                }

                .qa-env-badge,
                .col-platform::before {
                    display: inline-block;
                    padding: 4px 9px;
                    border-radius: 999px;
                    font-weight: 700;
                    font-size: 11px;
                    white-space: nowrap;
                }

                .qa-env-badge {
                    background: #e3f2fd;
                    color: #0d47a1;
                }

                .qa-platform-ios {
                    background: #e3f2fd;
                    color: #0d47a1;
                }

                .qa-platform-android {
                    background: #e8f5e9;
                    color: #1b5e20;
                }

                .qa-test-id {
                    font-size: 11px;
                    font-weight: 700;
                    color: #1866CF;
                    margin-bottom: 3px;
                }

                .qa-test-title {
                    font-size: 13px;
                    font-weight: 700;
                    color: #111827;
                    margin-bottom: 3px;
                }

                .qa-test-description {
                    font-size: 12px;
                    color: #4b5563;
                    line-height: 1.45;
                }

                .qa-internal-order {
                    position: absolute;
                    width: 1px;
                    height: 1px;
                    padding: 0;
                    margin: -1px;
                    overflow: hidden;
                    clip: rect(0, 0, 0, 0);
                    white-space: nowrap;
                    border: 0;
                }

                .col-testId {
                    width: 48%;
                }

                .col-result {
                    width: 90px;
                }

                .col-duration {
                    white-space: nowrap;
                    font-weight: 600;
                }

                .col-platform {
                    white-space: nowrap;
                    text-align: center;
                    font-size: 0;
                }

                .col-platform::before {
                    content: attr(data-platform);
                    font-size: 11px;
                }

                .col-platform.qa-platform-ios::before {
                    background: #e3f2fd;
                    color: #0d47a1;
                }

                .col-platform.qa-platform-android::before {
                    background: #e8f5e9;
                    color: #1b5e20;
                }

                .col-comments {
                    min-width: 260px;
                    max-width: 440px;
                    white-space: normal;
                    overflow-wrap: anywhere;
                    line-height: 1.4;
                }

                #results-table tbody.passed .extras-row,
                #results-table tbody.skipped .extras-row,
                #results-table tbody.qa-details-via-buttons .extras-row {
                    display: none !important;
                }

                #results-table tbody.passed .collapsible td,
                #results-table tbody.skipped .collapsible td,
                #results-table tbody.qa-details-via-buttons .collapsible td {
                    cursor: default !important;
                }

                #results-table tbody.qa-details-via-buttons .qa-detail-button {
                    cursor: pointer !important;
                }

                #results-table tbody.passed .collapsible td::after,
                #results-table tbody.skipped .collapsible td::after,
                #results-table tbody.qa-details-via-buttons .collapsible td::after {
                    display: none !important;
                }

                .logwrapper {
                    display: none !important;
                    background: #f8fafc;
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                }

                #results-table div.media {
                    display: none !important;
                }

                .qa-detail-actions {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin: 8px 0 0;
                }

                .qa-detail-button {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 36px;
                    padding: 7px 14px;
                    border: 1px solid #1866cf;
                    border-radius: 7px;
                    background: #1866cf;
                    color: #ffffff;
                    font-size: 12px;
                    font-weight: 700;
                    cursor: pointer;
                }

                .qa-detail-button:hover,
                .qa-detail-button:focus-visible {
                    background: #0d47a1;
                    border-color: #0d47a1;
                    outline: 2px solid #93c5fd;
                    outline-offset: 2px;
                }

                .qa-media-modal {
                    position: fixed;
                    inset: 0;
                    z-index: 10000;
                    display: none;
                    align-items: center;
                    justify-content: center;
                    padding: 24px;
                    background: rgba(15, 23, 42, 0.92);
                }

                .qa-media-modal.is-open {
                    display: flex;
                }

                .qa-media-modal img {
                    display: block;
                    max-width: 96vw;
                    max-height: 94vh;
                    width: auto;
                    height: auto;
                    object-fit: contain;
                    border-radius: 8px;
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
                }

                .qa-media-modal video {
                    display: block;
                    width: auto;
                    height: auto;
                    max-width: 96vw;
                    max-height: 94vh;
                    object-fit: contain;
                    border-radius: 8px;
                    background: #000000;
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
                }

                .qa-media-modal img[hidden],
                .qa-media-modal video[hidden],
                .qa-media-modal pre[hidden] {
                    display: none !important;
                }

                .qa-log-content {
                    width: min(1100px, 94vw);
                    max-height: 86vh;
                    margin: 0;
                    padding: 18px;
                    overflow: auto;
                    white-space: pre-wrap;
                    overflow-wrap: anywhere;
                    user-select: text;
                    border: 1px solid #94a3b8;
                    border-radius: 8px;
                    background: #e5e7eb;
                    color: #111827;
                    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco,
                        Consolas, "Liberation Mono", "Courier New", monospace;
                    font-size: 12px;
                    line-height: 1.5;
                    text-align: left;
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
                }

                .qa-media-modal__close {
                    position: fixed;
                    top: 14px;
                    right: 18px;
                    width: 40px;
                    height: 40px;
                    border: 1px solid rgba(255, 255, 255, 0.65);
                    border-radius: 999px;
                    background: rgba(15, 23, 42, 0.8);
                    color: #ffffff;
                    font-size: 25px;
                    line-height: 1;
                    cursor: pointer;
                }

            </style>

            <script>
                document.addEventListener("DOMContentLoaded", () => {
                    const detailTemplate = document.getElementById(
                        "template_results-table__tbody"
                    );
                    const emptyTemplate = document.getElementById(
                        "template_results-table__body--empty"
                    );
                    detailTemplate?.content.querySelector("td.extra")
                        ?.setAttribute("colspan", "6");
                    emptyTemplate?.content.querySelector("td")
                        ?.setAttribute("colspan", "6");
                    document.querySelectorAll("#results-table td.extra")
                        .forEach((cell) => cell.setAttribute("colspan", "6"));
                    document.querySelector("#results-table #not-found-message td")
                        ?.setAttribute("colspan", "6");

                    const modal = document.createElement("div");
                    modal.className = "qa-media-modal";
                    modal.setAttribute("role", "dialog");
                    modal.setAttribute("aria-modal", "true");
                    modal.setAttribute("aria-label", "Full-size failure screenshot");
                    modal.innerHTML = (
                        '<button class="qa-media-modal__close" type="button" '
                        + 'aria-label="Close media viewer">&times;</button>'
                        + '<img alt="Full-size failure screenshot" hidden>'
                        + '<video controls hidden></video>'
                        + '<pre class="qa-log-content" tabindex="0" hidden></pre>'
                    );
                    document.body.appendChild(modal);

                    const detailsByKey = new Map();
                    const dataContainer = document.getElementById("data-container");
                    let reportData = {};
                    try {
                        reportData = JSON.parse(dataContainer?.dataset.jsonblob || "{}");
                    } catch (error) {
                        console.warn("Embedded report media could not be read", error);
                    }

                    Object.values(reportData.tests || {}).forEach((reports) => {
                        reports.forEach((testReport) => {
                            const media = (testReport.extras || []).filter(
                                (item) => item.format_type === "image"
                                    || item.format_type === "video"
                            );
                            const log = testReport.log || "";
                            if (media.length || log.trim()) {
                                detailsByKey.set(testReport.testId, {media, log});
                            }
                        });
                    });

                    const closeModal = () => {
                        const modalVideo = modal.querySelector("video");
                        modalVideo.pause();
                        modalVideo.removeAttribute("src");
                        modalVideo.load();
                        modalVideo.hidden = true;
                        const modalImage = modal.querySelector("img");
                        modalImage.removeAttribute("src");
                        modalImage.hidden = true;
                        const modalLog = modal.querySelector("pre");
                        modalLog.textContent = "";
                        modalLog.hidden = true;
                        modal.classList.remove("is-open");
                    };
                    modal.addEventListener("click", (event) => {
                        if (event.target === modal || event.target.closest("button")) {
                            closeModal();
                        }
                    });
                    document.addEventListener("keydown", (event) => {
                        if (event.key === "Escape" && modal.classList.contains("is-open")) {
                            closeModal();
                        }
                    });
                    const openMedia = (media) => {
                        if (!media?.content) {
                            return;
                        }
                        const modalImage = modal.querySelector("img");
                        const modalVideo = modal.querySelector("video");
                        const modalLog = modal.querySelector("pre");
                        modalLog.hidden = true;
                        if (media.format_type === "image") {
                            modalVideo.hidden = true;
                            modalImage.src = media.content;
                            modalImage.alt = media.name || "Full-size failure screenshot";
                            modalImage.hidden = false;
                            modal.setAttribute("aria-label", "Full-size failure screenshot");
                        } else if (media.format_type === "video") {
                            modalImage.hidden = true;
                            modalVideo.src = media.content;
                            modalVideo.hidden = false;
                            modalVideo.load();
                            modal.setAttribute("aria-label", "Attached test video");
                        }
                        modal.classList.add("is-open");
                    };

                    const openLogs = (log) => {
                        if (!log?.trim()) {
                            return;
                        }
                        const decoder = document.createElement("textarea");
                        decoder.innerHTML = log;
                        const modalImage = modal.querySelector("img");
                        const modalVideo = modal.querySelector("video");
                        const modalLog = modal.querySelector("pre");
                        modalImage.hidden = true;
                        modalVideo.pause();
                        modalVideo.hidden = true;
                        modalLog.textContent = decoder.value;
                        modalLog.hidden = false;
                        modal.setAttribute("aria-label", "Failure logs and traceback");
                        modal.classList.add("is-open");
                        modalLog.focus();
                    };

                    const addDetailButtons = () => {
                        document.querySelectorAll(
                            "#results-table tbody.failed, #results-table tbody.error"
                        ).forEach((resultBody) => {
                            const commentsCell = resultBody.querySelector(".col-comments");
                            if (!commentsCell || commentsCell.querySelector(".qa-detail-actions")) {
                                return;
                            }
                            const details = detailsByKey.get(resultBody.id) || {};
                            const media = details.media || [];
                            const screenshot = media.find(
                                (item) => item.format_type === "image"
                                    && /failure screenshot/i.test(item.name || "")
                            ) || media.find((item) => item.format_type === "image");
                            const video = media.find((item) => item.format_type === "video");
                            const log = details.log || "";
                            if (!screenshot && !video && !log.trim()) {
                                return;
                            }

                            const actions = document.createElement("div");
                            actions.className = "qa-detail-actions";
                            if (screenshot) {
                                const screenshotButton = document.createElement("button");
                                screenshotButton.type = "button";
                                screenshotButton.className = "qa-detail-button";
                                screenshotButton.textContent = "View Screenshot";
                                screenshotButton.addEventListener(
                                    "click",
                                    (event) => {
                                        event.stopPropagation();
                                        openMedia(screenshot);
                                    },
                                );
                                actions.appendChild(screenshotButton);
                            }
                            if (video) {
                                const videoButton = document.createElement("button");
                                videoButton.type = "button";
                                videoButton.className = "qa-detail-button";
                                videoButton.textContent = "View Video";
                                videoButton.addEventListener("click", (event) => {
                                    event.stopPropagation();
                                    openMedia(video);
                                });
                                actions.appendChild(videoButton);
                            }
                            if (log.trim()) {
                                const logButton = document.createElement("button");
                                logButton.type = "button";
                                logButton.className = "qa-detail-button";
                                logButton.textContent = "View Logs";
                                logButton.addEventListener("click", (event) => {
                                    event.stopPropagation();
                                    openLogs(log);
                                });
                                actions.appendChild(logButton);
                            }
                            commentsCell.appendChild(actions);
                            const extraHtml = resultBody.querySelector(".extraHTML");
                            if (!extraHtml?.children.length) {
                                resultBody.classList.add("qa-details-via-buttons");
                            }
                        });
                    };

                    addDetailButtons();
                    const resultsObserver = new MutationObserver(addDetailButtons);
                    resultsObserver.observe(document.body, {
                        childList: true,
                        subtree: true,
                    });
                });
            </script>

            <div class="qa-tests-heading">Tests Executed</div>
            """
        ]
    )

def pytest_html_results_table_header(cells):
    """Adds custom columns to the results table header."""
    cells.insert(1, '<th class="sortable time" data-column-type="time">Time</th>')
    cells.insert(2, "<th>Platform</th>")
    cells.insert(3, "<th>Description</th>")


def pytest_html_results_table_row(report, cells):
    """Adds data for the custom columns in the results table."""
    current_time = getattr(report, "execution_time", datetime.now().strftime("%H:%M:%S"))
    desc = getattr(report, "description", "No description provided")
    
    # Determine platform based on test name or markers (defaults to Android if unknown)
    is_ios = "ios" in report.nodeid.lower() or "ios" in getattr(report, "keywords", [])
    platform_class = "qa-platform-ios" if is_ios else "qa-platform-android"
    platform_label = "iOS" if is_ios else "Android"
    
    cells.insert(1, f'<td class="col-time">{current_time}</td>')
    cells.insert(2, f'<td class="col-platform {platform_class}" data-platform="{platform_label}"></td>')
    cells.insert(3, f'<td class="col-comments">{desc}</td>')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Wraps test execution report generation -> embeds cached screenshot and extra metadata into pytest-html report."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

    # Attach description and time to the report
    report.description = str(item.function.__doc__) if item.function.__doc__ else getattr(item, 'name', 'No description')
    report.execution_time = datetime.now().strftime("%H:%M:%S")

    # Only process screenshots during the actual test call
    if report.when == "call":
        pytest_html = item.config.pluginmanager.getplugin("html")
        if pytest_html:
            embed_screenshot_in_html(report, item, pytest_html)

        if report.failed:
            img_bytes = getattr(item, "failed_step_png", getattr(item, "failed_screenshot_png", getattr(item, "latest_step_png", None)))
            if img_bytes:
                try:
                    import base64
                    encoded = base64.b64encode(img_bytes).decode("ascii")
                    report.extras = list(getattr(report, "extras", []) or [])
                    report.extras.append(extras.image(f"data:image/png;base64,{encoded}", name="Failure screenshot"))
                except Exception:
                    pass

            
        # Add test logs to the HTML report extras if there was a failure
        if report.failed:
            if hasattr(report, 'extras'):
                pass
            else:
                report.extras = []
            
            # Example: Could attach logs here if needed
            # report.extras.append(pytest_html.extras.text("Failed log details..."))