from lxml import html
import requests
from pymongo import MongoClient

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}

site = 'https://sportmail.ru/news/football/'

response = requests.get(site, headers=header)
dom = html.fromstring(response.text)
blocks = dom.xpath("//a[contains(@class, 'newsitem__title link-holder')]")

news = []
for block in blocks:
    item = {}
    link = block.xpath(".//@href")[0]
    item['link'] = link
    item['title'] = block.xpath(".//span[@class = 'newsitem__title-inner']/text()")
    response_1 = requests.get(link, headers=header)
    dom_1 = html.fromstring(response_1.text)
    date = dom_1.xpath("//@datetime")[0]
    item['date'] = date.replace("T", " ").replace("+03:00", "")
    item['ist'] = dom_1.xpath("//span[@class = 'note']//span[@class = 'link__text']/text()")

    news.append(item)

site = 'https://lenta.ru/rubrics/sport/football/'
response = requests.get(site, headers=header)
dom = html.fromstring(response.text)
blocks = dom.xpath('//div[@class = "news"]')
news = []

for block in blocks:
    item = {}
    link = block.xpath(".//@href")[0]
    item['link'] = link
    item['title'] = block.xpath(".//a/text()")[0].replace('\xa0', ' ')
    item['source'] = site
    day = block.xpath("//div[@class = 'g-date']/text()")[0]
    time = block.xpath("//span[@class = 'time']/text()")[0]
    item['date'] = day, time

    news.append(item)

client = MongoClient('localhost', 27017)
db = client['news_db']
news_db = db.sport_news
news_db.insert_many(news)
