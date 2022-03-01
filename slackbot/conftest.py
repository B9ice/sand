import time

import requests
import os

from requests.adapters import HTTPAdapter
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import tomli
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3 import Retry

from pages.BasePage import BasePage

pytest_plugins = ["docker_compose"]


def get_test_conf():
    p = Path(__file__).parent / "assets" / "slack.toml"
    with open(p, 'rb') as f:
        return tomli.load(f)


@pytest.fixture(scope="session", autouse=True)
def wait_for_hub_initialization(session_scoped_container_getter, hub_url="http://localhost:4444"):
    request_session = requests.Session()
    retries = Retry(total=10,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    res = {"ready": False}
    n = 0
    while not res["ready"] and n <= 5:
        time.sleep(10)
        res = request_session.get(hub_url + '/status').json()['value']
        n += 1

    assert res["ready"], "selenium-hub not ready"


@pytest.fixture
def setup_driver(request):
    """
    - Initializes a local chrome driver instance if no remote browser is specified via env_var `BROWSER`
    - Defaults to HEADLESS if `BROWSER=chrome` (due to xdg pop-up when chrome is launched on new ubuntu release)
    - Remote Firefox browser can be run headless by setting `BROWSER=firefox HEADLESS=true`
    """
    cfg = get_test_conf()
    # pass config to BasePage class
    request.cls.cfg = cfg
    browser = os.getenv('BROWSER')

    if browser is None:
        # default to locally installed chrome-driver if no remote browser is specified
        driver = webdriver.Chrome()
        opt = webdriver.ChromeOptions()
        if os.getenv('HEADLESS'):
            opt.add_argument('--headless')
    else:
        # initiate remote browser
        if browser.lower() not in ['chrome', 'firefox']:
            raise NameError(f'Invalid Browser: {browser}. Choose one of [chrome, firefox]')

        if browser.lower() == 'chrome':
            opt = webdriver.ChromeOptions()
            opt.add_argument("--disable-popup-blocking")
            # There is a bug with chrome on new versions of ubuntu when
            # launched without headless option
            opt.add_argument("--headless")
            driver = webdriver.Remote(command_executor=cfg['webdriver_endpoint'],
                                      options=opt)
        else:
            opt = webdriver.FirefoxOptions()
            if os.getenv('HEADLESS'):
                opt.add_argument('--headless')
            driver = webdriver.Remote(command_executor=cfg['webdriver_endpoint'],
                                      options=opt)

    driver.implicitly_wait(5)

    # login to slack client
    driver.get(cfg['slack_url'])

    driver.find_element(BasePage.get_strategy(cfg['locators']['login']['username']['by']),
                        cfg['locators']['login']['username']['selector']).send_keys(cfg['username'])
    driver.find_element(BasePage.get_strategy(cfg['locators']['login']['password']['by']),
                        cfg['locators']['login']['password']['selector']).send_keys(cfg['password'])
    driver.find_element(BasePage.get_strategy(cfg['locators']['login']['submit']['by']),
                        cfg['locators']['login']['submit']['selector']).click()

    # wait for app to finish loading
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((BasePage.get_strategy(cfg['locators']['channels']['dropdown']['by']),
                                            cfg['locators']['channels']['dropdown']['selector'])))
    except TimeoutException:
        p = Path(__file__).parent / "screenshots" / "login.png"
        driver.save_screenshot(p.as_posix())
        raise TimeoutException(f"Login Failed. See Screenshot {p}")
    # set driver in BasePage
    request.cls.driver = driver
    yield
    driver.close()
