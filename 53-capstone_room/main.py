import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



ROOMS_URL = "https://www.idealista.com/alquiler-habitacion/madrid/chamberi/con-sexo_chico,compartidos_con-trabajadores/pagina-{}.htm"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdJ5rrzOybzThe-Lr8uOpFWzyJEsQunVg_NywRzsyCqOi6J_Q/viewform?usp=sf_link"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
}
address = []
price = []
link = []


def get_rooms_from_page(address_list, links_list, prices_list):
    item_links_elements = soup.select("div.item-info-container  a.item-link")
    item_price_elements = soup.find_all(class_="item-price h2-simulated")
    for item in item_links_elements:
        room_address = item.get_text(strip=True)
        room_link = f"https://idealista.com{item.get('href')}"
        address_list.append(room_address)
        links_list.append(room_link)
    for item in item_price_elements:
        room_price = int(item.get_text(strip=True).strip("€/mes").replace(".", ""))
        prices_list.append(room_price)


for i in range(3):
    print(f"Page {i+1}")
    connection = requests.get(ROOMS_URL.format(i+1), headers=headers)
    connection.raise_for_status()
    soup = BeautifulSoup(connection.text, "html.parser")
    get_rooms_from_page(address, link, price)

print(len(address))
print(address)
print(len(price))
print(price)
print(len(link))
print(link)


driver_options = webdriver.ChromeOptions()
driver_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=driver_options)

driver.get(FORM_URL)

time.sleep(2)


for i in range(len(address)):
    address_input_item = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                             '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))

    price_input_item = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                           '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    link_input_item = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                          '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    send_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')))

    address_input_item.send_keys(address[i])
    price_input_item.send_keys(price[i])
    link_input_item.send_keys(link[i])
    send_button.click()
    new_form_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))
    new_form_button.click()

driver.quit()