"""
С использованием фреймворка pytest написать тест операции checkText
SOAP API
Тест должен использовать DDT и проверять наличие определенного
верного слова в списке предложенных исправлений к определенному
неверному слову.
Слова должны быть заданы через фикстуры в conftest.py,
адрес wsdl должен быть вынесен в config.yaml.
Методы работы с SOAP должны быть вынесены в отдельную библиотеку.

"""
from Seminar_1.task_1.api_utils import check_text
import cgi


def test_step1(valid_word, invalid_word) -> None:
    assert valid_word in check_text(invalid_word), 'test_step1 FAIL'