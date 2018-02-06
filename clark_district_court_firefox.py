# coding: utf-8
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from time import sleep
import os, logging


class Browser:
    
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        HOME=os.path.expanduser('~')
        download_dir=HOME+'/data/Courts/'
        log_dir = download_dir + 'logs/'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_name = log_dir + 'browser_errs.log'
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('clark_courts_firefox_browser')
        handler = logging.FileHandler(log_file_name)
        handler.setLevel(logging.WARN)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir",download_dir)
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/tiff;application/pdf")
        self.driver = webdriver.Firefox(firefox_options=options,firefox_profile=fp)
        self.driver.implicitly_wait(30)
        self.close = lambda: self.driver.close()
        self.login()
    
    def login(self):
        self.driver.get("https://www.clarkcountycourts.us/Portal/Account/Login")
        elem = self.driver.find_element_by_id("UserName")
        elem.clear()
        elem.send_keys(os.environ['CLARK_COURTS_USER'])
        elem = self.driver.find_element_by_id("Password")
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
        elem = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT,search_string)))
        if elem:
            elem.click()
            
    def download(self, search_string):
        self.logger.info('Downloading %s',search_string)
        self.search(search_string)
        section = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,"divDocumentsInformation_body")))
        if section:
            self.logger.debug('Found section')
            docs = section.find_elements_by_tag_name('p')
            downloaded = False
            if docs:
                self.logger.debug('Found docs')
                attempt = 1
                while not bool(downloaded):
                    for doc in docs:
                        try:
                            if 'Bindover' in doc.text:
                                attempt-=1
                                self.logger.debug('Found Bindover')
                                link = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT,"View Document")))
                                if link:
                                    self.driver.execute_script("arguments[0].click();", link)
                                    #link.click()
                                    sleep(5)
                                    elem = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT,"Download Document")))
                                    sleep(4)
                                    if elem:
                                        sleep(1)
                                        elem.click()
                                        downloaded = True
                                        break
                            elif attempt < len(docs):
                                sleep(3)
                                self.logger.debug('Finished attempt #%s',attempt)
                                self.logger.debug('Found document with title %s', doc.text)
                                attempt+=1
                                continue
                            else:
                                self.logger.warn('%s has no Bindover listed',search_string)
                                downloaded = True
                                break
                        except (StaleElementReferenceException,NoSuchElementException) as e:
                            self.logger.warn('StaleElementReference or NoSuchElement Exception triggered while parsing case: %s',search_string)
                            if attempt < 4:
                                sleep(3)
                                attempt+=1
                                continue
                            else:
                                self.logger.warn('%s had problems listing documents',search_string)
                                downloaded = True
                                break
                        except Exception as e:
                            self.logger.error('Unknown error downloading case %s',search_string,exc_info=True)
