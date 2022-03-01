import datetime
import os
import time
import unittest

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures('setup_driver')
class BasePage(unittest.TestCase):

    @staticmethod
    def unique_message():
        dt = datetime.datetime.today().isoformat()
        return f"This is a unique msg [{dt}]"

    @staticmethod
    def get_strategy(st):
        """
        maps strategy string to By
        """
        return getattr(By, st)

    def select_channel(self, name):
        """
        Select channel from channels dropdown. Ensure that channels dropdown is
        expanded before proceeding
        """
        # check if channels is expanded
        side_menu = self.driver.find_element(self.get_strategy(self.cfg['locators']['channels']['dropdown']['by']),
                                             self.cfg['locators']['channels']['dropdown']['selector'])

        if not side_menu.get_attribute('aria-expanded'):
            self.driver.find_element(self.get_strategy(self.cfg['locators']['channels']['by']),
                                     self.cfg['locators']['channels']['selector']).click()
        # select channel
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((BasePage.get_strategy(self.cfg['locators']['channels'][name]['by']),
                                            self.cfg['locators']['channels'][name]['selector']))).click()
        return self

    def send_message(self, message):
        # select channel text editor
        msg_input = self.driver.find_element(self.get_strategy(self.cfg['locators']['texteditor']['by']),
                                             self.cfg['locators']['texteditor']['selector'])
        msg_input.click()
        msg_input.send_keys(message)
        msg_input.send_keys(Keys.ENTER)
        # allow time for message to propagate
        time.sleep(5)
        return self

    def search_saved_messages(self, message, refresh=True, wait_time=60):
        # wait for saved message to be indexed
        time.sleep(wait_time)
        # click on search box and enter 'has:star'
        self.driver.find_element(self.get_strategy(self.cfg['locators']['search_button']['by']),
                                 self.cfg['locators']['search_button']['selector']).click()

        search_box = self.driver.find_element(self.get_strategy(self.cfg['locators']['texteditor']['by']),
                                              self.cfg['locators']['texteditor']['selector'])
        search_box.send_keys('has:star')
        search_box.send_keys(Keys.ENTER)

        if refresh:
            # click on search box again and hit enter to allow refresh
            self.driver.find_element(self.get_strategy(self.cfg['locators']['search_button']['by']),
                                     self.cfg['locators']['search_button']['selector']).click()
            time.sleep(5)
            # locate 'has:start' in the suggestion list and click on it
            self.driver.find_element(By.XPATH, "//li[@data-replacement='has:star']").click()

        time.sleep(5)
        text = self.driver.find_element(self.get_strategy(self.cfg['locators']['search_results']['by']),
                                        self.cfg['locators']['search_results']['selector']).text
        print(f"Expected: {message}")
        print(f"Found: {text}")
        return text == message

    def save_message(self, message):
        # find message in message pane and perform save via mouse hover action
        g = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{message}')]")
        action = ActionChains(self.driver)
        action.move_to_element(g).perform()
        # allow time for hover action to complete
        time.sleep(3)

        # click save ribbon on popup bar
        self.driver.find_element(self.get_strategy(self.cfg['locators']['tool_tip']['save_message']['by']),
                                 self.cfg['locators']['tool_tip']['save_message']['selector']).click()
        # click save_messages button on side menu to display saved messages
        self.driver.find_element(self.get_strategy(self.cfg['locators']['saved_messages']['button']['by']),
                                 self.cfg['locators']['saved_messages']['button']['selector']).click()
        time.sleep(3)
        # check if save was successful by searching for message in saved messages
        text = self.driver.find_element(self.get_strategy(self.cfg['locators']['saved_messages']['text']['by']),
                                        self.cfg['locators']['saved_messages']['text']['selector']).text
        return text == message
