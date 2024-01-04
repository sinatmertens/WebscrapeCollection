from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import scraperlib as hs

from datetime import datetime
import os
import time
import requests
import re

# Variables
log_list = []
project_name = 'reflecta'

timestr = time.strftime("%Y%m%d")
weekday = datetime.today().strftime('%A')

path = '2 - Ressources & Organisation (o, r, s)/r - 1 - Data & Databases/Webscraper-Database/' + str(
    timestr) + ' - reflecta/'


def log(string):
    log_list.append(str(time.strftime("%Y%m%d %H:%M:%S")) + ' - ' + string + ' \n')


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

#driver = webdriver.Chrome(options=chrome_options,
#                           executable_path='D:/Github Repositories/webscrape-repo/tests/geckodriver.exe')

chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver.implicitly_wait(10)


# Log into reflecta.network
def login():
    driver.get("https://www.reflecta.network/")
    driver.implicitly_wait(30)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="js_cookieNotice_accept"]'))).click()
    driver.implicitly_wait(5)
    driver.find_element_by_tag_name("a[href*='sign_in']").click()
    driver.implicitly_wait(5)
    driver.find_element_by_tag_name("input[id*='user_email']").send_keys('sinatmertens@gmail.com')
    driver.implicitly_wait(5)
    driver.find_element_by_tag_name("input[id*='user_password']").send_keys('9NefXPyCTZpC4Ck')
    driver.implicitly_wait(5)
    driver.find_element_by_tag_name("input[value*='Login']").click()
    driver.implicitly_wait(5)

orga = 'Organisation'
startups = 'Startup'
campaigns = 'Campaign'


def scrape_urls(href, filename):
    # Start scraper
    page = 0
    search_results_list = []

    for i in range(100):

        try:
            url = 'https://www.reflecta.network/suche?0=2&page=' + str(page) + '&type%5B%5D=' + str(href)
            driver.get(url)
            search_results = driver.find_element_by_tag_name("div[class*='results']")
            search_results = search_results.find_elements_by_tag_name(
                "a[href*='https://www.reflecta.network/']")

            for search_result in search_results:
                search_results_list.append(search_result.get_attribute('href'))

            page += 1

        except:
            break

    search_results_list_final = list(set(search_results_list))
    search_results_str_final = '\n'.join(search_results_list_final)
    example_page = ''.join(search_results_list_final[0:1])  # Get url of first page as example page
    print(example_page)
    hs.file_to_nextcloud(path=path, string=search_results_str_final, file_name=filename)
    return example_page


if __name__ == "__main__":
    log('Start scraper for Project - ' + str(project_name))

    # Create Folder
    try:
        hs.create_folder(d_format='day', project_name='reflecta')
        log('Created folder for Project - ' + str(project_name))
        print('Created folder for Project - ' + str(project_name))
    except:
        log('Folder for Project already existing.')

    log('Login to reflecta.network')
    login()

    # Check whether Organisations got scraped already and if not scrape them
    try:
        hs.check_for_file(path=path, file_name='urls - organisations.txt')
        print('File exists')
        log('Campaigns already scraped.')
    except:

        log('Start scraping organisations.')
        example_page_orga = scrape_urls(orga, 'urls - organisations.txt')  # Scrape page links AND retrieve example_page_url

        log('Start scraping example page of organisations as html File')
        example_soup_orga = hs.get_examplepage(path, example_page_orga, file_name='examplepage - organisations.html')

        log('Start getting css-Files for example page of organisations.')
        hs.get_css(path, example_soup_orga)

    # Check whether Social Startups got scraped already and if not scrape them
    try:
        hs.check_for_file(path=path, file_name='urls - social_startups.txt')
        log('Campaigns already scraped.')
    except:
        log('Start scraping social_startups.')
        example_page_startup = scrape_urls(startups, 'urls - social_startups.txt')  # Scrape page links AND retrieve example_page_url

        log('Start scraping example page of social_startups as html File')
        example_soup_startups = hs.get_examplepage(path, example_page_startup, file_name='examplepage - startups.html')

        log('Start getting css-Files for example page of social_startups.')
        hs.get_css(path, example_soup_startups)

    # Check whether Campaigns got scraped already and if not scrape them
    try:
        hs.check_for_file(path=path, file_name='urls - campaigns.txt')
        log('Campaigns already scraped.')

    except:
        log('Start scraping campaigns.')
        example_page_campaign = scrape_urls(campaigns, 'urls - campaigns.txt')  # Scrape page links AND retrieve example_page_url

        log('Start scraping example page of campaigns as html File')
        example_soup_campaign = hs.get_examplepage(path, example_page_campaign, file_name='examplepage - campaigns.html')

        log('Start getting css-Files for example page of campaigns.')
        hs.get_css(path, example_soup_campaign)