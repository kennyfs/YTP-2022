from pythonsrc import CrawlerCNA, CrawlerManager, YTP_Bot, tfidf

crawler = CrawlerCNA.CrawlerCNA()
with CrawlerManager.CrawlerManager(crawler, "cna-aipl.json") as manager:
    manager.getNewsByCategory("政治", 100)
tfidf.getImage("cna-aipl.json", "cna-aipl.jpg")
YTP_Bot.run("cna-aipl.jpg")
