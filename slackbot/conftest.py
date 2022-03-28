import time

import requests
import os

from requests.adapters import HTTPAdapter
from pathlib import Path
import tomli
import pytest
from selenium import webdriver
from urllib3 import Retry

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


@pytest.fixture(scope="class")
def setup_driver(request):
    """
    - Initializes a local chrome driver instance if no remote browser is specified via env_var `BROWSER`
    - A remote chrome browser can be run headless by setting `BROWSER=chrome HEADLESS=true`
    """
    cfg = get_test_conf()
    # pass config to BasePage class
    request.cls.cfg = cfg
    browser = os.getenv('BROWSER')

    if browser is None:
        # default to locally installed chrome-driver if no remote browser is specified
        # for debugging
        driver = webdriver.Chrome()
        opt = webdriver.ChromeOptions()
        if os.getenv('HEADLESS'):
            opt.add_argument('--headless')
    else:
        # initiate remote browser
        # not tested in firefox
        if browser.lower() not in ['chrome', 'firefox']:
            raise NameError(f'Invalid Browser: {browser}. Choose one of [chrome, firefox]')

        if browser.lower() == 'chrome':
            opt = webdriver.ChromeOptions()
            opt.add_argument("--disable-popup-blocking")
        else:
            opt = webdriver.FirefoxOptions()

        if os.getenv('HEADLESS'):
            opt.add_argument('--headless')
        driver = webdriver.Remote(command_executor=cfg['webdriver_endpoint'],
                                  options=opt)

    driver.implicitly_wait(5)

    # login to slack client
    driver.get(cfg['github_url'])

    # set driver in BasePage
    request.cls.driver = driver
    yield
    driver.close()
