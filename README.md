# LinkedIn Job Searcher

Scrapes all jobs for a given title & location.

NOTE: It's still unstable & not certain to make it to the end alive.


## Setup

1. Download a copy of the chrome webdriver from https://sites.google.com/a/chromium.org/chromedriver/downloads


2. Install all required packages
```bash
cd /LinkedIn_Job_Searcher
pip install -r requirements.txt
```

3. Setup your config with:
```yaml
username: <LinkedIn Username>
password: <LinkedIn Password>
selenium: <Location of the chrome web driver>
job_details:
    title: <Job title>
    location: <Location>
```

3. Run the search via:
```bash
python run.py
```