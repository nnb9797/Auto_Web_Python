from requests import JSONDecodeError

from HW_4.BaseApp import BasePage, BaseRestApiSession
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
import logging
import yaml


class TestSearchLocators:
    """Locators keeping class"""
    ids = dict()
    with open("locators.yaml", encoding="utf-8") as f:
        locators = yaml.safe_load(f)

    for locator in locators["xpath"].keys():
        ids[locator] = (By.XPATH, locators["xpath"][locator])

    for locator in locators["css"].keys():
        ids[locator] = (By.CSS_SELECTOR, locators["css"][locator])


class OperationsHelper(BasePage):
    """Класс, содержащий методы для работы с элементами на веб-страницах"""

    #  EXCEPTIONS
    def enter_text_into_field(self, locator, word, description=None):
        """Text entering function"""
        if description:
            element_name = description
        else:
            element_name = locator
        logging.info(f"Send {word} to element {element_name}")

        field = self.find_element(locator)
        if not field:
            logging.debug(f"Element {locator} is not found")
            return False
        try:
            field.clear()
            field.send_keys(word)
        except TimeoutException:
            logging.exception(f"Exception while operation with {locator}")
            return False

        return True

    def click_button(self, locator, description):
        """Вспомогательный метод для методов нажатия на кнопку"""
        if description:
            element_name = description
        else:
            element_name = locator

        button = self.find_element(locator)
        if not button:
            return False

        try:
            button.click()
        except TimeoutException:
            logging.exception("Exception with click button")

        logging.debug(f"Clicked {element_name}")
        return True

    def get_text_from_element(self, locator, description=None):
        """Вспомогательный метод для методов возврата текста из элемента"""
        if description:
            element_name = description
        else:
            element_name = locator

        field = self.find_element(locator, time=3)
        if not field:
            return None

        try:
            text = field.text
        except TimeoutException:
            logging.exception(f"Exception while getting a test from {element_name}")
            return None

        logging.debug(f"Found text {text} in field {element_name}")
        return text

    # ENTERING TEXT
    def enter_login(self, word):
        """Entering a login in an authorisation field"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_LOGIN_FIELD'], word,
                                   description="Entering a login in an authorisation field")

    def enter_pass(self, word):
        """Entering a password in an authorisation field"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_PASS_FIELD'], word,
                                   description="Entering a password in an authorisation field")

    def enter_post_title(self, word):
        """Entering a post title in a creating post form"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_FORM_POST_TITLE'], word,
                                   description="Entering a post title in a creating post form")

    def enter_post_description(self, word):
        """Entering a post description in a creating post form"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_FORM_POST_DESCRIPTION'], word,
                                   description="Entering a post description in a creating post form")

    def enter_post_content(self, word):
        """Entering post content in a creating post form"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_FORM_POST_CONTENT'], word,
                                   description="Entering post content in a creating post form")

    def enter_username_contact_us_form(self, word):
        """Entering username in a contact us form"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_USERNAME_FIELD_CONTACT_US_FORM'], word,
                                   description="Entering username in a contact us form")

    def enter_email_contact_us_form(self, word):
        """Entering an email in a contact us form"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_EMAIL_FIELD_CONTACT_US_FORM'], word,
                                   description="Entering an email in a contact us form")

    def enter_content_contact_us_form(self, word):
        """Entering content in a contact us form'"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_CONTENT_FIELD_CONTACT_US_FORM'], word,
                                   description="Entering content in a contact us form")

    #  GET TEXT
    def get_error_text(self):
        """Getting an error text from authorization page"""
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_ERROR_FIELD'],
                                          description="Getting an error text from authorization page")

    def get_login_text(self):
        """Getting user's name"""
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_USER_PROFILE_LINK'],
                                          description="Get login")

    def get_post_title(self):
        """Getting user's post name"""
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_POST_NAME'],
                                          description="Getting user's post name")

    def get_alert(self):
        """Get alert text after sending Contact us form"""
        logging.info("Get alert text")
        text = self.get_alert_text()
        logging.info(text)
        return text

    #  CLICK BUTTON
    def click_login_button(self):
        """Clicking Login button"""
        self.click_button(TestSearchLocators.ids['LOCATOR_LOGIN_BTN'],
                          description="Clicking Login button")

    def click_create_post_button(self):
        """Clicking post creation button"""
        self.click_button(TestSearchLocators.ids['LOCATOR_CREATE_POST_BTN'],
                          description="Clicking post creation button")

    def click_save_post_button(self):
        """Clicking post saving button"""
        self.click_button(TestSearchLocators.ids['LOCATOR_SAVE_POST_BTN'],
                          description="Clicking post saving button")

    def click_contact_us_button(self):
        """Clicking Contact Us Form opening button"""
        self.click_button(TestSearchLocators.ids['LOCATOR_CONTACT_FORM_BTN'],
                          description="Clicking Contact Us Form opening button")

    def click_send_contact_us_form(self):
        """Clicking Sending Contact Us form button"""
        self.click_button(TestSearchLocators.ids['LOCATOR_SEND_CONTACT_US_FORM_BTN'],
                          description="Clicking Sending Contact Us form button")


class RestHelper(BaseRestApiSession):
    """Class contains REST API requests work methods"""

    def get_user_token(self):
        """Authorization and getting token function"""
        token = ''
        try:
            token = self.login()
        except KeyError:
            logging.exception(f'Failed user {self.user_name} login')
        except JSONDecodeError:
            logging.exception(f"404 not found!")

        return token

    def get_post(self, url_posts):
        """Getting list of all users' posts function"""
        logging.info("Getting list of all users' posts...")

        token = self.get_user_token()
        results = []

        try:
            data = self.session.get(url=url_posts,
                                    headers={'X-Auth-Token': token},
                                    params={'owner': 'notMe'}).json()['data']
            results = [i['title'] for i in data]
        except KeyError:
            logging.exception("Wrong token in GET request")

        if len(results) > 0:
            logging.info("Success")
        else:
            logging.info("List with posts is empty!")

        return results

    def new_post(self, url_posts, title, description, content):
        """New post creation function"""
        logging.info("Creating a new post...")

        token = self.get_user_token()
        descriptions = []

        try:
            self.session.post(url=url_posts,
                              headers={'X-Auth-Token': token},
                              data={'title': title, 'description': description, 'content': content})
            posts_info = self.session.get(url=url_posts,
                                          headers={'X-Auth-Token': token}).json()['data']
            descriptions = [i['description'] for i in posts_info]
        except KeyError:
            logging.exception("Wrong data in requests")

        if len(descriptions) > 0:
            logging.info("Success")
        else:
            logging.info("Post creation failed!")

        return descriptions