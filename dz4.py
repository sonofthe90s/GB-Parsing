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


#     news_link = news_link if news_link.find('http') != -1 else site + news_link
#     item['link'] = news_link if news_link.find('http') != -1 else site + news_link
#     item['title'] = result.xpath(".//text()")[0].replace("\xa0", " ")
#     response1 = requests.get(news_link, headers=header)
#     dom1 = html.fromstring(response1.text)
#     date_time = dom1.xpath('.//@datetime')[0] if dom1.xpath('.//@datetime')[0] else 'Новость без даты'
#     item['date'] = date_time.replace("T", " ").replace("+03:00", "") if date_time else 'Новость без даты'
#     item['source'] = dom1.xpath('//span[@class="note"]//span[@class="link__text"]/text()')[0]
#     news.append(item)