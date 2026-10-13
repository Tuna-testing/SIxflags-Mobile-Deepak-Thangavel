# hooks/bdd_hooks.py
from utils.report_helpers import attach_step_screenshot


def pytest_bdd_after_step(
    request, feature, scenario, step, step_func, step_func_args
):
    """Triggers after every passed BDD step -> attaches screenshot inside the step in Allure."""
    driver = getattr(request.node, "driver", None)
    if driver:
        attach_step_screenshot(
            driver,
            name=f"Step: {step.name}",
            node=request.node,
            cache_attr="latest_step_png",
        )


def pytest_bdd_step_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    """Triggers on BDD step failure -> marks node as failed and attaches failure screenshot."""
    driver = getattr(request.node, "driver", None)
    if driver:
        request.node.has_failed = True
        attach_step_screenshot(
            driver,
            name=f"FAILED Step: {step.name}",
            node=request.node,
            cache_attr="failed_step_png",
        )