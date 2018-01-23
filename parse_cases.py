# coding: utf-8
from clark_district_court_firefox import Browser

from subprocess import Popen, PIPE

from time import sleep

import random, os, csv

random.seed()

browser = Browser()

with open('/home/ubuntu/data/Courts/case_numbers.csv') as f:
    
    reader = csv.reader(f)
    
    next(reader, None) # skip header
    
    for row in reader:
        
        if len(row)>0:
            
            x = random.randint(53,135)
            
            y = random.randint(1,10)
            
            z = x+y
            
            case_number = row[0]
            
            tiff_file = case_number + '.tif'
            
            print("downloading",case_number)
            
            browser.download(case_number)
            
            process = Popen(['tesseract',tiff_file,case_number,'-l','eng','-psm','1','pdf'],cwd='/home/ubuntu/data/Courts/',stdout=PIPE, stderr=PIPE)
            
            sleep(z)
            
browser.close()
