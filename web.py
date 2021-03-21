from selenium import webdriver

# Указываем место где webdriver
# Версия 89.0.4389.90 (Официальная сборка), (64 бит)
# https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(
    executable_path=r'/home/nafanz/chromedriver'
)