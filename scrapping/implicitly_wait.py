from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException


import datetime as dt
ser = Service("C:/Users/rover0811/chromedriver.exe")  # 크롬 드라이버 잡아주는 것
op = webdriver.ChromeOptions()  # initial
op.add_experimental_option("excludeSwitches", ["enable-logging"])  # option 주기
op.add_argument('--window-size=1920,1080')
# op.add_argument("headless")  # option 주기
s = webdriver.Chrome(service=ser, options=op)  # 초기화
start_time = time.process_time()


s.get("https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Fsaint.ssu.ac.kr%2FwebSSO%2Fsso.jsp")

ID = s.find_element(By.ID, "userid")
PWD = s.find_element(By.ID, "pwd")
LoginButton = s.find_element(By.CLASS_NAME, 'btn_login')

ID.send_keys("학번 입력할 부분")  # 학번
PWD.send_keys('비밀번호 입력할 부분')  # 비밀번호
LoginButton.click()
# 학사관리 클릭
WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#ddba4fb5fbc996006194d3c0c0aea5c4 > a"))).click()
#성적/졸업 클릭
WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,r"#\38 d3da4feb86b681d72f267880ae8cef5 > a"))).click()
#닫기 창 누르기 위하여 iframe 바꾸기
WebDriverWait(s,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"URLSPW-0")))
#닫기 클릭
WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#WD01C5"))).click()
#iframe 이동
WebDriverWait(s,10)
s.switch_to.parent_frame()
WebDriverWait(s,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"contentAreaFrame")))
WebDriverWait(s,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"isolatedWorkArea")))
#2021학년도 클릭
WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#WD011C-btn"))).click()
#2학기 클릭
WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#WD0161"))).click()
#텍스트가 TBody에 들어올 때까지 대기
WebDriverWait(s,10).until(EC.text_to_be_present_in_element((By.ID,"WD0186-contentTBody"),"조회"))

html = s.page_source
soup = BeautifulSoup(html, 'html.parser')

tableitems = soup.find('tbody', {'id': "WD0186-contentTBody"})
# print(type(tableitems))
# print(tableitems)

soup = tableitems.find_all(
    'span', {"style": "white-space:normal;"})

scorelist = []
for index, value in enumerate(soup):
    if (index % 8 == 0):
        if (index == 0):
            low = list()
        else:
            scorelist.append(low)
            low = list()
    else:
        low.append(value.text)
df = pd.DataFrame(scorelist, columns=[
                  "이수학기", "과목코드", "과목명", "과목학점", "과목성적", "과목등급", "교수명"])
print(df)
df.to_excel("../result/practice.xlsx")
end_time = time.process_time()
print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")

