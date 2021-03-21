from web import driver

def authorization(object, username, password, login):
    '''
    Заполняем форму авторизации

    :param object: Название сайта
    :param username: Имя пользователя
    :param password: Пароль
    :param login: Кнопка "Войти"
    :return:
    '''
    driver.find_element_by_xpath(username).send_keys(f"{object['login']}")
    driver.find_element_by_xpath(password).send_keys(f"{object['password']}")
    driver.find_element_by_xpath(login).click()