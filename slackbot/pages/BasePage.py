import datetime
import os
import time
import unittest

import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures('setup_driver')
class BasePage(unittest.TestCase):

    @staticmethod
    def get_strategy(st):
        """
        maps strategy string to By
        """
        return getattr(By, st)

    def search(self, text):
        """
        Locate github search box and send text
        """
        search_box = self.driver.find_element(self.get_strategy(self.cfg['locators']['search']['q']['by']),
                                              self.cfg['locators']['search']['q']['selector'])
        # enter text
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.ENTER)

        return self

    def advanced_search_page(self):
        """
        Go to advance search page iff not on page
        """
        try:
            self.driver.find_element(
                self.get_strategy(self.cfg['locators']['advanced']['search']['page']['by']),
                self.cfg['locators']['advanced']['search']['page']['selector'])
        except NoSuchElementException:
            # locate advance search hypertext link and click
            adv_search_link = self.driver.find_element(
                self.get_strategy(self.cfg['locators']['search']['advanced']['by']),
                self.cfg['locators']['search']['advanced']['selector'])
            adv_search_link.click()
        return self

    def advanced_search_field(self, by, selector, value, submit=True):
        """
        Goto advanced search page, enter criteria and submit
        """
        # got to advanced search page
        self.advanced_search_page()

        # fill in the search criteria
        self.driver.find_element(self.get_strategy(by), selector).send_keys(value)

        # submit search criteria
        if submit:
            search_button = self.driver.find_element(self.get_strategy(self.cfg['locators']['search']['button']['by']),
                                                     self.cfg['locators']['search']['button']['selector'])
            search_button.click()
        return self

    def advanced_search_options(self, option, options, submit=True):
        """
        Goto advanced search page, select option and submit
        """
        # goto advanced search page
        self.advanced_search_page()

        # go to options dropdown
        self.driver.find_element(self.get_strategy(options['by']), options['selector']).click()

        # fill in the search criteria
        opt = option['selector'] % option['value']
        self.driver.find_element(self.get_strategy(option['by']), opt).click()

        # submit search criteria
        if submit:
            search_button = self.driver.find_element(self.get_strategy(self.cfg['locators']['search']['button']['by']),
                                                     self.cfg['locators']['search']['button']['selector'])
            search_button.click()
        return self

    def text_exists(self, text):
        return text in self.driver.page_source

    def link_exists(self, text):
        return self.driver.find_element(By.LINK_TEXT, text)
