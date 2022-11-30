import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from webdriver_manager.chrome import ChromeDriverManager
from constant import *

import parse

class Saint:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.driver = self._init_driver()

        
    def _close_connection(self):
        self.session.close()
        self.driver.quit()
        

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-extensions")
        # options.add_argument('--disable-logging')
        options.add_argument('--blink-settings=imagesEnabled=false')
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
        options.add_argument("window-size=1920,1000")
        options.add_argument("lang=ko")
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)
    

    def _set_sap_token(self, stoken) -> None:
        login_cookies = {'sAddr':'', 'sToken':stoken, 'ASPSESSIONIDQCSDRQAQ':'', 'uid':''}
        self.session.get(f"{SAPTOKEN_URL}{stoken}", cookies=login_cookies)
        self.session.cookies['sToken'] = stoken
        self.session.cookies['Active'] = 'true'

    
    def _login_grade_page(self) -> str:
        try:
            self.driver.get(GRADE_URL)
            for cookie in self.session.cookies:
                self.driver.add_cookie({'name':cookie.name,'value':cookie.value,'path':'/'})

            self.driver.refresh()
            self.click_btn("SESSION_QUERY_CONTINUE_BUTTON")
            self.click_btn("WD0207") #팝업이 있을 경우 눌러준다.
            return "Success"
        
        except TimeoutError as e:
            print(e)
        
            
    def _find_until_load(self, timeout, find_func, *args):
        try:
            element = WebDriverWait(self.driver, timeout).until(find_func(args))
            return element
        
        except NoSuchElementException as e:
            print(e)
        
        except TimeoutException as e:
            print(e)

            
    def click_btn(self, btn_id):
        try:
            button = self._find_until_load(5, EC.element_to_be_clickable, By.ID, btn_id)
            if button:
                print(btn_id, button)
                button.click()
        
        except NoSuchElementException as e:
            print(e)
        
        except AttributeError as e:
            print(e)
        
        except TimeoutError:
            print(e)

            
    def _wait_content(self, content_selector):
        table = self.driver.find_element(By.ID, content_selector)
        def compare_element(driver):
            try:
                return table != driver.find_element(By.ID, content_selector)

            except WebDriverException:
                pass 

        WebDriverWait(self.driver, 5).until(compare_element)
    

    def _get_grade_page(self, year, semester):
        table_selector = 'WD01C4'
        try:
            years_button_id = "WD015E-btn"
            self.click_btn(years_button_id)
            
            first_year, first_year_id = 1954, int('160', 16)
            year_id = f"WD0{year - first_year + first_year_id:X}"
            self.click_btn(year_id)
            
            #로딩 대기
            self._wait_content(table_selector)

            semesters_button_id = "WD01B2-btn"
            self.click_btn(semesters_button_id)
            semester_id = f"WD0{int('1B4', 16) + semester:X}"
            self.click_btn(semester_id)
            
            #로딩 대기
            self._wait_content(table_selector)
            return self.driver.page_source
        
        except Exception as e:
            print(e)



def get_token():
    login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
    user_data = {
        "userid": "20180806",
        "pwd": "kidok0714!"
    }
    login_res = requests.post(login_url, data=user_data)
    token = login_res.cookies['sToken']
    return token


if __name__ == "__main__":
    saint = Saint()
    saint._set_sap_token(get_token())
    saint._login_grade_page()

    page_res = saint._get_grade_page()
    parse.parse_grade(page_res)
    saint._close_connection()
