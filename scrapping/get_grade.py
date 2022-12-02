
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from webdriver_manager.chrome import ChromeDriverManager #크롬 웹 브라우저 자동 설치를 위한 라이브러리

from constant import * 
import parse

import time

class Saint:
    """
    스크래핑을 진행하는 웹 드라이버 객체입니다.
    """
    def __init__(self, stoken:str) -> None:
        """
        객체 내부에서 사용하는 세션과 브라우저를 초기화 합니다.
        """
        self.session = self._get_login_session(stoken)
        self.driver = self._get_webdriver()

        
    def _close_connection(self):
        """
        연결 종료를 위해서 사용한다.
        """
        self.session.close()
        self.driver.quit()
        

    def _get_webdriver(self) -> webdriver.Chrome:
        """
        웹 드라이버를 옵션에 맞게 초기화 한후 반환 합니다.
        
        Returns:
            webdriver.Chrome: 브라우저 컨트롤 객체
        """
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") #CLI에서 실행
        options.add_argument('--no-sandbox') #GPU관련 작업 하지 않음
        options.add_argument('--disable-gpu') #GPU관련 작업 하지 않음
        options.add_argument('--disable-dev-shm-usage') #공유 메모리 사용하지 않음, 속도 개선을 위해
        options.add_argument("--disable-extensions") #크롬 확장 프로그램 사용하지 않음
        options.add_argument('--blink-settings=imagesEnabled=false') #이미지 로딩하지 않음
        # options.add_argument("window-size=1920,1000") #창 크기를 지정함 창 크기로 블락 당하는 경우가 존재.
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)
    

    def _get_login_session(self, stoken:str) -> None:
        """
        로그인을 진행하고 얻은 로그인 쿠키를 초기화된 드라이버에 저장합니다.

        Args:
            stoken (str):  API 서버에서 전달 받은 토큰
        """
        session = requests.Session()
        login_cookies = {'sAddr':'', 'sToken':stoken, 'ASPSESSIONIDQCSDRQAQ':'', 'uid':''} #로그인에 필요한 쿠키 형식
        session.get(f"{SAPTOKEN_URL}{stoken}", cookies=login_cookies)
        session.cookies['sToken'] = stoken #로그인 토큰 정보
        session.cookies['Active'] = 'true' #세션 활성화 여부
        return session


    def _set_driver_cookies(self):
        """
        웹 드라이버에 쿠키를 설정합니다.
        """
        self.driver.delete_all_cookies() #드라이버의 쿠키를 초기화
        for cookie in self.session.cookies:
            self.driver.add_cookie({'name':cookie.name,'value':cookie.value,'path':'/'})
    

    def _get_ec_element(self, expected_condtion:EC, By_:By, selector:str, ignored_exceptions:list=None, timeout:int=3):
        """
        대기를 진행하다 엘리먼트를 찾으면 반환 합니다.

        Args:
            expected_condtion (callable): 셀레니움 기대 조건 함수, 해당 조건을 만족할 때 까지 대기함
            By_ (By): 셀렉터 탐색 기준
            selector (str): 셀렉터
            ignored_exceptions (list, optional): 대기시 무시할 예외. Defaults to None.
            timeout (int, optional): 최대 대기시간. Defaults to 3.

        Returns:
            WebElement: 셀레니움 웹 엘리먼트
        """
        element = None
        try:
            #엘리먼트를 찾을 때까지 대기한다.
            element = WebDriverWait(self.driver, timeout, ignored_exceptions=ignored_exceptions).until(expected_condtion((By_, selector))) #엘리먼트가 로딩 될 떄까지 대기했다가 탐색
        
        except TimeoutException as e:
            print("EC Error", By_, selector,)
            print(e)
        
        finally:
            return element
    

    def _click_ec_element(self, By_:By, selector:str, ignored_exceptions:list=None, timeout:int=3):
        """
        엘리먼트 로딩을 대기하다 완료되면 클릭을 진행한다.

        Args:
            By_ (By): 셀렉터 선택 기준
            selector (str): 요소 셀렉터
            ignored_exceptions (list, optional): 대기시 무시할 예외. Defaults to None.
            timeout (int, optional): 최대 대기시간. Defaults to 3.

        Returns:
            WebElement: 셀레니움 웹 엘리먼트
        """
        try:
            #버튼의 로딩을 대기한다.
            button = self._get_ec_element(EC.element_to_be_clickable, By_, selector, ignored_exceptions, timeout)
            if button: 
                print(selector, button)
                button.click()
        
        #버튼을 누를 수 없다면
        except ElementNotInteractableException as e:
            print("Error: ", By_, selector)
            print(e)
        
        finally:
            return button

    
    def _load_grade_page(self) -> str:
        """
            브라우저에서 성적 페이지를 로딩 합니다. 
        """
        try:
            if self.driver.current_url != GRADE_URL:
                self.driver.get(GRADE_URL) 

            self._set_driver_cookies()
            self.driver.refresh()

            session_button_selector = "SESSION_QUERY_CONTINUE_BUTTON"
            popup_button_selector = ".urPWButtonTable div"

            #세션 재접속 버튼이 있는 경우
            session_button = self._click_ec_element(By.ID, session_button_selector)
            
            #팝업 버튼이 있는 경우
            popup_button = self._click_ec_element(By.CSS_SELECTOR, popup_button_selector)
            
        except Exception as e:
            print("login_problem")
            print(e)

            
    def wait_element_updated(self, selector:str):
        """
        성적 컨텐츠가 로딩 될 때까지 대기합니다.
        Args:
            content_selector (str): 컨텐츠 id
        """
        table = self._get_ec_element(EC.presence_of_element_located, By.CSS_SELECTOR, selector)
        def compare_table(driver):
            try:
                return table != driver.find_element(By.CSS_SELECTOR, selector)  #기존의 테이블과 다를때까지 반복
            except WebDriverException:
                pass 

        return WebDriverWait(self.driver, 2).until(compare_table)


    def _get_grade_page(self, year:str, semester:str):
        """
        유세인트에서 성적 정보를 스크래핑해 페이지 소스로 반환 합니다.

        Args:
            year (int): 유저가 요청한 년도
            semester (int): 유저가 요청한 학기 0: 1학기, 1: 여름학기, 2: 2학기, 3: 겨울학기

        Returns:
            page_resource: 성적정보를 포함한 페이지 html 소스
        """
        #성적 테이블의 id
        table_selector = 'td[class="urSTSStd"][id^="WD0"]'
        
        try:
            year_drop_selector = 'input[role="combobox"][value$="년도"]'
            year_selector = f'div[class="lsListbox__value"][data-itemkey="{year}"]'
            self._click_ec_element(By.CSS_SELECTOR, year_drop_selector)
            self._click_ec_element(By.CSS_SELECTOR, year_selector)
            
            #로딩 대기
            self.wait_element_updated(table_selector)
            
            semester_drop_selector = 'input[role="combobox"][value$="학기"]'
            semester_selector = f'div[class="lsListbox__value"][data-itemkey="09{semester}"]'
            self._click_ec_element(By.CSS_SELECTOR, semester_drop_selector, ignored_exceptions=[StaleElementReferenceException])
            self._click_ec_element(By.CSS_SELECTOR, semester_selector, ignored_exceptions=[StaleElementReferenceException])

            #로딩 대기
            self.wait_element_updated(table_selector)
            return self.driver.page_source
        
        except Exception as e:
            print(e)



def get_token(id_="", passwd="!"):
    login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
    user_data = {
        "userid": id_,
        "pwd": passwd
    }
    login_res = requests.post(login_url, data=user_data)
    token = login_res.cookies['sToken']
    return token


if __name__ == "__main__":
    saint = Saint(get_token("", ""))
    saint._load_grade_page()

    page_res = saint._get_grade_page('2021', '0')
    parse.parse_grade(page_res)

    # saint.session.get("https://ecc.ssu.ac.kr:8443/sap/public/bc/icf/logoff")
    # saint.session.close()

    # saint._get_login_session(get_token("20213118", "rlagustn1!"))
    # saint._load_grade_page()

    # page_res = saint._get_grade_page(2021, 2)
    # parse.parse_grade(page_res)

    # saint._close_connection()