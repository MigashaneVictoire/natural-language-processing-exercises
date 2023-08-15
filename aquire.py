from requests import get
from bs4 import BeautifulSoup
import os
from pprint import pprint

url = "https://inshorts.com/en/read"
# set different categories to perse through
category = ["Business"]#, "Sports", "Technology", "Entertainment"]

parse = {}
for cat in category:
    # read the url
    res = get(url + "/" + cat)
    print(res)
    
    # create a beautiful soup object
    soup_parser = BeautifulSoup(res.content, 'html.parser')
    # locate the main tag containing all the articles
    soup = soup_parser.find("div", style = "min-height: calc(100vh - 348px);")
    # parse[cat] = soup
    
    for i in range(len(soup.find_all("div"))):
            pprint(soup.find_all("div")[i])