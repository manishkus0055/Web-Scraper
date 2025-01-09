# THIS FILE IS FOR ACTUAL AUTOMATING THE BROWSER AND DIFFERENT KIND OF LOGIN/REGISTER METHODS ON A SITE

import requests

from selenium import webdriver

from selenium.webdriver.common.proxy import Proxy, ProxyType

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import WebDriverException

def web_automation_normal(url):
    options = webdriver.FirefoxOptions()
    """ALL the options"""
    #options.proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': 'http.proxy:1234'})
    #options.add_argument("-headless")
    options.page_load_strategy = "normal"
    options.unhandled_prompt_behavior = 'accept and notify'

    driver = webdriver.Firefox(options=options)

    driver.get(url)
    driver.maximize_window()
    
    return driver.page_source
    
def web_automation_with_login(url, userid=None, password=None):
    options = webdriver.FirefoxOptions()
    """ALL the options"""
    #options.proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': 'http.proxy:1234'})
    #options.add_argument("-headless")
    options.page_load_strategy = "normal"
    options.unhandled_prompt_behavior = 'accept and notify'

    driver = webdriver.Firefox(options=options)

    driver.get(url)
    driver.maximize_window()
    
    driver.find_element(By.XPATH, "//*[@id='username']").send_keys(userid)
    driver.find_element(By.XPATH, "//*[@id='password']").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/main/div[2]/div[1]/div[2]/div/div/div/form/button").click()

    return driver.page_source

def web_automation_with_register_page(url, userid=None, password=None, confirm_password=None):
    options = webdriver.FirefoxOptions()
    """ALL the options"""
    #options.proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': 'http.proxy:1234'})
    #options.add_argument("-headless")
    options.page_load_strategy = "normal"
    options.unhandled_prompt_behavior = 'accept and notify'

    driver = webdriver.Firefox(options=options)

    driver.get(url)
    driver.maximize_window()
    
    driver.find_element(By.XPATH, "//*[@id='username']").send_keys(userid)
    driver.find_element(By.XPATH, "//*[@id='password']").send_keys(password)
    driver.find_element(By.XPATH, "//*[@id='confirmPassword']").send_keys(confirm_password)
    driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[2]/div/div/div/form/button").click()

    return driver.page_source
