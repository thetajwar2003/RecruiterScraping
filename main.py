import os
from selenium import webdriver
from time import sleep
from dotenv import load_dotenv
import collections
import csv
import os.path
from os import path
import pandas as pd

load_dotenv()

# Variables
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
QUOTA = 0

# Check if there is a csv file. If there isn't create one with the specific headers. Otherwise open the csv file to append new data.
if(path.exists("results_file.csv")):
    writer = csv.writer(open('results_file.csv', 'a'))
    df = pd.read_csv("results_file.csv")
else:
    writer = csv.writer(open('results_file.csv', 'w'))
    writer.writerow(['Name', 'Job Title', 'Company', 'Location', 'URL'])

# Connect driver
driver = webdriver.Chrome("/Users/sab0taj/ProgramFiles/chromedriver")
# Go to LinkedIn homepage
driver.get("https://www.linkedin.com/")


# Sign in with my credentials
sleep(3)
username = driver.find_element_by_id("session_key")
username.send_keys(USERNAME)
sleep(2)

password = driver.find_element_by_id("session_password")
password.send_keys(PASSWORD)
sleep(3)

log_in_button = driver.find_element_by_class_name(
    "sign-in-form__submit-button")
log_in_button.click()


# Go to page with list of recruiters in the internet and computer software industry
driver.get("https://www.linkedin.com/search/results/people/?industry=%5B%226%22%2C%224%22%5D&keywords=recruiter&origin=FACETED_SEARCH")

while QUOTA != 10:
    # Grab all of the recruiters' urls
    all_links = driver.find_elements_by_tag_name("a")
    proper_links = [link.get_attribute("href") for link in all_links]
    recruiter_links = [link for link,
                       count in collections.Counter(proper_links).items() if count > 1]
    sleep(0.5)

    # Keep going to the next page if all the recruiters are already in the csv
    while recruiter_links[-1] in df["URL"]:
        next_button = driver.find_element_by_xpath(
            "//div[@aria-label='Next']/div[@class='mn-hd-txt' and text()='Next']")
        next_button.click()
        sleep(2)

    # Go to each recruiter's page and extract information
    for link in recruiter_links:
        driver.get(link)
        sleep(5)
        # Checks to see if the user I am currently looking at is a recruiter or not and if the recruiter has been recroded already yet
        if "?miniProfileUrn" in driver.current_url and driver.current_url not in df["URL"]:
            linkedin_url = driver.current_url

            name = driver.find_element_by_class_name("text-heading-xlarge")
            if name:
                name = name.text

            job_title = driver.find_element_by_class_name("text-body-medium")
            if job_title:
                job_title = job_title.text

            company = driver.find_element_by_class_name(
                "inline-show-more-text")
            if company:
                company = company.text

            location = driver.find_elements_by_class_name("text-body-small")[1]
            if location:
                location = location.text

            writer.writerow([name, job_title, company, location, linkedin_url])
            QUOTA += 1
driver.quit()
