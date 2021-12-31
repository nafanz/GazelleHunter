from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def web(mode):
    if mode == 'tor':
        options = Options()
        # Использование прокси, Tor Browser должен быть запущен
        options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
        # options.add_argument("headless")
        driver = webdriver.Chrome(
            ChromeDriverManager(log_level=0).install(),
            options=options
        )
    else:
        driver = webdriver.Chrome(ChromeDriverManager(log_level=0).install())

    return driver


def authorization(driver, object, username, password, login):
    driver.find_element(By.XPATH, username).send_keys(f"{object['login']}")
    driver.find_element(By.XPATH, password).send_keys(f"{object['password']}")
    driver.find_element(By.XPATH, login).click()


def send(driver, text, title, body, button):
    driver.find_element(By.XPATH, title).send_keys("Трекеры")
    driver.find_element(By.XPATH, body).send_keys(text)
    driver.find_element(By.XPATH, button).click()