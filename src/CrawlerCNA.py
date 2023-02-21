import collections
import re

import requests
from bs4 import BeautifulSoup

CrawlerResult = collections.namedtuple(
    "CrawlerResult", ["id", "url", "status", "category", "text", "headline", "outdated"]
)


class CrawlerCNA:
    url = "https://www.cna.com.tw/cna2018api/api/WNewsList"
    json = {"action": "0", "category": "aall", "pageidx": 1}
    abbrToCategories = {
        "aall": "即時",
        "aipl": "政治",
        "aopl": "國際",
        "acn": "兩岸",
        "aie": "產經",
        "asc": "證券",
        "ait": "科技",
        "ahel": "生活",
        "asoc": "社會",
        "aloc": "地方",
        "acul": "文化",
        "aspt": "運動",
        "amov": "娛樂",
    }
    categoriesToAbbr = {
        "即時": "aall",
        "政治": "aipl",
        "國際": "aopl",
        "兩岸": "acn",
        "產經": "aie",
        "證券": "asc",
        "科技": "ait",
        "生活": "ahel",
        "社會": "asoc",
        "地方": "aloc",
        "文化": "acul",
        "運動": "aspt",
        "娛樂": "amov",
    }

    def __init__(self):
        pass

    def get_list(self, category, pageidx):
        self.json["category"] = category
        self.json["pageidx"] = pageidx
        r = requests.post(self.url, json=self.json)
        list = r.json()["ResultData"]["Items"]
        result = []
        for item in list:
            result.append(item["Id"])
        return result

    def get_page(self, id):
        url = f"https://www.cna.com.tw/news/aall/{id}.aspx"
        r = requests.get(url)
        status = r.status_code
        if status != 200:
            return {"status": status, "text": None}
        DOM = BeautifulSoup(r.text, "html.parser")
        url, headline, category, text = self.pageinfo(DOM)
        text = re.sub(r"<a href='https[^']*'>|</a>", "", text)
        return {
            "url": url,
            "status": status,
            "category": category,
            "text": text,
            "headline": headline,
            "outdated": "您所瀏覽的新聞已過查詢時效" in r.text,
        }

    def get_news_by_list(self, category, pageidx, maxpage=0):
        if category in self.categoriesToAbbr:
            category = self.categoriesToAbbr[category]
        assert category in self.abbrToCategories, f"category {category} not found"
        news_list = self.get_list(category, pageidx)
        if len(news_list) == 0:
            return "ERROR"
        result = {}
        if maxpage != 0:
            news_list = news_list[:maxpage]
        for i, id in enumerate(news_list):
            result[id] = self.get_page(id)
            print(f"getting news {i+1}/{len(news_list)}")
        return result

    @staticmethod
    def pageinfo(DOM):
        url = DOM.find("meta", property="og:url")
        url = url["content"]
        headline = DOM.find("h1").text
        category = DOM.find("a", attrs={"class": "blue"}).text
        paragraphs = DOM.find("div", attrs={"class": "paragraph"})
        paragraphs = paragraphs.find_all("p")
        text = ""
        for paragraph in paragraphs:
            text += paragraph.text.strip()
        if text[0] == "（":
            text = text[text.find("）") + 1 :]
        elif text[0] == "(":
            text = text[text.find(")") + 1 :]
        text = text[: text.rfind("。") + 1]
        return url, headline, category, text

    def get_news_by_date(self, date, maxpage=0):
        num = 240
        length = 0
        result = {}
        margin = 10
        while True:
            if margin == 0:
                break
            id = f"{date}{num:04d}"
            r = self.get_page(id)
            print(r["status"])
            if r["status"] == 404:
                margin -= 1
                num += 1
                continue
            else:
                margin = 10
            result[id] = r
            print(f"getting news {id}")
            num += 1
            length += 1
            if maxpage != 0 and length == maxpage:
                break
        return result


if __name__ == "__main__":
    a = CrawlerCNA()
    a.get_page("https://www.cna.com.tw/news/afe/202002060380.aspx")
    a.get_news_by_date("20200206")
