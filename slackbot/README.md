# Solution Overview

**Components / Tools**
- Selenium
  - Standalone docker images for `Chrome` and `Firefox` browsers on
    ubuntu. See docker-compose.yml
- Pytest
- Python 3

# Installation / Setup

1. Clone slackbot or unzip slackbot.zip
2. Create and activate a python3  virtual env 
   - python3 -m venv .slackenv
   - source .slackenv/bin/activate
3. cd slackbot & pip install -r requirements.txt

# Execution examples
1. Ensure docker is installed and start it 
2. BROWSER=chrome python -m pytest --docker-compose ./docker-compose.yml --html=report.html --no-header -v --junitxml=result.xml

# Notes
- To view the test run live please set `BROWSER`=`chrome` and open vnc viewer connected via port 6900.
- Machine-readable output is retrievable from the junit xml file `--junitxml=result.xml`
- Human readable output is retrievable by adding to command `--html=report.html`
- `pytest-xdist` is a pytest plugin installed to support running additional tests
  in parallel by specifying -n <number or parallel tests>