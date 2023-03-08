from pythonsrc import CrawlerCNA, CrawlerManager, YTP_Bot, tfidf
import datetime
import os


today = datetime.date.today()
todayDate = today.strftime("-%m-%d-%Y")
imageName = "cna-aipl" + todayDate + ".jpg"

if os.path.isfile(imageName) == False :
    yesterday =  today - datetime.timedelta(days=1)
    yesterdayDate = yesterday.strftime("-%m-%d-%Y")
    yesterdayImage = "cna-aipl" + yesterdayDate + ".jpg"
    if os.path.isfile("/home/Astrayt/YTP-2022/" + yesterdayImage) :
        os.remove("/home/Astrayt/YTP-2022/" + yesterdayImage)
    crawler = CrawlerCNA.CrawlerCNA()
    with CrawlerManager.CrawlerManager(crawler, "cna-aipl.json") as manager:
        manager.getNewsByCategory("政治", 100)
    tfidf.getImage("cna-aipl.json", imageName)
YTP_Bot.run(imageName)
