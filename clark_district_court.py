# coding: utf-8
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

class Browser:
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.close = lambda: self.driver.close()
        self.login()
    
    def login(self):
        self.driver.get("https://www.clarkcountycourts.us/Portal/")
        sleep(5)
        elem = self.driver.find_element_by_id("dropdownMenu1")
        elem.click()
        elem = self.driver.find_element_by_link_text("Sign In")
        elem.click()
        elem = self.driver.find_element_by_name("UserName")
        elem.clear()
        elem.send_keys(os.environ['CLARK_COURTS_USER'])
        elem = self.driver.find_element_by_name("Password")
        elem.clear()
        elem.send_keys(os.environ['CLARK_COURTS_PASS'])
        elem = self.driver.find_element_by_class_name("Resizable")
        elem.click()
        
    def search(self, search_string):
        self.driver.get("https://www.clarkcountycourts.us/Portal/Home/Dashboard/29")
        elem = self.driver.find_element_by_id("caseCriteria_SearchCriteria")
        if elem:
            elem.clear()
            elem.send_keys(search_string)
        elem = self.driver.find_element_by_id("btnSSSubmit")
        if elem:
            elem.click()
        sleep(5)
        elem = self.driver.find_element_by_link_text(search_string)
        if elem:
            elem.click()
            
    def download(self, search_string):
        self.search(search_string)
        sleep(5)
        section = self.driver.find_element_by_id("divDocumentsInformation_body")
        if section:
            docs = lambda: section.find_elements_by_tag_name('p')
            link = ''
            downloaded = False
            if docs():
                for doc in docs():
                    while not bool(downloaded):
                        try:
                            if 'Bindover' in doc.text:
                                link = doc.find_element_by_link_text("View Document")
                                if link:
                                    link.click()
                                    elem = self.driver.find_element_by_link_text("Download Document")
                                    if elem:
                                        elem.click()
                                        downloaded = True
                                        sleep(2)
                                        break
                        except StaleElementReferenceException:
                            sleep(1)
                            continue
