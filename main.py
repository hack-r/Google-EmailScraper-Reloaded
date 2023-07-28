# Google-EmailScraper
# 
# Purpose: Scraper that searches Google based on a query and scrapes all emails found on each page.
# Output files are saved as csv.
# 
# Author: Jason
# Date: 2023-07-27
# 
# This program is released under the MIT License.
# Credit for the defunct Python 2 version: https://github.com/kennyledet/Google-EmailScraper
# 
# This version uses the Serp API instead of the deprecated xGoogle library.

from serpapi import GoogleSearch
from urllib.request import Request, urlopen
import re, csv, os
import argparse
from dotenv import load_dotenv

class ScrapeProcess(object):
    emails = []  # for duplication prevention

    def __init__(self, filename):
        self.filename  = filename
        self.csvfile   = open(filename, 'w+')
        self.csvwriter = csv.writer(self.csvfile)

    def go(self, query, pages):
        load_dotenv()
        serp_api_key = os.getenv('SERP_API_KEY')

        for i in range(pages):
            params = {
                'q': query,
                'num': 10,
                'start': i * 10,
                'api_key': serp_api_key
            }
            search = GoogleSearch(params)
            results = search.get_dict().get('organic_results', [])
            print(f'Number of results: {len(results)}')
            for page in results:
                self.scrape(page)
            
    def scrape(self, page):
        try:
            request = Request(page['link'])
            html = urlopen(request).read().decode('utf8')
            print(f'Scraping page: {page["link"]}')
        except Exception as e:
            print(f'Could not scrape page: {page["link"]}')
            return

        emails = re.findall(r'([A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*)', html)

        for email in emails:
            if email not in self.emails:  # if not a duplicate
                print(f'Found email: {email}')
                self.csvwriter.writerow([page['title'], page['link'], email])
                self.emails.append(email)

parser = argparse.ArgumentParser(description='Scrape Google results for emails')
parser.add_argument('-query', type=str, default='test', help='a query to use for the Google search')
parser.add_argument('-pages', type=int, default=10, help='number of Google results pages to scrape')
parser.add_argument('-o', type=str, default='emails.csv', help='output filename')
parser.add_argument('-key', type=str, default=os.getenv('SERP_API_KEY'), help='Serp API key')

args   = parser.parse_args()
args.o = args.o+'.csv' if '.csv' not in args.o else args.o  # make sure filename has .csv extension

s = ScrapeProcess(args.o)
s.go(args.query, args.pages)
