"""
title           :main.py
description     :This will scrapping phone number by keyword search  in naver cafe
author          :DevHyung
date            :20171228
version         :1.0.0
usage           :python3 main.py
python_version  :3.6
required module :selenium+chromewebdriver
"""
from selenium import webdriver
from HEADER import *
import time
from bs4 import BeautifulSoup
import re
reg = re.compile('\d{3}[-\.\s]??\d{4}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{4}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}')
if __name__=="__main__":
    # Setting variable
    dir = './chromedriver'  # Driver Path
    driver = webdriver.Chrome(dir)
    # Login start
    driver.get("http://cafe.naver.com/0404ab") # target page
    driver.find_elements_by_xpath('//*[@id="gnb_login_button"]/span[3]')[0].click()
    driver.find_elements_by_xpath('//*[@id="id"]')[0].send_keys(NAVER_ID)
    driver.find_elements_by_xpath('//*[@id="pw"]')[0].send_keys(NAVER_PW)
    driver.find_elements_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input')[0].click()
    # Login end
    # Search start
    time.sleep(0.5)
    driver.find_elements_by_xpath('//*[@id="cafe-menu"]/div[2]/ul[2]/li[1]')[0].click()
    ## SwitchTo iframe
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="cafe_main"]'))
    time.sleep(0.5)
    driver.find_element_by_id('query').send_keys(KEYWORD)
    driver.find_elements_by_xpath('//*[@id="main-area"]/div[9]/form/a/img')[0].click()
    # Search end
    # Parsing start
    time.sleep(1)
    driver.find_elements_by_xpath('//*[@id="main-area"]/div[7]/form/table/tbody/tr[1]/td[2]/span/span/a')[0].click()
    time.sleep(1)
    bs4 = BeautifulSoup(driver.page_source,"lxml")
    div = bs4.find('div',class_="tbody m-tcol-c")
    results = reg.findall(div.get_text())
    print(div.get_text())
    print(results)
