from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
import datetime
import csv

# user is prompted for a queue of urls to be crawled
user_input_another_URL = "y"
new_urls = deque([])
while user_input_another_URL == "y":
    user_input_url = input("Enter URL here: ")
    new_urls.append(user_input_url)
    user_input_another_URL = input("Enter another URL ([y]/n)? ")
    while user_input_another_URL != "y" and user_input_another_URL != "n":
        print("Enter y or n")
        user_input_another_URL = input("Enter another URL ([y]/n)? ")

# a set of urls that we have already crawled
processed_urls = set()

# a set of crawled emails
emails = set()

# process urls one by one until we exhaust the queue
while len(new_urls):

    # move next url from the queue to the set of processed urls
    url = new_urls.popleft()
    processed_urls.add(url)

    # extract base url to resolve relative links
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url

    # get url's content
    print("Processing %s" % url)
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors
        continue

    # extract all email addresses and add them into the resulting set
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    emails.update(new_emails)

# Write emails to timestamped CSV
now = datetime.datetime.now()
extensionDateTime = now.strftime("%Y%m%d_%H%M%S")
csvfile = "output_emails_"+extensionDateTime+".csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in emails:
        writer.writerow([val])

print("Completed. View output file for emails.")
