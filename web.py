import os
from selenium import webdriver

home = os.getenv('HOME')

# Указываем место где webdriver
# https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(
    executable_path=f'{home}/chromedriver'
)