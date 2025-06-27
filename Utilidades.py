from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from typing import List, Tuple, Union
from seleniumbase import Driver
from selenium import webdriver

def iniciar_driver(isHeadless: bool = None) -> WebDriver:
    # options = Options()
    # options.add_argument('--headless')
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("window-size=700,500")
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36")
    # options.add_argument("--start-maximized")
    # page = webdriver.Chrome(options=options)
    if isHeadless:
        page: WebDriver = Driver(browser='chrome', headless=isHeadless, uc=True)
    else:
        page: WebDriver = Driver(browser='chrome', headless=False, uc=True)
    page.maximize_window()
    return page

def iniciarDriver(isHeadless: bool = False):
    options = Options()
    if isHeadless:
        options.add_argument('--headless=new')
        
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36")
    options.add_argument('--window-size=1920,1080')
    # options.add_argument('--start-maximized')
    # For Windows
    service = Service(ChromeDriverManager().install())

    browser = webdriver.Chrome(service=service, options=options)
    return browser

def waitTo(driver, ByType: Tuple[str, str], time: int = 5, multiplesElements: bool = False) -> Union[WebElement, List[WebElement], None]:        
    try:
        if multiplesElements:
            return WebDriverWait(driver, time).until(
                EC.visibility_of_all_elements_located(ByType)
            )
        else:
            return WebDriverWait(driver, time).until(
                EC.visibility_of_element_located(ByType)
                # EC.presence_of_element_located(ByType)
            )
    except TimeoutException:
        if multiplesElements:
            return []
    return None