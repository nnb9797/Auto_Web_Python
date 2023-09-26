import pytest
import requests
import yaml

with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)
    username, password, address = data['username'], data['password'], data['address']

S = requests.Session()


@pytest.fixture()
def get_token():
    res1 = S.post(url=address, data={'username': username, 'password': password})
    return res1.json()['token']


@pytest.fixture()
def post_description():
    return 'A post about my pets'
