# Joseph Wang
# 1/14/2021
# Practice scraper program using BeautifulSoup and requests packages

from bs4 import BeautifulSoup
import requests
import csv

# Use requests library to get the html code from the website
source = requests.get('https://coreyms.com').text

soup = BeautifulSoup(source, 'lxml')

csv_file = open('cms_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary', 'video_link'])

for article in soup.find_all('article'):
    headline = article.h2.a.text
    print(headline)

    summary = article.find('div', class_='entry-content').p.text
    print(summary)

    try:
        # To access an attribute of a tag (instead of the contents), access it like a dictionary
        vid_src = article.find('iframe', class_='youtube-player')['src']

        # Extract the Youtube video ID
        vid_id = vid_src.split('/')[4]
        vid_id = vid_id.split('?')[0]
        yt_link = f'https://youtube.com/watch?v={vid_id}'
    except TypeError:
        yt_link = None

    print(yt_link)
    print()

    csv_writer.writerow([headline, summary, yt_link])

csv_file.close()