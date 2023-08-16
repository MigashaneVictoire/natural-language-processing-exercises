import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import os
from pprint import pprint
from datetime import datetime as dt


def get_blog_articles():
    headers = {'User-Agent': 'Codeup Data Science'} # Some websites don't accept the pyhon-requests default user-agent

    # read the url
    res = get("https://codeup.edu/blog/", headers=headers)
    # create a beautiful soup object
    soup_parser = BeautifulSoup(res.content, 'html.parser').body
    soup_id = soup_parser.find("div", id="et-boc")

    # find all the titles and link to the hlog contemt
    blog = {}
    title_entry = soup_id.select(".entry-title") # soup_id.find_all("h2", class_="entry-title")
    for i in range(len(title_entry)):
        blog[f"blog {i}"] = [f"{title_entry[i].a.text}", f'{title_entry[0].a["href"]}']
        
    for cont in blog.keys():
        # read the url
        blog_cont = get(blog[cont][1], headers=headers)
        blog_content = BeautifulSoup(blog_cont.content,"html.parser").body.text
        # blog_content.replace("\n", "", regex=False)
        blog[cont].append(blog_content.replace("\n", "").replace("\t", ""))
    return blog
        
    

def get_news_articles():
    url = "https://inshorts.com/en/read"
    # set different categories to perse through
    category = ["business", "sports", "technology", "entertainment"]

    articles = {}
    df_setup = []
    for cat in category:
        # read the url
        res = get(url + "/" + category[0])
        print(res)

        # create a beautiful soup object
        soup_parser = BeautifulSoup(res.content, 'html.parser').body

        soup = soup_parser.find_all("span", itemprop="mainEntityOfPage")
        for i in range(len(soup)):
            link = soup[i]["itemid"]

            article = get(link)
            article_soup = BeautifulSoup(article.content,"html.parser").body

            article_title = article_soup.find('span', itemprop='headline').text
            article_body = article_soup.find('div', itemprop='articleBody').text
            # articles[f"article {cat} {i}"] = [article_title, cat ,link ,article_body]

            article_instance = {
                'title': article_title,
                'content': article_body,
                'category': cat,
            }

            df_setup.append(article_instance)
    return pd.DataFrame(df_setup)