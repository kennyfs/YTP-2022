from pythonsrc import CrawlerCNA, CrawlerManager, YTP_Bot, tfidf
import datetime
import os


today = datetime.date.today()
todayDate = today.strftime("-%m-%d-%Y")
imageName = "cna-aipl" + todayDate + ".jpg"
JSON_Name = "cna-aipl" + todayDate + ".json"
 
if os.path.isfile(imageName) == False :
    yesterday =  today - datetime.timedelta(days=1)
    yesterdayDate = yesterday.strftime("-%m-%d-%Y")
    yesterdayImage = "cna-aipl" + yesterdayDate + ".jpg"
    if os.path.isfile(yesterdayImage) :
        os.remove(yesterdayImage)
    crawler = CrawlerCNA.CrawlerCNA()
    if os.path.isfile("cna-aipl" + yesterdayDate + ".json"):
        os.remove("cna-aipl" + yesterdayDate + ".json")
    if os.path.isfile(JSON_Name) == False :
        with CrawlerManager.CrawlerManager(crawler, JSON_Name) as manager:
            manager.getNewsByCategory("政治", 100)
    tfidf.getImage(JSON_Name, imageName)
YTP_Bot.run(imageName)
