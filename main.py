from serpapi import GoogleSearch
from urllib.request import Request, urlopen
import re, csv, os
import argparse
from dotenv import load_dotenv
from datetime import datetime

class ScrapeProcess(object):
    emails = {}  # for duplication prevention and post-processing

    def __init__(self, filename, email_only, no_gov):
        if os.path.isfile(filename):
            filename = f"{os.path.splitext(filename)[0]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        self.filename = filename
        self.email_only = email_only
        self.no_gov = no_gov
        self.csvfile = open(filename, 'w+')
        self.csvwriter = csv.writer(self.csvfile)
        
        # Load TLD list
        with open('tld.txt', 'r') as tld_file:
            self.tld_list = [line.strip() for line in tld_file]

    def validate_email(self, email):
        email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')
        return email_regex.match(email)

    def get_tld(self, email):
        return email.split('.')[-1]

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

        self.post_process()

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
            email = email.lower()
            if self.no_gov and re.search(r'\.gov|sheriff|county|federal', email):
                continue
            if email[-1] == '.':
                tld = email.split('.')[-2]
                if tld in ['com', 'net', 'org', 'edu', 'gov']:
                    email = email[:-1]
            if re.search(r'\d$', email):
                continue
            if email not in self.emails and self.validate_email(email) and self.get_tld(email) in self.tld_list:  # if not a duplicate and valid email with valid TLD
                print(f'Found email: {email}')
                self.emails[email] = (page['title'], page['link'])

    def post_process(self):
        for email, (title, link) in self.emails.items():
            if self.email_only:
                self.csvwriter.writerow([email])
            else:
                self.csvwriter.writerow([title, link, email])

parser = argparse.ArgumentParser(description='Scrape Google results for emails')
parser.add_argument('-query', type=str, default='test', help='a query to use for the Google search')
parser.add_argument('-pages', type=int, default=10, help='number of Google results pages to scrape')
parser.add_argument('-o', type=str, default='emails.csv', help='output filename')
parser.add_argument('-key', type=str, default=os.getenv('SERP_API_KEY'), help='Serp API key')
parser.add_argument('-P', action='store_true', help='Enable post-processing (lowercase and dedupe)')
parser.add_argument('-Eo', action='store_true', help='Email only output')
parser.add_argument('-Ng', action='store_true', help='Exclude .gov emails')

args = parser.parse_args()
args.o = args.o+'.csv' if '.csv' not in args.o else args.o  # make sure filename has .csv extension

s = ScrapeProcess(args.o, args.Eo, args.Ng)
s.go(args.query, args.pages)
