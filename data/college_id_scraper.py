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
url = 'https://nces.ed.gov/collegenavigator/'

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
        self.collegeid_file = open('college_ids.csv', 'w+', newline='', encoding='utf-8')
        self.collegeid_writer = csv.writer(self.collegeid_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        
    def navigateToNextState(self, stateIndex):
        # If stateIndex is 60, all pages have been traversed and we return
        if (stateIndex >= 59):
            return
        # Define the select object on the page
        # TODO: stateindex = 60 breaks this part. figure out why
        try:
            select_state = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphCollegeNavBody_ucSearchMain_ucMapMain_lstState"]'))))
        except RecursionError:
            print("\n\nRecursionError occurred: stateIndex {}.".format(stateIndex))
            
        select_state.deselect_by_index(stateIndex-1)
        select_state.select_by_index(stateIndex)
        
        # Click for new results page
        showResultsPage = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphCollegeNavBody_ucSearchMain_btnSearch"]')))
        ActionChains(self.driver).move_to_element(showResultsPage).click().perform()
        
        stateIndex += 1
        
        # Grab the first page of ids
        self.grabIds(stateIndex)
    
    
    # Move to the next page
    def navigateToNextPage(self, stateIndex):
        nextPageXPATH = '//*[@id="ctl00_cphCollegeNavBody_ucResultsMain_divPagingControls"]/div/a'

        isNextPagePresent = len(self.driver.find_elements(By.XPATH, nextPageXPATH))
        
        # CASE: There is only one page of results
        if (isNextPagePresent==0):
            self.navigateToNextState(stateIndex)
            return

        
        if (isNextPagePresent>1):
            gotoNextPage =  WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, nextPageXPATH + '[2]')))
            ActionChains(self.driver).move_to_element(gotoNextPage).click().perform()
            self.grabIds(stateIndex)
        elif ('Next Page' in self.driver.find_element(By.XPATH, nextPageXPATH).text):
            gotoNextPage =  WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, nextPageXPATH)))
            ActionChains(self.driver).move_to_element(gotoNextPage).click().perform()
            self.grabIds(stateIndex)
        elif stateIndex < 60:
            self.navigateToNextState(stateIndex)
        else:
            return

    # Traverse the current page and grab all college IDs and names
    def grabIds(self, stateIndex):        
        # Find the results table
        resultsTable =  WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'resultsTable')))

        # Make soup of the results table
        resultsTableHtml = resultsTable.get_attribute('innerHTML')
        resultsTableSoup = BeautifulSoup(resultsTableHtml, 'html.parser')

        # Make list of all college ids
        results = resultsTableSoup.find_all("tr", {"class": (re.compile('results[WY]'))})
        college_id = ''
        college_name = ''
        college_loc = ''
        for college in results:
            #College ID
            college_id = college.contents[2].contents[0].get("href").split("=")[-1]
            # College Name
            college_name = college.contents[2].contents[0].get_text()
            # College Location
            college_loc = college.contents[2].contents[2].get_text()
            # Write to CSV
            self.collegeid_writer.writerow([college_id, college_name, college_loc])

        # Move to next page
        self.navigateToNextPage(stateIndex)


def main():
    bot = collegeIDScraper()
    # ORIGINAL CODE
    bot.navigateToNextState(1)

    # Close files and driver session
    bot.collegeid_file.close()
    bot.driver.close()
    bot.driver.quit()
    exit()


            
if __name__ == "__main__":
    main()