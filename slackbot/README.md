# Solution Overview

**Components / Tools**
- Selenium
  - Standalone docker images for `Chrome` and `Firefox` browsers on
    ubuntu. See docker-compose.yml
- Pytest
- Python 3

# Installation / Setup

1. unzip slackbot.zip
2. Create and activate a python3  virtual env 
   - python3 -m venv .slackenv
   - source .slackenv/bin/activate
3. cd slackbot & pip install -r requirements.txt
4. locate assets/slack.toml and enter login credentials for slack client
5. run `BROWSER=chrome pytest --docker-compose ./docker-compose.yml --no-header -v --junitxml=result.xml`

# Notes
- There is a bug with xdg pop up when launching chrome browser on new ubuntu
  release. So this solution is hard-coded to launch chrome headless when runnning
  remotely in docker container.
  Setting the browser to Chrome or Firefox via env var `BROWSER` will launch 
  the specified browser on the linux docker container and execute the test.
- To view the test run live please set `BROWSER`=`firefox` and open vnc viewer connected via port 6902.
- Machine-readable output is retrievable from the junit xml file - result.xml
- `pytest-xdist` is a pytest plugin installed to support running additional tests
  in parallel by specifying -n <number or parallel tests>

# Executing Locally Anywhere
- To run on chrome locally anywhere without the remote docker solution simply repeat
  steps 1 - 3 above and follow these additional steps:
  1. Install a stable release of chrome-browser and the matching chromedriver version.
  2. run `pytest --no-header -v --junitxml=result.xml` (Note: do not specify a browser)

     
