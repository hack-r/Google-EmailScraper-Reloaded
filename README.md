# Google-EmailScraper-Reloaded

Google-EmailScraper-Reloaded is a tool that searches Google based on a query and scrapes all emails found on each page. The output files are saved as csv. Based on Google-EmailScraper for Python 2.x and xgoogle by Kenny Ledet (https://github.com/kennyledet/Google-EmailScraper).

This repo contains a list of valid TLD's (tld.txt) which aids in email validation. You may edit it to fit your needs.

## Installation

1. Clone the repository.
2. Install the required Python libraries by running the following command:

    pip install -r requirements.txt


## Usage

You can run the script using the following command:

python main_serp.py -query "Your Search Query" -pages 10 -o "output.csv" -key "Your_Serp_API_Key"


Where:

  - `-query` is your search query.
  - `-pages` is the number of Google results pages to scrape (default is 10).
  - `-o` is the output filename (default is 'emails.csv').
  - `-key` is your Serp API key.

There are three optional flags for post-processing:

  -P: Enable post-processing. This will convert all emails to lowercase, remove duplicates, and validate the emails.
  -Eo: Email only output. This will only include emails in the output CSV, not the source page info.
  -Ng: Exclude .gov emails. This will remove all .gov emails, as well as emails from sheriff, county, and federal domains.

You can provide the Serp API key either directly as a command line argument using `-key`, or you can set it in a `.env` file with the variable name `SERP_API_KEY`. The script will automatically load the API key from the `.env` file if it's not provided in the command line.

Please replace "Your Search Query", "output.csv", and "Your_Serp_API_Key" with your actual search query, desired output file name, and Serp API key respectively.

Remember to create a .env file in the same directory as your script, and add your Serp API key to it like this, if you prefer not to provide it in the command line:

    SERP_API_KEY=your_serp_api_key
    
Replace your_serp_api_key with your actual Serp API key.
