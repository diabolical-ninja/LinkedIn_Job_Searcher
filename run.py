#%%
from selenium import webdriver
import yaml
import time
import pandas as pd
import csv
from tqdm import tqdm

# Import helper funtions
# from scrape_tools import *

#%%

def element_text_entry(element, value):
    item = driver.find_element_by_id(element)
    item.send_keys(value)


def find_and_click_element(element):
    item = driver.find_element_by_class_name(element)
    item.click()


def get_job_details():

    # Get Location based on element type
    try:
        location = driver.find_element_by_class_name('jobs-details-top-card__exact-location').text
    except:
        # location = driver.find_element_by_xpath('//*[@id="ember1046"]/div/div[2]/div[1]/div[1]/div/span[3]').text
        location = driver.find_element_by_class_name('jobs-details-top-card__bullet').text

    return {
        'job_title': driver.find_element_by_class_name('jobs-details-top-card__job-title').text,
        'company': driver.find_element_by_class_name('jobs-details-top-card__company-url').text,
        'location': location,
        'description': driver.find_element_by_xpath('//*[@id="job-details"]').text
    }


def login(username, password):
    """
    To-Do: Add mechanism to manage "add phone number" page
    """
    element_text_entry('username', username)
    element_text_entry('password', password)
    find_and_click_element('login__form_action_container')

    # To-Do
    # skip_phone_addition = driver.find_element_by_class_name('secondary-action')
    # skip_phone_addition.click()


def get_jobs():
    jobs = driver.find_elements_by_class_name('occludable-update')
    return jobs


def search_jobs(job, location):
    # Enter job & location
    element_text_entry('jobs-search-box-keyword-id-ember35', job)
    element_text_entry('jobs-search-box-location-id-ember35', location)

    # Run search
    find_and_click_element('jobs-search-box__submit-button')

def failover(element_list, index, class_name):
    try:
        element_list[index].find_element_by_class_name(class_name).text
    except:
        return None


def get_job_details():

    # Get Location based on element type
    try:
        location = driver.find_element_by_class_name('jobs-details-top-card__exact-location').text
    except:
        # location = driver.find_element_by_xpath('//*[@id="ember1046"]/div/div[2]/div[1]/div[1]/div/span[3]').text
        location = driver.find_element_by_class_name('jobs-details-top-card__bullet').text

    # Company Name
    try:
        company = driver.find_element_by_class_name('jobs-details-top-card__company-url').text
    except:
        company_text = driver.find_element_by_class_name('jobs-details-top-card__company-info').text
        company = company_text.split('\n')[1]

    # Extract
    div_box = driver.find_elements_by_class_name('jobs-box__group')

    seniority_level = failover(div_box, 0, 'jobs-box__body')
    industry = failover(div_box, 2, 'jobs-box__body')
    employment_type = failover(div_box, 1, 'jobs-box__list-item')
    job_functions = failover(div_box, 3, 'jobs-box__list-item')


    return {
        'job_title': driver.find_element_by_class_name('jobs-details-top-card__job-title').text,
        'company': company,
        'location': location,
        'seniority_level': seniority_level,
        'employment_type': employment_type,
        'industry': industry,
        'job_functions': job_functions,
        'description': driver.find_element_by_xpath('//*[@id="job-details"]').text
    }



#%%
# Import run configuration such as driver location & credentials
config = yaml.safe_load(open('config.yaml'))

#%%

# Instantiate driver & navigate to LinkedIn
driver = webdriver.Chrome(config['selenium'])
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

# Login
login(config['username'], config['password'])

# Navigate to jobs page
driver.get('https://www.linkedin.com/jobs/')

#%%
# Search for jobs
search_jobs(config['job_details']['title'], config['job_details']['location'])



#%%
time.sleep(2)
results_pages = driver.find_elements_by_class_name('artdeco-pagination__indicator')
num_results = len(results_pages)
current_page = 1
job_details = []

print(f"{num_results} pages of search results found")

#%%
while current_page <= num_results:

    print(f"Scraping page {current_page}")

    # Get all listings
    jobs = get_jobs()

    # Extract job details for each listing
    for job in tqdm(jobs):

        # Select listing
        job_card = job.find_element_by_class_name('job-card-search__title')
        job_card.click()

        # Extract details
        job_details.append(get_job_details())

        # Take a nap to not spam the service
        time.sleep(1.5)

    # Navigate to next page
    results_pages = driver.find_elements_by_class_name('artdeco-pagination__indicator')
    
    # Check if its the last page
    if current_page != len(results_pages):
        results_pages[current_page].click()
        time.sleep(0.5)
    current_page += 1



#%%
print(f"{len(job_details)} jobs found")

#%%


#%%
jobs_df = pd.DataFrame(job_details)

# Build filename
results_file = f"{config['job_details']['title']} - {config['job_details']['location']} - search results.csv"
jobs_df.to_csv(results_file,
               sep = "|",
               index = False,
               quoting = csv.QUOTE_ALL,
               encoding='utf-8'
               )

#%%
