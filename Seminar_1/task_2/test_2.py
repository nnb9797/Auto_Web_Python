"""
Написать тест с использованием pytest и requests, в котором:
● Адрес сайта, имя пользователя и пароль хранятся в config.yaml
● conftest.py содержит фикстуру авторизации по адресу
https://test-stand.gb.ru/gateway/login с передачей параметров
“username" и "password" и возвращающей токен авторизации
● Тест с использованием DDT проверяет наличие поста
с определенным заголовком в списке постов другого
пользователя, для этого выполняется get запрос по адресу
https://test-stand.gb.ru/api/posts c хедером, содержащим токен
авторизации в параметре "X-Auth-Token". Для отображения
постов другого пользователя передается "owner": "notMe".

"""

import requests
import yaml

with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)

S = requests.Session()


def test_step1(user_login, post_title):
    result = S.get(url=data["address"], headers={"X-Auth-Token": user_login}, params={"owner": "notMe"}).json()["data"]
    result_title = [i['title'] for i in result]
    assert post_title in result_title, 'test_step1 FAIL'

