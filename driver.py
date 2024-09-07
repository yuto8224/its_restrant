import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def init_driver():
    ##options = webdriver.ChromeOptions()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    driver = webdriver.Remote(
        command_executor='http://{}:4444/wd/hub'.format(os.environ['SELENIUM_WORKER_HOST']),
        options=options
    )
    driver.set_window_size(500, 500)
    driver.implicitly_wait(10)

    return driver


def finish_driver(driver):
    driver.quit()