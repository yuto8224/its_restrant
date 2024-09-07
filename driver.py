import os

from selenium import webdriver


def init_driver():
    options = webdriver.ChromeOptions()

    ...

    driver = webdriver.Remote(
        command_executor='http://{}:4444/wd/hub'.format(os.environ['SELENIUM_WORKER_HOST']),
        options=options
    )
    driver.set_window_size(500, 500)
    driver.implicitly_wait(10)

    return driver


def finish_driver(driver):
    driver.quit()