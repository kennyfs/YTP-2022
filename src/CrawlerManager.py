import json
from datetime import timedelta

import CrawlerCNA


class CrawlerManager:
    def __init__(self, crawler, filename):
        self.crawler = crawler
        self.filename = filename
        self.fileIO = None
        self.json = {}

    def __enter__(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as self.fileIO:
                self.json = json.load(self.fileIO)
        except:
            pass
        self.fileIO = open(self.filename, "w")
        return self

    def __exit__(self, type, value, traceback):
        json.dump(self.json, self.fileIO, ensure_ascii=False)
        self.fileIO.close()

    def getNewsByDate(self, start, end, max_pages=0):
        date = start
        end_date = end
        delta = timedelta(days=1)
        accumulated = 0
        while date <= end_date:
            date_str = date.strftime("%Y%m%d")
            print(date_str)
            date += delta
            data = self.crawler.get_news_by_date(date_str, max_pages - accumulated)
            self.json.update(data)
            accumulated += len(data)
            if accumulated >= max_pages:
                break

    def getNewsByCategory(self, category, max_pages=0):
        i = 1
        accumulated = 0
        while True:
            data = self.crawler.get_news_by_list(category, i, max_pages - accumulated)
            if data == "ERROR":
                break
            self.json.update(data)
            accumulated += len(data)
            if accumulated >= max_pages:
                break


if __name__ == "__main__":
    crawler = CrawlerCNA.CrawlerCNA()
    # with CrawlerManager(crawler, 'cna-date-20190101(example).json') as manager:
    # 	manager.getNewsByDate(date(2019, 1, 1), date(2019, 1, 1), 10)
    with CrawlerManager(crawler, "cna-category-aipl(example).json") as manager:
        manager.getNewsByCategory("政治", 100)
