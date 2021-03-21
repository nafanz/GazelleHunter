from selenium import webdriver

# Использование прокси, Tor Browser должен быть запущен
options = webdriver.ChromeOptions()
# options.add_argument("headless")
options.add_argument('--proxy-server=socks5://127.0.0.1:9150')

# Указываем место где webdriver
driver = webdriver.Chrome(
    executable_path=r'/home/nafanz/chromedriver',
    chrome_options=options
)
