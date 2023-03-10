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

path = 'chromedriver'
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
        # Expand to show all college info
        expand_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="RightContent"]/div[5]/div/a[1]')))
        expand_btn.click()

        # Turn into soup
        college_details = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="RightContent"]')))
        college_details_html = college_details.get_attribute('innerHTML')
        college_details_soup = BeautifulSoup(college_details_html, 'html.parser')
        
        # Get name and address
        college_name_address = list(college_details_soup.find("span", style="position:relative").stripped_strings)

        # Get name
        college_name = college_name_address[0]
        
        # Get address
        college_address = college_name_address[1]
        # Parse city, state, zip
        college_address_split = college_address.split(',')
        college_city = college_address_split[1].strip()
        college_state = ' '.join(college_address_split[2].strip().split(' ')[:-1])
        college_zip = college_address_split[2].strip().split(' ')[-1]
                
        # Get the 'type' and split into years and privacy
        college_years = ''
        college_privacy = ''
        college_awards = []
        college_setting = ''
        college_enrollment_tot = ''
        college_enrollment_ug = ''
        college_ratio = ''
        
        overview_tab = college_details_soup.find("table", class_="layouttab")
        for row in overview_tab.find_all("tr"):
            row_data = row.find_all("td")
            label = row_data[0].text.strip()
            info = row_data[1].text.strip()

            match label:
                case "Type:":
                    type_list = info.split(',')
                    college_years = type_list[0].strip()
                    college_privacy = type_list[1].strip()
                # Parse a list of all awards offered
                case "Awards offered:":
                    info = str(row_data[1])
                    college_awards = info.replace('<td>', '').replace('</td>', '').split('<br/>')
                # Parse campus setting
                case "Campus setting:":
                    college_setting = info
                # Get the total and undergrad student population
                case "Student population:":
                    enrollment_list = info.split(' ')
                    college_enrollment_tot = enrollment_list[0]
                    
                    if len(enrollment_list) > 1:
                        college_enrollment_ug = enrollment_list[1].replace('(', '')
                # Get the student-to-faculty ratio
                case "Student-to-faculty ratio:":
                    college_ratio = info.strip()
        
        # Scrape the values I want from the general info section
        has_rotc = False
        has_abroad = False
        ap_credit = False
        ib_credit = False
        general_info = college_details_soup.find("div", id="ctl00_cphCollegeNavBody_ucInstitutionMain_divNPC").text
        if "ROTC" in general_info:
            has_rotc = True
        if "Study abroad" in general_info:
            has_abroad = True
        if "AP" in general_info:
            ap_credit = True
        if "IB" in general_info:
            ib_credit = True

        tuition_info = college_details_soup.find("div", id="divctl00_cphCollegeNavBody_ucInstitutionMain_ctl00")
        tuition_total_element = tuition_info.find("tbody")
        print(tuition_total_element.tr.children)


                

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