# coding: utf-8
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, localtime
import os

def time_now():
    (_,_,_,h,m,s,_,_,_) = localtime()
    time_now = ''
    for x in [h,m,s]:
        if x < 10:
            x = '0' + str(x)
        else:
            x = str(x)
        time_now+=x
        time_now+=':'
    time_now = time_now[:-1]
    return time_now
        
print('Start time:',time_now())
    
driver = webdriver.Chrome()

driver.get("https://www.clarkcountycourts.us/Portal/")
sleep(5)
elem = driver.find_element_by_id("dropdownMenu1")
elem.click()
elem = driver.find_element_by_link_text("Sign In")
elem.click()
elem = driver.find_element_by_name("UserName")
elem.clear()
elem.send_keys(os.environ['CLARK_COURTS_USER'])
elem = driver.find_element_by_name("Password")
elem.clear()
elem.send_keys(os.environ['CLARK_COURTS_PASS'])
elem = driver.find_element_by_class_name("Resizable")
elem.click()
elem = driver.find_element_by_id("portlet-29")
elem.click()
elem = driver.find_element_by_id("caseCriteria_SearchCriteria")
elem.click()
elem.clear()
elem.send_keys("C-13-287145-1")
elem = driver.find_element_by_id("btnSSSubmit")
elem.click()
sleep(5)
elem = driver.find_element_by_link_text("C-13-287145-1")
elem.click()
sleep(5)
elem = driver.find_element_by_link_text("Events and Hearings")
elem.click()
section = driver.find_element_by_id("divDocumentsInformation_body")
docs = section.find_elements_by_tag_name('p')
link = ''
for doc in docs:
    if 'Bindover' in doc.text:
        link = doc.find_element_by_link_text("View Document")

link.click()
print('Downloading Bindover')
elem = driver.find_element_by_link_text("Download Document")
elem.click() #Popup dialog for downloading?
elem = driver.find_element_by_link_text("Back")
elem.click()
elem = driver.find_element_by_id("tcControllerLink_0")
elem.click()

print('End time:',time_now())
choice = input("Hit return to exit...")
