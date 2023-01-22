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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from bs4 import Comment
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait


# Globals

path = 'chromedriver.exe'
url = 'https://nces.ed.gov/collegenavigator/?s=IN'

class collegeIDScraper():
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
        self.collegeid_file = open('scraper_output.csv', 'w+', newline='', encoding='utf-8')
        self.collegeid_writer = csv.writer(self.collegeid_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    
    # Move to the next page
    def navigateToNextPage(self):
        nextPageXPATH = '//*[@id="ctl00_cphCollegeNavBody_ucResultsMain_divPagingControls"]/div/a'
        isNextPagePresent = len(self.driver.find_elements(By.XPATH, nextPageXPATH))
        if (isNextPagePresent>1):
            gotoNextPage =  WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, nextPageXPATH + '[2]')))
            ActionChains(self.driver).move_to_element(gotoNextPage).click().perform()
            self.grabIds()
        elif (self.driver.find_element(By.XPATH, nextPageXPATH).text == 'Next Page »'):
            gotoNextPage =  WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, nextPageXPATH)))
            ActionChains(self.driver).move_to_element(gotoNextPage).click().perform()
            self.grabIds()
        else:
            return

    # Traverse the current page and grab all college IDs and names
    def grabIds(self):
        # Find the results table
        resultsTable =  WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'resultsTable')))

        # Make soup of the results table
        resultsTableHtml = resultsTable.get_attribute('innerHTML')
        resultsTableSoup = BeautifulSoup(resultsTableHtml, 'html.parser')

        # Make list of all college ids
        results = resultsTableSoup.find_all("tr", {"class": (re.compile('results[WY]'))})
        for college in results:
            print("\ncontents[2]:")
            print(college.contents[2])
            print("\ncollege.contents[2].contents[0]")
            print(college.contents[2].contents[0])
            print("\nhref")
            print(college.contents[2].contents[0].get("href"))
            print("\nget_text:")
            print(college.contents[2].contents[0].get_text())
            print(college.contents[2].contents[2].get_text())
            print("\n\n\n")

        

        # Write to output file
        self.collegeid_writer.writerow([])
        # Move to next page
        self.navigateToNextPage()
        return


def main():
    bot = collegeIDScraper()
    bot.grabIds()
    # Close files and driver session
    bot.collegeid_file.close()
    bot.driver.close()
    bot.driver.quit()
    


            
if __name__ == "__main__":
    main()