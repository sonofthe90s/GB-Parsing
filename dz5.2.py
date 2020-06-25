from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
from pprint import pprint
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru')

while True:
    try:
        next_button = driver.find_element_by_xpath(
            "(//div[@class='gallery-layout sel-hits-block '])[2]//a[@class='next-btn sel-hits-button-next']")
        actions = ActionChains(driver)
        actions.move_to_element(next_button).click(next_button).perform()
    except:
        break

hits_block = driver.find_elements_by_xpath(
    "(//div[@class='gallery-layout sel-hits-block '])[2]//a[@class='sel-product-tile-title']")
items = []
for item in hits_block:
    item = json.loads(item.get_attribute('data-product-info'))
    items.append(item)
    pprint(item)

client = MongoClient('localhost', 27017)
db = client['mvideo']
mvideo_db = db.mvideo_db
mvideo_db.insert_many(items)
