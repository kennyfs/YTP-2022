import requests
from bs4 import BeautifulSoup as beautifulSoup

websiteContent = requests.get("https://peienwu.com/").text
soup = beautifulSoup(websiteContent, "html.parser")
print(soup.prettify())
print(soup.title)
tagsOfA = soup.find_all("a")
for tag in tagsOfA:
    tagTitle = tag.string
    tagLink = tag.get("href")
    tagClass = tag.get("class")
    if tagClass != ["post-title-link"]:
        continue
    print(f"Title:{tagTitle}，Link:https://peienwu.com{tagLink}。")
