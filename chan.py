#-*- encoding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

start_url = "http://blog.sina.com.cn/s/articlelist_1215172700_0_1.html"

links = []
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}


def get_links(url):
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text)
    articles = soup.select(".atc_title")

    for article in articles:
        if str(article.text).__contains__("教你炒股票"):
            links.append(article.a['href'])

    next_page = soup.select(".SG_pgnext")[0].a['href']

    return links, next_page

def get_article(url):
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text)
    title = soup.select(".articalTitle")[0].text
    content = []
    raw_content = soup.select(".articalContent")
    for line in raw_content:
        content.append(line.text)

    return title, content

def save_article(url):
    pass



all_content = []


if __name__ == "__main__":
    links, next_page = get_links(start_url)

    for link in links:
        title, content = get_article(link)
        all_content.append([title, content])

    for i in range(21):
        links, next_page = get_links(next_page)
        print("page", i+2, "done")
        for link in links:
            title, content = get_article(link)
            all_content.append([title, content])

    all_content.reverse()

    with open('chan.txt', 'w') as chan:
        for article in all_content:
            chan.write(article[0] + article[1][0])