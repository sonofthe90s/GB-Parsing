import requests
import json

username = input('Введите username: ')
main_link = f'https://api.github.com/users/{username}/repos'
response = requests.get(main_link)

if response.ok:
    data = response.json()
    for repo in data:
        print(repo['name'])
else:
    print(f'Такого пользователя нет. Начните сначала')

with open('dz1.json', 'w') as f:
    json.dump(data, f)
