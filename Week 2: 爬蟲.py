import requests as 要求
from bs4 import BeautifulSoup as 美麗的湯
取文字=要求.get
印=print
解析器='html.parser'

網頁文字=取文字('https://peienwu.com/').text
湯=美麗的湯(網頁文字,解析器)
#印(湯.prettify())
#印(湯.title)
a標籤=湯.find_all('a')
for 標籤 in a標籤:
    標題=標籤.string
    連結=標籤.get('href')
    類別=標籤.get('class')
    if(類別!=['post-title-link']):
        continue
    印(f'標題:{標題}，連結:https://peienwu.com{連結}')
