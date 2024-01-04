"""Web Scraping Tool for Meetup.com

This tool opens up the event section of Meetup, first scraping a list
of all the event links listed on that page. Afterwards it retrieves all
necessary information on each single event into a list. Finally the
list is printed into a csv file.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import os

# Defining where and which subject is to be webscraped on Meetup
city = "Dortmund"
country = "Deutschland"
URL = "https://www.meetup.com/de-DE/find/events/"

# Defining which webdriver to use and how to name the output files
driver = webdriver.Firefox()
filename = '../../MeetupEventList.csv'
filenameCleaned = 'eventListCleaned.csv'

# Lists to store information in
eventListings = []
# a list to store the event Listing URLs
event = []
# a list to store the event information before getting written in CSV

def open_meetup():
    # Opens Meetup and puts in city and country
    driver.get(URL)
    location = driver.find_element_by_xpath("/html/body/div[5]/div[1]/div[4]/div[1]/div[1]/form/div[5]")
    location.click()
    simpleLocation = driver.find_element_by_id("locationSearch")
    driver.implicitly_wait(100)
    simpleLocation.send_keys(city + ", " + country)
    simpleLocation.send_keys(Keys.ENTER)

def more():
    # Clicks the MORE button to open up more content
    driver.find_elements_by_class_name("button span-100").send_keys(Keys.ENTER)

def get_links():
    # Collects all the links from the given URL into a list
    soupOne = BeautifulSoup(driver.page_source, 'html.parser')
    listing = soupOne.find('ul', attrs={"searchResults resetList clearfix"})
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("simple-view"))
    for link in listing.find_all('a'):
        eventListings.append(link.get('href'))
        # Adds all links to the global list named eventListings
    print('All links collected')

def get_info():
    # Collects all the information on the events from that page
    listingStatus = 1
    # Counter on how many listings got scraped already
    for i in eventListings:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('div', attrs={"child-wrapper"})

        if table == None:
            print('Link Nr. ' + str(listingStatus) + ' is not a listing.')
            listingStatus = listingStatus + 1
            continue

        for row in table:
            # Searches through each listing link for title, date, start
            # time, end time, runningText and picture and stores it inside
            # the event table
            table = {}
            try:
                table['title'] = soup.title.string
            except:
                print('No title found in Listing Nr. ' + str(listingStatus) + '.')
                pass
            try:
                table['date'] = soup.find(class_='eventTimeDisplay-startDate').text
            except:
                print('No date found in Listing Nr. ' + str(listingStatus) + '.')
                pass
            try:
                table['startTime'] = soup.find(class_="eventTimeDisplay-startDate-time").text
            except:
                print('No start time found in Listing Nr. ' + str(listingStatus) + '.')
                pass
            try:
                table['endTime'] = soup.find(class_="eventTimeDisplay-endDate-partialTime").text
            except:
                print('No end time found in Listing Nr. ' + str(listingStatus) + '.')
                pass
            try:
                table['runningText'] = soup.find(class_="event-description runningText").text
            except:
                print('No description text found in Listing Nr. ' + str(listingStatus) + '.')
                pass
            try:
                table['picture'] = soup.find(class_="photoCarousel-photoContainer keepAspect--16-9").get('style')
            except:
                print('No picture found in Listing Nr. ' + str(listingStatus) + '.')
                pass
            event.append(table)

        with open(filename, 'w', newline='') as f:
            # Saving the data inside the csv file
            w = csv.DictWriter(f, ['title', 'date', 'startTime', 'endTime', 'runningText', 'picture'])
            w.writeheader()
            for table in event:
                w.writerow(table)

        print('Saved all information from Listing Nr.' + str(listingStatus) + '.')
        listingStatus = listingStatus + 1

# need to add host!


    print('All listings scraped! Start removing all duplicates.')

def clean_duplicates(str):
    # Cleans the collected information in oldFile off all doublets
    # and saves it into newFile
    oldFile = pd.read_csv(str)
    newFile = oldFile.drop_duplicates(subset='title')
    newFile.to_csv(filenameCleaned, index=False)  # index adds extra column



open_meetup()
print('Meetup is open.')

get_links()
print( len(eventListings) + ' links collected.')

get_info()
print('All information collected.')

clean_duplicates(filename)
print('All finished!')