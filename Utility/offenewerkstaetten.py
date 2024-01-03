from bs4 import BeautifulSoup
import pandas as pd
import csv
import requests


def webscrape():
    url = "https://www.offene-werkstaetten.org/werkstaetten"

    # Get the website
    website = requests.get(url).text
    soup = BeautifulSoup(website, 'html.parser')

    # Go through html and get information needed
    table = soup.find('table', class_="list")

    filename = 'offene_werkstaetten_data.csv'
    header = ["Alphabet", "Name", "Address", "Mail", "Website"]
    output_rows = []

    for table_row in table.findAll('tr'):
        # Write data into columns and store inside table
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)

    with open(filename, 'w', newline='') as csvfile:
        # Write the header into csv
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(i for i in header)

        # Write data into csv
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)

    # Delete unneeded columns
    f = pd.read_csv(filename)
    keep_col = ["Name", "Address", "Mail", "Website"]
    new_f = f[keep_col]
    new_f.to_csv(filename, index=False)

    # Clean the Data
    text = open(filename, "r")

    # Split after countries
    text = ''.join([i for i in text]) \
        .replace('Deutschland', 'Deutschland", "')
    text = ''.join([i for i in text]) \
        .replace('Schweiz', 'Schweiz", "')
    text = ''.join([i for i in text]) \
        .replace('Österreich', 'Österreich", "')

    # Split off Website
    text = ''.join([i for i in text]) \
        .replace('http', '", "http')

    x = open(filename, "w")
    x.writelines(text)
    x.close()
