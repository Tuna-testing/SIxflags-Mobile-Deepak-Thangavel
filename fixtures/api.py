import pytest


@pytest.fixture(scope="session")
def env(request):
    """Returns the environment passed via CLI command (defaults to prod)."""
    return request.config.getoption("--env").lower()