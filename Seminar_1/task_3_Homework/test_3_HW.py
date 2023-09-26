"""
Домашнее задание
Задание 1.
Добавить в задание с REST API еще один
тест, в котором создается новый пост,
а потом проверяется его наличие на сервере
по полю “описание”.
Подсказка:
Создание поста выполняется запросом
к https://test-stand.gb.ru/api/posts с передачей
параметров title, description, content.

"""

import requests
import yaml

S = requests.Session()

with open("config.yaml", encoding='utf-8') as f:
    data = yaml.safe_load(f)
    address_posts = data['address_posts']


def test_create_post(get_token):
    res = S.post(url=address_posts, headers={'X-Auth-Token': get_token},
                 data={'title': 'My pets', 'description': 'A post about my pets',
                       'content': 'My life could be much more calm| and easy without my cats.'
                                  'I could sleep longer in the morning and spend less time cleaning my house'
                                  'if I lived without my favourite cats. But all this can not be compared with  '
                                  'all love and tenderness, that they give us every day.'})

    assert res.ok


def test_rest(get_token, post_description):
    res = S.get(url=address_posts, headers={'X-Auth-Token': get_token}).json()['data']
    r = [i['description'] for i in res]

    assert post_description in r
