from lxml import html
import requests
from pprint import pprint

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}

site = 'https://news.mail.ru'

response = requests.get(site, headers=header)

dom = html.fromstring(response.text)

# links = dom.xpath("//a[contains(@class, 'pm-logo__name')]/@href | //a[contains(@class, 'js-topnews__item')]/@href")
# result = dom.xpath("//td/div[contains(@class, 'daynews__item daynews__item_big')]/a/@href | //td//div[contains(@class, 'daynews__item')]/a/@href")
# result = dom.xpath("//a[contains(@class, 'js-topnews__item')]/@href")
blocks = dom.xpath("//a[contains(@class, 'js-topnews__item')]")

news = []
for block in blocks:
    item = {}
    name = block.xpath(".//span[contains(@class, 'js-topnews__notification')]/text()")
    links = block.xpath(".//a[contains(@class, 'js-topnews__item')]/@href")
    a = block.xpath(".//@href")[0]
    item['name'] = name
    item['links'] = links
    item['a'] = a
    news.append(item)

pprint(news)

