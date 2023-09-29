import yaml
import time
from HW_3.testpage import OperationsHelper
from HW_3.BaseApp import BasePage
import logging

with open("testdata.yaml", encoding="utf-8") as f:
    testdata = yaml.safe_load(f)


def test_login_negative(browser):
    logging.info("Test login_negative Starting")
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.enter_login("test")
    testpage.enter_pass("test")
    testpage.click_login_button()
    assert testpage.get_error_text() == "401", "test_login_negative FAILED"


def test_login_positive(browser):
    logging.info("Test login_positive Starting")
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.enter_login(testdata["login"])
    testpage.enter_pass(testdata["password"])
    testpage.click_login_button()
    assert testpage.login_success() == f"Hello, {testdata['login']}", "test_login_positive FAILED"


def test_add_post(browser):
    logging.info("Test add_post Starting")
    testpage = OperationsHelper(browser)
    # testpage.go_to_site()
    # testpage.enter_login(testdata["login"])
    # testpage.enter_pass(testdata["password"])
    # testpage.click_login_button()
    testpage.click_add_post_button()
    testpage.add_title(testdata["title"])
    testpage.add_description(testdata["description"])
    testpage.add_content(testdata["content"])
    testpage.click_save_post_button()
    testpage.find_new_post_title()
    assert testpage.find_new_post_title() == f"{testdata['title']}", "test add post FAILED"


"""
Добавить в проект тест по проверке механики работы формы Contact Us. Должно проверятся открытие формы, 
ввод данных в поля, клик по кнопке и появление всплывающего alert.
"""
def test_step4(browser):
    logging.info("Test4 Starting")
    testpage = OperationsHelper(browser)
    testpage.click_contact_us_link()
    time.sleep(5)
    testpage.enter_contact_name(testdata["contact_name"])
    testpage.enter_contact_email(testdata["contact_email"])
    testpage.enter_contact_form_content(testdata["contact_form_content"])
    testpage.click_save_contact_us_button()
    time.sleep(2)
    assert testpage.get_alert_text() == 'Form successfully submitted'



