# coding: utf-8
from clark_district_court_firefox import Browser

from time import sleep

import random, os, csv

def sorted_dir(folder):
    def getmtime(name):
        path = os.path.join(folder, name)
        return os.path.getmtime(path)

    return sorted(os.listdir(folder), key=getmtime, reverse=True)

random.seed()

HOME=os.path.expanduser('~')

download_dir=HOME+'/data/Courts/'

cases=download_dir+'case_numbers.csv'

os.chdir(download_dir)

most_recent_tiff=lambda x: sorted_dir(x)[0].split('.')[0]

case_nums=[x.strip() for x in open(cases).readlines()[1:]]

limit=0 # don't download previously saved cases

browser = Browser()

most_recent_index=case_nums.index(most_recent_tiff(download_dir))

with open(cases) as f:
    
    reader = csv.reader(f)

    for row in reader:
        
        if limit<=most_recent_index:

            limit+=1

            continue

        else:

            if len(row)>0:
            
                x = random.randint(3,53)
            
                y = random.randint(1,10)
            
                z = x+y
            
                case_number = row[0]
            
                browser.download(case_number)

                sleep(z)
            
browser.close()
