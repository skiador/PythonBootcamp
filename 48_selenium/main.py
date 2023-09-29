import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

STORE_ITEMS_IDS = ['buyElder Pledge', 'buyTime machine', 'buyPortal', 'buyAlchemy lab', 'buyShipment', 'buyMine', 'buyFactory', 'buyGrandma', 'buyCursor']


def buy_from_store():
    for store_item_id in STORE_ITEMS_IDS:
        try:
            store_item = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, store_item_id)))
            if store_item.get_attribute("class") == "grayed":
                pass
            else:
                store_item = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, store_item_id)))
                store_item.click()
        except selenium.common.exceptions.StaleElementReferenceException:
            pass


driver_options = webdriver.ChromeOptions()
driver_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=driver_options)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie_button = driver.find_element(By.ID, "cookie")

start_time0 = time.time()
start_time1 = time.time()
gap_time = 5
while time.time() - start_time0 < 300:
    cookie_button.click()
    if time.time() - start_time1 > gap_time:
        gap_time += 1
        start_time1 = time.time()
        buy_from_store()

cookies_per_second = driver.find_element(By.ID, "cps")
print(cookies_per_second.text)

driver.quit()

