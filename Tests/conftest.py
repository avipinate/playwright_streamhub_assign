import pytest

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_name):
    return {"headless": False, "args": ["--start-maximized"]}

