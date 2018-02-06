# coding: utf-8
from clark_district_court_firefox import Browser

from time import sleep

import random, os, csv

random.seed()

HOME=os.path.expanduser('~')

download_dir=HOME+'/data/Courts/'

cases=download_dir+'case_numbers.csv'

browser = Browser()

with open(cases) as f:
    
    reader = csv.reader(f)
    
    next(reader, None) # skip header
    
    for row in reader:
        
        if len(row)>0:
            
            x = random.randint(3,53)
            
            y = random.randint(1,10)
            
            z = x+y
            
            case_number = row[0]
            
            browser.download(case_number)
            
            sleep(z)
            
browser.close()
