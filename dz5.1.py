from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://m.mail.ru/login')

elem = driver.find_element_by_name('Login')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_name('Password')
elem.send_keys('NextPassword172')

elem.send_keys(Keys.RETURN)

button = driver.find_element_by_class_name('messageline__subject')
button.click()

mails = []
letter_num = 1
page = 1
while page <= letter_num:
    item = {}
    item['sender'] = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class = 'readmsg__text-container']//strong"))).text
    item['date'] = driver.find_element_by_class_name('readmsg__mail-date').text
    item['theme'] = driver.find_element_by_class_name('readmsg__theme').text
    item['letter_text'] = driver.find_element_by_id('readmsg__body').text
    mails.append(item)

    button = driver.find_element_by_class_name('readmsg__horizontal-block__right-block')
    button.click()

    page += 1

pprint(mails)
