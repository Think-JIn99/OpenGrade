
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from webdriver_manager.chrome import ChromeDriverManager #크롬 웹 브라우저 자동 설치를 위한 라이브러리

from constant import * 
import parse
# from user import * #user id
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
        # options.add_argument("headless") #CLI에서 실행
        options.add_argument('no-sandbox') #GPU관련 작업 하지 않음
        options.add_argument('disable-gpu') #GPU관련 작업 하지 않음
        options.add_argument('disable-dev-shm-usage') #공유 메모리 사용하지 않음, 속도 개선을 위해
        options.add_argument("disable-extensions") #크롬 확장 프로그램 사용하지 않음
        options.add_argument('blink-settings=imagesEnabled=false') # 이미지 로딩하지 않음
        options.add_argument("disable-infobars")
        capabilities = DesiredCapabilities().CHROME
        capabilities['pageLoadStarategy'] = 'none'

        # prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
        # options.add_experimental_option('prefs', prefs)

        return webdriver.Chrome(ChromeDriverManager().install(), options=options, desired_capabilities=capabilities)
    

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
            self.driver.get(GRADE_URL) 
            self._set_driver_cookies()
            self.driver.refresh()

            session_button_selector = "SESSION_QUERY_CONTINUE_BUTTON"
            popup_button_selector = ".urPWButtonTable div"

            #세션 재접속 버튼이 있는 경우
            session_button = self._click_ec_element(By.ID, session_button_selector, ignored_exceptions=[StaleElementReferenceException])
            
            #팝업 버튼이 있는 경우
            popup_button = self._click_ec_element(By.CSS_SELECTOR, popup_button_selector,ignored_exceptions=[StaleElementReferenceException])
            
        except Exception as e:
            print("login_problem")
            print(e)

            
    def wait_table_updated(self):
        """
        성적 컨텐츠가 로딩 될 때까지 대기합니다.
        Args:
            content_selector (str): 컨텐츠 id
        """
        selector = 'tbody[id^="WD0"]' 
        # table = self._get_ec_element(EC.presence_of_element_located, By.CSS_SELECTOR, selector)
        table = self.driver.find_element(By.CSS_SELECTOR, selector)
        def compare_table(driver):
            try:
                return table != driver.find_element(By.CSS_SELECTOR, selector)  #기존의 테이블과 다를때까지 반복
            except WebDriverException:
                pass 
        
        try:
            return WebDriverWait(self.driver, 1).until(compare_table)
        
        except TimeoutException:
            print('Content Not loaded')
            return
        

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
        
        #드랍 다운 요소를 클릭하는 함수
        def click_drop_down(drop_down_selector, element_selector, ignored_exceptions=None):
            #클릭이 되지 않으면 최대 3번 진행
            for _ in range(3):
                #드랍다운 버튼을 클릭한다.
                drop_down_button = self._click_ec_element(By.CSS_SELECTOR, drop_down_selector, ignored_exceptions=ignored_exceptions, timeout=1)
                #요소를 클릭한다.
                element_button = self._click_ec_element(By.CSS_SELECTOR, element_selector, ignored_exceptions=ignored_exceptions, timeout=1)
                #버튼이 둘다 존재하면 둘다 클릭했으므로 그만한다.
                if drop_down_button and element_button: break

        try:
            #각 요소 선택을 위한 셀렉터
            year_drop_selector = 'input[role="combobox"][value^="20"]'
            year_selector = f'div[class~="lsListbox__value"][data-itemkey="{year}"]'

            semester_drop_selector = 'input[role="combobox"][value$="학기"]'
            semester_selector = f'div[class~="lsListbox__value"][data-itemkey="09{semester}"]'
            #년도와 학기 모두 변경해야하는 경우
            if year != YEAR and semester != SEMESTER:
                click_drop_down(year_drop_selector, year_selector)
                #다니지 않은 학기의 성적을 조회하려하면 예외가 발생한다.
                self._click_ec_element(By.CSS_SELECTOR, ".urPWButtonTable div", ignored_exceptions=[StaleElementReferenceException])
                #테이블만 업데이트 됐다면 바로 진행
                click_drop_down(semester_drop_selector, semester_selector, ignored_exceptions=[StaleElementReferenceException])

            else:
                #올해 성적을 쿼리할 경우 년도 버튼을 누를 필요는 없다.
                if year != YEAR:
                    click_drop_down(year_drop_selector, year_selector)

                #학기가 동일할 경우 학기 버튼을 누를 필요 없다.
                if semester != SEMESTER:
                    click_drop_down(semester_drop_selector, semester_selector)
            
            self.wait_table_updated()
            # self._get_ec_element(EC.presence_of_element_located, "tbody[id^="WD0"] > .rr")
            return self.driver.page_source

        except Exception as e:
            print("main", e)
            
    def _get_grade_page_year(self):
        def click_drop_down(drop_down_selector, element_selector, ignored_exceptions=None):
                #클릭이 되지 않으면 최대 3번 진행
                for _ in range(3):
                    #드랍다운 버튼을 클릭한다.
                    drop_down_button = self._click_ec_element(By.CSS_SELECTOR, drop_down_selector, ignored_exceptions=ignored_exceptions, timeout=1)
                    #요소를 클릭한다.
                    element_button = self._click_ec_element(By.CSS_SELECTOR, element_selector, ignored_exceptions=ignored_exceptions, timeout=1)
                    #버튼이 둘다 존재하면 둘다 클릭했으므로 그만한다.
                    if drop_down_button and element_button: break
        try:
            semester_drop_selector = 'input[role="combobox"][value$="학기"]'
            first_semester_selector = f'div[class~="lsListbox__value"][data-itemkey="090"]'
            self.wait_table_updated()
            second_semester_page_source=self.driver.page_source #2학기 성적은 변동이 필요없으므로 바로 받아온다.
            click_drop_down(semester_drop_selector, first_semester_selector)
            self.wait_table_updated()
            first_semester_page_source=self.driver.page_source

            return(first_semester_page_source,second_semester_page_source)
        except Exception as e:
            print("main", e)




    



#userid 입력 필요
def get_token(id_:str, passwd:str):
    login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
    user_data = {
        "userid": id_,
        "pwd": passwd
    }
    login_res = requests.post(login_url, data=user_data)
    token = login_res.cookies['sToken']
    return token


# if __name__ == "__main__":
#     saint = Saint(get_token())
#     saint._load_grade_page()

#     page_res = saint._get_grade_page('2021', '2')
#     # parse.parse_grade(page_res)

#     # page_res = saint._get_grade_page('2021', '0')
#     parse.parse_grade(page_res)

#     # page_res = saint._get_grade_page('2022', '1')
#     # parse.parse_grade(page_res)
#     # saint.session.get("https://ecc.ssu.ac.kr:8443/sap/public/bc/icf/logoff")

#     saint._close_connection()