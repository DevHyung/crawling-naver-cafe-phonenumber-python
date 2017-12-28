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
import pymysql
import re
reg = re.compile('\d{3}[-\.\s]??\d{4}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{4}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}')
#---DB연결
conn = pymysql.connect(ip,id,pw,name,charset="utf8")
curs = conn.cursor()
sql_jangpan = """insert into jangpan(content,url,tel)
                   values (%s, %s, %s)"""
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
    for pageidx in range(62,100):
        driver.get('http://cafe.naver.com/0404ab?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=18600855%26search.media=0%26search.searchdate=all%26search.defaultValue=1%26userDisplay=15%26search.option=0%26search.sortBy=date%26search.searchBy=0%26search.query=%B5%A5%C4%DA%C5%B8%C0%CF+%BD%C3%B0%F8+010%26search.viewtype=title%26search.page=' + str(1+pageidx))
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="cafe_main"]'))
        time.sleep(1)
        bs4 = BeautifulSoup(driver.page_source, "lxml")
        div = bs4.find('div', class_="article-board m-tcol-c")
        a = div.find_all('a', class_="m-tcol-c")
        for idx  in range (0,15):
            driver.get("http://cafe.naver.com/"+a[0+3*idx]['href'])
            driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="cafe_main"]'))
            time.sleep(1)
            bs4 = BeautifulSoup(driver.page_source,"lxml")
            div = bs4.find('div',class_="tbody m-tcol-c")
            try:
                results = reg.search(div.get_text()).group()
                curs.execute(sql_jangpan, (div.get_text(),"http://cafe.naver.com/"+a[0+3*idx]['href'], results))
                conn.commit()
            except:
                print("추출실패 : ","http://cafe.naver.com/"+a[0+3*idx]['href'])
                try:
                    curs.execute(sql_jangpan, (div.get_text(),"http://cafe.naver.com/" + a[0 + 3 * idx]['href'], ''))
                    conn.commit()
                except:
                    pass
            driver.execute_script("window.history.go(-1)")

    conn.close()