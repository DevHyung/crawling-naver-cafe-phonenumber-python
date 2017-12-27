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
NAVER_ID = "PUT_YOUR_NAVER_ID"
NAVER_PW = "PUT_YOUR_NAVER_PW"
if __name__=="__main__":
    dir = './chromedriver'  # Driver Path
    driver = webdriver.Chrome(dir)
    driver.get("https://cafe.naver.com/0404ab") # target page
    driver.find_elements_by_xpath('//*[@id="gnb_login_button"]/span[3]')[0].click()
    driver.find_elements_by_xpath('//*[@id="id"]')[0].send_keys(NAVER_ID)
    driver.find_elements_by_xpath('//*[@id="pw"]')[0].send_keys(NAVER_PW)
    driver.find_elements_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input')[0].click()
