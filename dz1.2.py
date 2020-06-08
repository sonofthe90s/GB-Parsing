import requests
import json

method_name = 'users.getFollowers'
main_link = f'https://api.vk.com/method/{method_name}'
user_id = '3133347'
params = {'user_id': user_id,
          'v': '5.52',
          'access_token': 'токен удален'}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Accept': '*/*'}

response = requests.get(main_link, params=params, headers=header)

if response.ok:
    data = response.json()
else:
    print(f'Такого пользователя нет. Начните сначала')

with open('dz2.json', 'w') as f:
    json.dump(data, f)
