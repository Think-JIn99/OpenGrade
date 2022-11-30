
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from webdriver_manager.chrome import ChromeDriverManager #크롬 웹 브라우저 자동 설치를 위한 라이브러리

from constant import * 
import parse

class Saint:
    """
    스크래핑을 진행하는 웹 드라이버 객체입니다.
    """
    def __init__(self) -> None:
        """
        객체 내부에서 사용하는 세션과 브라우저를 초기화 합니다.
        """
        self.session = requests.Session()
        self.driver = self._init_driver()

        
    def _close_connection(self):
        """
        연결 종료를 위해서 사용한다.
        """
        self.session.close()
        self.driver.quit()
        

    def _init_driver(self) -> webdriver.Chrome:
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
    

    def _set_sap_token(self, stoken:str) -> None:
        """
        로그인을 진행하고 쿠키 정보를 세션에 저장합니다.

        Args:
            stoken (str):  API 서버에서 전달 받은 토큰
        """
        login_cookies = {'sAddr':'', 'sToken':stoken, 'ASPSESSIONIDQCSDRQAQ':'', 'uid':''} #로그인에 필요한 쿠키 형식
        self.session.get(f"{SAPTOKEN_URL}{stoken}", cookies=login_cookies)
        self.session.cookies['sToken'] = stoken #로그인 토큰 정보
        self.session.cookies['Active'] = 'true' #세션 활성화 여부

    
    def _login_grade_page(self) -> str:
        """
            브라우저에서 성적 페이지를 로딩 합니다. 
        """
        try:
            self.driver.get(GRADE_URL) 
            for cookie in self.session.cookies:
                self.driver.add_cookie({'name':cookie.name,'value':cookie.value,'path':'/'})

            self.driver.refresh()
            self.click_btn("SESSION_QUERY_CONTINUE_BUTTON")
            self.click_btn("WD0207") #팝업이 있을 경우 눌러준다.
        
        #  추가적인 예외 처리 필요
        except TimeoutError as e:
            print(e)
        
            
    def _find_until_load(self, timeout:int, find_func, *args):
        """
        특정 엘리먼트가 로딩 될때까지 대기 한 후 찾아 반환 합니다.

        Args:
            timeout (int): 최대 대기 시간
            find_func (Callable[[tuple]]): 엘리먼트 탐색을 위해 사용할 함수

        Returns:
            WebElement: 셀레니움 웹 엘리먼트
        """
        element = None
        
        try:
            element = WebDriverWait(self.driver, timeout).until(find_func(args)) #엘리먼트가 로딩 될 떄까지 대기했다가 탐색
        
        except TimeoutException as e:
            print(e)
        
        finally:
            return element

            
    def click_btn(self, btn_id:str):
        """
        버튼을 로딩 대기하다 클릭 합니다.

        Args:
            btn_id (str): 버튼의 id
        """
        try:
            button = self._find_until_load(2, EC.element_to_be_clickable, By.ID, btn_id)
            print(btn_id)
            if button:
                button.click()
            else:
                raise NoSuchElementException
        
        except NoSuchElementException as e:
            print(e)

            
    def _wait_content(self, content_selector:str):
        """
        성적 컨텐츠가 로딩 될 때까지 대기합니다.

        Args:
            content_selector (str): 컨텐츠 id

        """
        table = self.driver.find_element(By.ID, content_selector)
        def compare_element(driver):
            try:
                #기존의 테이블과 다를때까지 반복
                return table != driver.find_element(By.ID, content_selector)

            except WebDriverException:
                pass 

        WebDriverWait(self.driver, 5).until(compare_element)
    

    def _get_grade_page(self, year:int, semester:int):
        """
        유세인트에서 성적 정보를 스크래핑해 페이지 소스로 반환 합니다.

        Args:
            year (int): 유저가 요청한 년도
            semester (int): 유저가 요청한 학기 0: 1학기, 1: 여름학기, 2: 2학기, 3: 겨울학기

        Returns:
            page_resource: 성적정보를 포함한 페이지 html 소스
        """
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
        "userid": "",
        "pwd": ""
    }
    login_res = requests.post(login_url, data=user_data)
    token = login_res.cookies['sToken']
    return token


if __name__ == "__main__":
    saint = Saint()
    saint._set_sap_token(get_token())
    saint._login_grade_page()

    page_res = saint._get_grade_page(2018, 1)
    parse.parse_grade(page_res)


    page_res = saint._get_grade_page(2019, 0)
    parse.parse_grade(page_res)

    page_res = saint._get_grade_page(2021, 2)
    parse.parse_grade(page_res)
    saint._close_connection()
