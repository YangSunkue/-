from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager

from boj.core import constant
from boj.core.error import IllegalStatementError


class RemoteWebDriver:
    pass


def initialize_driver(
    browser: str,
    cache_manager: DriverCacheManager,
):
    if browser == "firefox":
        return webdriver.Firefox(
            service=Service(GeckoDriverManager(cache_manager=cache_manager).install()),
        )
    elif browser == "chrome":
        return webdriver.Chrome(
            service=Service(ChromeDriverManager(cache_manager=cache_manager).install()),
        )
    elif browser == "edge":
        return webdriver.Edge(
            service=Service(ChromeDriverManager(cache_manager=cache_manager).install()),
        )
    else:
        raise FatalError(f"{browser} is not a valid browser")




# 크롬 드라이버 관련 ##### 중요한 확인 사항 ######
# 각 유저 디렉터리 ( ~/.boj-cli/username ) 하위에 같은 양식의 크롬드라이버를 전부 넣어줘야 하는가?
# 아니면 크롬드라이버는 현상태처럼 상위 디렉터리에서 ( ~/.boj-cli ) 공유해도 문제가 없는가?
class Browser:
    driver: WebDriver
    url: str

    def __init__(self, url: str, browser: str):
        self.url = url
        driver_cache_manager = DriverCacheManager(root_dir=constant.boj_cli_path()) # 상위에? 하위에?

        self.driver = initialize_driver(browser, driver_cache_manager)
        self.driver.maximize_window()

    def open(self):
        self.driver.get(url=self.url)

    def close(self):
        self.driver.close()
