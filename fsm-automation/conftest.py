"""PyTest configuration and shared fixtures"""

import os
import pytest
import allure
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
def browser_config():
    """Browser configuration settings"""
    return {
        "headless": os.getenv("HEADLESS", "False").lower() == "true",
        "slow_mo": int(os.getenv("SLOW_MO", "400")),
        "second_monitor_x": int(os.getenv("SECOND_MONITOR_X", "1920")),
    }


@pytest.fixture(scope="session")
def browser(playwright: Playwright, browser_config):
    """Launch browser with custom configuration"""
    browser = playwright.chromium.launch(
        headless=browser_config["headless"],
        slow_mo=browser_config["slow_mo"],
        args=[
            f"--window-position={browser_config['second_monitor_x']},0",
            "--start-maximized",
        ]
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create new browser context for each test"""
    context = browser.new_context(
        viewport=None,  # Use full window size
        ignore_https_errors=True,
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create new page for each test"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def credentials():
    """Load FSM credentials from environment"""
    return {
        "url": os.getenv("FSM_URL"),
        "username": os.getenv("FSM_USERNAME"),
        "password": os.getenv("FSM_PASSWORD"),
    }


@pytest.fixture(scope="function")
def screenshot_dir():
    """Create screenshot directory for test"""
    screenshots_path = Path("reports/screenshots")
    screenshots_path.mkdir(parents=True, exist_ok=True)
    return screenshots_path


def pytest_configure(config):
    """Create reports directories"""
    Path("reports/allure-results").mkdir(parents=True, exist_ok=True)
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    Path("reports/TES070").mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot to Allure report on test failure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get page fixture if available
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_bytes = page.screenshot()
            allure.attach(
                screenshot_bytes,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
