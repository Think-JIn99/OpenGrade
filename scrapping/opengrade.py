from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import datetime as dt

ser = Service("C:/Users/rover0811/chromedriver.exe")  # 크롬 드라이버 잡아주는 것
op = webdriver.ChromeOptions()  # initial
op.add_experimental_option("excludeSwitches", ["enable-logging"])  # option 주기
op.add_argument('--window-size=1920,1080')
op.add_argument("headless")  # option 주기
s = webdriver.Chrome(service=ser, options=op)  # 초기화


s.get("https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Fsaint.ssu.ac.kr%2FwebSSO%2Fsso.jsp")

ID = s.find_element(By.ID, "userid")
PWD = s.find_element(By.ID, "pwd")
LoginButton = s.find_element(By.CLASS_NAME, 'btn_login')

ID.send_keys("")  # 학번
PWD.send_keys('')  # 비밀번호
LoginButton.click()

time.sleep(5)

학사관리Button = s.find_element(
    By.CSS_SELECTOR, "#ddba4fb5fbc996006194d3c0c0aea5c4 > a")

학사관리Button.click()

time.sleep(5)

성적졸업Button = s.find_element(
    By.CSS_SELECTOR, r"#\38 d3da4feb86b681d72f267880ae8cef5 > a")

성적졸업Button.click()

time.sleep(5)

s.switch_to.frame("URLSPW-0")
time.sleep(2)

s.find_element(By.CSS_SELECTOR, "#WD01C5").click()  # 여기서 에러가 나네?? 계절학기 이슈

time.sleep(5)
s.switch_to.parent_frame()

s.switch_to.frame("contentAreaFrame")
s.switch_to.frame("isolatedWorkArea")
s.find_element(By.CSS_SELECTOR, "#WD011C-btn").click()
s.find_element(By.CSS_SELECTOR, "#WD0161").click()  # 여기까지가 접근부

time.sleep(3)
html = s.page_source

soup = BeautifulSoup(html, 'html.parser')
tableitems = soup.select(
    '#WD0186-contentTBody')


tableitems = tableitems[0].find_all('tr')

data = {
    "index": [""],
    '이수학년도': [""],
    '이수학기': [""],
    '과목코드': [""],
    '과목명': [""],
    '과목학점': [""],
    '과목성적': [""],
    '과목등급': [""],
    '교수명': [""],
    '비고': [""],
}
# df = pd.DataFrame(data)
data = []
for i in tableitems:
    newitem = list()
    for k in i:
        newitem.append(str(k.text[:(len(k.text)//2)]))
    data.append(newitem)
    # df.loc[len(df)] = newitem
# for t in data:
#     print(t)

df = pd.DataFrame(data, columns=data[0])
df.to_excel("../result/result.xlsx")
v = open(
    "../result/seleniumpath.txt", "w+")
# v = open("./variables.txt", "w")
# f.write(str(tableitems))
v.write("ID: {0}\n".format(ID))
v.write("ID: {0}\n".format(PWD))
v.write("ID: {0}\n".format(LoginButton))
v.write("ID: {0}\n".format(학사관리Button))
v.write("ID: {0}\n".format(성적졸업Button))

v.close()

# v.write(str(PWD))
# v.write(str(LoginButton))
# v.write(str(학사관리Button))
# v.write(str(성적졸업Button))


# actions = webdriver.ActionChains(s).move_to_element(
#     닫기Button).click()

# _cookies = s.get_cookies()
# cookie_dict = {}
# for cookie in _cookies:
#     cookie_dict[cookie['name']] = cookie['value']
# print(cookie_dict)

# s.quit()
