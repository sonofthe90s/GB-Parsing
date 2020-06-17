from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient
# import json

main_link = 'https://hh.ru'

vacancies = []
search_vacancy = 'data scientist'
page = 0
while True:
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

    params = {'text': search_vacancy,
              'clusters': 'true',
              'enable_snippets': 'true',
              'salary': '',
              'st': 'searchVacancy',
              'fromSearch': 'true',
              'page': page}

    response = requests.get(main_link + '/search/vacancy/', params=params, headers=header)
    soup = bs(response.text, 'html.parser')

    vacancy_block = soup.find('div', {'class': 'vacancy-serp'})

    vacancy_list = vacancy_block.findChildren(recursive=False)

    for vacancy in vacancy_list:
        if vacancy['class'] == ['vacancy-serp-item'] or vacancy['class'] == ['vacancy-serp-item', 'vacancy-serp-item_premium']:
            link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
            company = vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'})
            company = company.text if company else None
            city = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'}).text
            name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
            salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).text
            if len(salary) == 0:
                min_salary, max_salary = float('nan'), float('nan')
                currency = [float('nan')]
            else:
                currency = re.search('([^\d]*$)', salary)
                _sal = salary.split('-')
                if len(_sal) == 1:
                    if 'от' in _sal[0]:
                        min_salary = re.sub('\D', '', _sal[0])
                        max_salary = float('nan')
                    else:
                        max_salary = re.sub('\D', '', _sal[0])
                        min_salary = float('nan')
                else:
                    min_salary = re.sub('\D', '', _sal[0])
                    max_salary = re.sub('\D', '', _sal[1])

            vacancy_data = {'link': link,
                            'company': company,
                            'city': city,
                            'name': name,
                            'min_salary': min_salary,
                            'max_salary': max_salary,
                            'cur': currency[0]}

            vacancies.append(vacancy_data)

    page += 1

    if soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}) is None:
        break

# with open("hh.json", "w", encoding="utf-8") as file:
#     json.dump(vacancies, file)
#
# with open('news.json', 'r', encoding='utf-8') as f:
#     text = json.load(f)
#     print(text)
# vac.insert_many(hh), {'upsert': True}

# Задание 1
client = MongoClient('localhost', 27017)
db = client['hh']
hh = db.vacancies
hh.insert_many(vacancies)

# Задание 2
limit = float(input('Введите желаемую минимальную зарплату: '))

def vacancies_request(limit):
    for vacancy in hh.find({'$or': [{'min_salary': {'$gt': limit}}, {'max_salary': {'$gt': limit}}]}):
        print(vacancy)
