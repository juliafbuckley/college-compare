# Selenium-driven program to pull college ids from https://nces.ed.gov/collegenavigator/

# PLEASE NOTE: For cleanup, run cmd as admin and run ' taskkill /F /IM "chrome.exe" /T '
# This will kill all chrome processes.

# Imports
import sys
import os
import time
import string
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from bs4 import Comment
from fake_useragent import UserAgent


# Globals

path = 'chromedriver.exe'
url = 'https://nces.ed.gov/collegenavigator/?id=198419'

class collegeDetailsScraper():
    def __init__(self):

        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        
        # Fix access denied issue
        ua = UserAgent()
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')
        
        self.driver = webdriver.Chrome(executable_path=path, options=options)

        self.driver.get(url)

        # The 'a+' attribute makes it append.
        self.collegeid_file = open('college_details.csv', 'w+', newline='', encoding='utf-8')
        self.collegeid_writer = csv.writer(self.collegeid_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    
    def grabDetails(self):
        cols = ['Name', 'Address', 'Type', 'Awards offered', 'Campus setting', 'Campus housing', 'Student population', 'Student-to-faculty ratio']
        college_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="RightContent"]/div[4]/div/div[2]/span/span'))).text
        college_address = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="RightContent"]/div[4]/div/div[2]/span'))).text.split("\n")[1]
                
        collegeOverview = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="RightContent"]/div[4]/div/div[2]/table/tbody')))
        collegeOverviewHtml = collegeOverview.get_attribute('innerHTML')
        collegeOverviewSoup = BeautifulSoup(collegeOverviewHtml, 'html.parser')
        
        # Create dict of stat names and values
        college_stats = {}
        
        for stat in collegeOverviewSoup.find_all("tr"):
            k = stat.td.string.split(":")[0]
            if (k == ("General information" or "Website")):
                pass
            elif (k == ("Awards offered")):
                lst = [str(t) for t in stat.find_all("td")[1].contents]
                college_stats[k] = ''.join(lst).replace("<br/>", "/")
            else:
                v = stat.find_all("td")[1].string
                college_stats[k] = v
                
        new_row = [college_name, college_address]
        
        for c in cols[2:]:
            if c in college_stats:
                new_row.append(college_stats[c])
            else:
                new_row.append("")
        
        self.collegeid_writer.writerow(new_row)


def main():
    bot = collegeDetailsScraper()
    # ORIGINAL CODE
    bot.grabDetails()

    # Close files and driver session
    bot.collegeid_file.close()
    bot.driver.close()
    bot.driver.quit()
    exit()


            
if __name__ == "__main__":
    main()