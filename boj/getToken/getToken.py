from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import random

# user_id, user_pw 입력받아 사용
def getToken(user_id, user_pw):
    print('getToken() 호출')

    # 사용자 입력 (웹 페이지에서 전달받은 값으로 설정)

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 헤드리스 모드
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-automation");
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("window-size=1400,1500")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("start-maximized")
    #chrome_options.add_argument("enable-automation")
    #chrome_options.add_argument("--disable-infobars")
    #chrome_options.add_argument("--disable-dev-shm-usage")






    ###########
    # 블랙리스트 가능성 있음, 프록시/핫스팟를 이용한 IP주소 변경
    # 쿠키 저장
    ###########

    print('옵션 설정 완료')

    # 브라우저 드라이버 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print('드라이버 설정 완료')



    # 백준 로그인 페이지 접속
    driver.get("https://www.acmicpc.net/login?next=%2F")

    print('백준 로그인 페이지 접속 완료')


    # 쿠키 지우기
    driver.delete_all_cookies()
    print("모든 쿠키 삭제 완료")

    # 로컬 스토리지 지우기
    driver.execute_script("window.localStorage.clear();")
    print("로컬 스토리지 삭제 완료")


    # 랜덤 지연 추가
    time.sleep(random.uniform(1, 3))


    # 아이디와 비밀번호 입력
    try:
        id_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "login_user_id"))
        )
        pw_input = driver.find_element(By.NAME, "login_password")

        id_input.send_keys(user_id)
        pw_input.send_keys(user_pw)
    except Exception as e:
        print(f"아이디 비밀번호 입력 실패: {e}")
        driver.quit()
        exit()

    print('아이디 패스워드 입력 완료')

    # 랜덤 지연 추가
    time.sleep(random.uniform(1, 3))

    # 로그인 상태 유지 체크박스 선택
    try:
        remember_me_checkbox = driver.find_element(By.NAME, "auto_login")
        if not remember_me_checkbox.is_selected():
            remember_me_checkbox.click()
    except Exception as e:
        print(f"로그인 상태 유지 체크박스 선택 실패: {e}")
        driver.quit()
        exit()

    print('로그인 상태 유지 체크박스 선택 완료')

    # 랜덤 지연 추가
    time.sleep(random.uniform(1, 3))


    # 로그인 버튼 클릭
    try:
        login_go = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "submit_button"))
        )
        login_go.click()
    except Exception as e:
        print(f"오류 발생: {e}")
        driver.quit()
        exit()

    print('로그인 버튼 클릭 완료(로그인 완료 대기 중)')

    # 로그인 결과 대기
    try:
        WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.LINK_TEXT, "로그아웃"))
        )
    except Exception as e:
        print(f"로그인 후 로그아웃 요소를 찾는 데 실패하였습니다: {e}")
        driver.save_screenshot('login_error.png')


    print('로그인 완료')

    username = ''
    # username 가져오기
    try:
        element = WebDriverWait(driver, 200).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "username"))
        )
        username = element.text
    except Exception as e:
        print(f"username 가져오기 실패: {e}")
        driver.save_screenshot('login_error.png')
        # print(driver.page_source)

    print('username 가져오기 완료')

    # 특정 토큰 값 가져오기 (예: 로그인 후 쿠키 값)
    try:
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'bojautologin':
                token_value = cookie['value']
                print(f"bojautologin: {token_value}")
    except Exception as e:
        print(f"쿠키 가져오기 오류: {e}")

    # 브라우저 종료
    driver.quit()

    # 결과 리턴
    print(f'username : {username}, token : {token_value}')
    return {"username": username, "token": token_value}
