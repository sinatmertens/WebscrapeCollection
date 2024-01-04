#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as r
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime

cal_week = datetime.today().isocalendar()[1]
timestr = time.strftime("%Y%m%d")
year = time.strftime("%Y")


def create_folder(d_format, project_name):
    """Creates folder convention for the scraper

    :param project_name: Name of the webscraper project (raw name without slashes)
    :type project_name: str
    """

    if d_format == 'cal_week':
        date_format = str(year) +' - KW' + str(cal_week)
    else:
        date_format = timestr


def check_for_file(path, file_name):
    pass


def file_to_nextcloud(path, string, file_name):
    """ Saves file into given path in Nextcloud

    :param path: Path to where file is to be saved (put '/' at the end)
    :param string: String to be stored inside file.
    :param file_name: Name of file (including file_type, e.g. .css, .html, .txt)
    """


def get_html(url_list):
    """"""

    # ist of all urls to scrape
    html_list = []

    # Go through list
    for u in url_list:
        response = r.get(u)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        html_list.append(str(soup) + ' \n')

    liststring = ''
    liststring = liststring.join(html_list)
    return liststring


def get_examplepage(path, url, file_name):
    """This function saves an example page in the project directory.

    :param path: Path to project directory in Nextcloud
    :type path: str
    :param html: Html of a url, received from response statement
    :type html: str
    """

    # TODO: Replace href path inside html with stylesheet name,
    #  because css-file will be stored inside same folder as examplepage.
    try:
        response = r.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        soup = str(soup.prettify())
        file_to_nextcloud(path=path + 'examplepage/', string=soup, file_name=file_name)
        return soup
    except:
        soup = ''
        print('No soup')
        return soup


def get_css(path, html, href=''):
    """ This function saves all CSS Stylesheets into the same directory as the example page.

    :param path: Path to project directory in Nextcloud
    :type path: str
    :param html: Html of a url, received from response statement
    :type html: str
    :param href: href to complete url to get stylesheet, in case the stylesheet is a relative path
        (default in None)
    :type href: str
    """

    # Find css style sheets in soup
    soup = BeautifulSoup(html, 'lxml')
    css_sheets = soup.find_all('link', rel='stylesheet', href=True)

    # Loop through stylesheets
    for sheet in css_sheets:
        # Get their name without relative path
        sheet_name = re.findall('([^/]+$)', sheet['href'])[0]

        # Get the soup of the stylesheet
        resp = r.get(href + str(sheet['href']))
        css_html = resp.text
        css_soup = BeautifulSoup(css_html, 'lxml')

        # Encode soup to string
        css_soup = str(css_soup.text).encode('utf-8')

        # Save stylesheet with true name int same directory as the examplepage.html
        file_to_nextcloud(path=path + 'examplepage/', string=css_soup, file_name=str(sheet_name))