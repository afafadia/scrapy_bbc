# Scrapy - Web Scraping (https://www.bbc.com)

# Code Walkthrough

## Environment setup:

1. Clone this repository
2. Navigate to the folder location of this cloned repository on your laptop/PC
3. Create virtual environment: `python3 -m venv venv`
4. Activate virtual environment: `source ./venv/bin/activate`
5. Install packages from `./requirements.txt` file: `pip install -r ./requirements.txt`

## Steps to get the scraped results:

1. Run command: `scrapy crawl bbc`
2. Check contents of file(`./bbc_feed.json`): `less ./bbc_feed.json`
