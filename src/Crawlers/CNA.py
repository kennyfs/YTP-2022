import collections
import json
import re

import requests
from bs4 import BeautifulSoup

CNAnews = collections.namedtuple("CNAnews", ["category", "url", "headline"])


class CNACrawler:
    def __init__(self):
        self.url = "https://www.cna.com.tw/cna2018api/api/WNewsList"
        self.json = {"action": "0", "category": "aall", "pageidx": 1}

    def get_list(self, category, pageidx):
        self.json["category"] = category
        self.json["pageidx"] = pageidx
        r = requests.post(self.url, json=self.json)
        # print(r.text)
        list = r.json()["ResultData"]["Items"]
        result = []
        for item in list:
            result.append(CNAnews(item["ClassName"], item["PageUrl"], item["HeadLine"]))
        return result

    def get_page(self, url):
        r = requests.get(url)
        DOM = BeautifulSoup(r.text, "html.parser")

        paragraphs = DOM.find("div", attrs={"class": "paragraph"})
        paragraphs = paragraphs.find_all("p")
        result = ""
        for paragraph in paragraphs:
            result = paragraph.text.strip()
        result=result[result.find('）')+1:result.rfind('（')]
        return result

    def get_news(self, category, pageidx, maxpage=0):
        news_list = self.get_list(category, pageidx)
        result = []
        if maxpage != 0:
            news_list = news_list[:maxpage]
        for i, news in enumerate(news_list):
            result.append(
                {
                    "headline": news.headline,
                    "content": self.get_page(news.url),
                    "url": news.url,
                    "category": news.category,
                }
            )
            print(f'getting news {i+1}/{len(news_list)}, {news.headline}')
        json.dump(result, open("cna.json", "w"), ensure_ascii=False)


if __name__ == "__main__":
    a = CNACrawler()
    result = a.get_news("aall", 1, 10)
