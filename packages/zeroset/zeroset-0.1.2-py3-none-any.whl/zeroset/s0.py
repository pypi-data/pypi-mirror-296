import selenium
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
import os
from webdriver_manager.chrome import ChromeDriverManager
import shutil
import screeninfo

CHROME_DRIVER_PATH = ChromeDriverManager().install()


def get_selenium_driver(headless: bool = False, incognito: bool = False, download_dir: str = None) -> WebDriver:
    monitors = screeninfo.get_monitors()
    width, height = (monitors[0].width, monitors[0].height) if len(monitors) != 0 else (1024, 768)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('lang=ko')
    chrome_options.add_argument(f'window-size={width},{height}')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
    if incognito:
        chrome_options.add_argument('--incognito')
    if headless:
        chrome_options.add_argument('--headless=new')

    prefs = {
        "safebrowsing.enabled": True,
    }
    if download_dir is not None:
        download_dir = os.path.abspath(download_dir)
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        prefs["download.default_directory"] = download_dir
        prefs["download.prompt_for_download"] = False
        prefs["download.directory_upgrade"] = True
        prefs["profile.default_content_setting_values.automatic_downloads"] = 1
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(options=chrome_options, service=service)
    return driver


def get_element(element, key, value, timeout=30):
    WebDriverWait(element, timeout).until(EC.presence_of_element_located((key, value)))
    return element.find_element(key, value)


def get_elements(element, key, value, timeout=30):
    WebDriverWait(element, timeout).until(EC.presence_of_element_located((key, value)))
    return element.find_elements(key, value)


def get_alert_text(driver, timeout=30):
    WebDriverWait(driver, timeout).until(EC.alert_is_present())
    r = driver.switch_to.alert
    text = r.text
    r.accept()
    return text


def get_any_element(element, key1, value1, key2, value2, timeout=30):
    def any_of(*expected_conditions):
        def any_of_condition(driver):
            for idx, expected_condition in enumerate(expected_conditions):
                try:
                    result = expected_condition(driver)
                    if result:
                        return idx, result
                except WebDriverException:
                    pass
            return False

        return any_of_condition

    return WebDriverWait(element, timeout).until(any_of(
            EC.presence_of_element_located((key1, value1)),
            EC.presence_of_element_located((key2, value2))))


if __name__ == '__main__':
    driver = get_selenium_driver(headless=False, incognito=True)
    driver.get("")
    print(type(driver).__name__)
    driver.close()
    driver.quit()
