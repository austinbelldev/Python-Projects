from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

## Insert decimal into
def insert_decimal(value):
    numeric_value = ''.join(filter(str.isdigit, value))
    if len(numeric_value) < 2:
        numeric_value = '0' + numeric_value
    new_value = numeric_value[:-2] + '.' + numeric_value[-2:]
    return new_value

## Scroll Script
def ScrollToBottom():
    print("Scrolling to bottom...")
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("Bottom reached")

def ScrapeAll():
    department_number = 6
    while department_number < 18:
        driver.implicitly_wait(5)
        department_element = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div[1]/nav/ul/li[{department_number}]/a')
        department_element.click()
        ScrollToBottom()
        
        print("Scraping department...")
        
        all_products = driver.find_elements(By.CLASS_NAME, 'e-13udsys')
        for product in all_products:
            name = product.find_element(By.XPATH, './/*[@class="e-1eh94b4"]/h2').text
            price = product.find_element(By.XPATH, './/*[@class="e-0"]').text
            item = {
                'area_code': zipcode,
                'store': 'The Fresh Market',
                'item_name': name,
                'item_price': insert_decimal(price),
            }
            product_list.append(item)
        print("Next Department")

        department_number += 1

#
# MAIN
#

zipcode = input('Enter your zipcode: ')

# Opens Driver
url = 'https://shop.thefreshmarket.com/'
driver = webdriver.Firefox()
driver.get(url)

# Zipcode
driver.find_element(By.CSS_SELECTOR, "input[type='text' i]").send_keys(zipcode)
driver.find_element(By.CSS_SELECTOR, "input[type='text' i]").submit()

# In-Store
driver.implicitly_wait(5)
driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/header/div[2]/div[2]/button[3]').click()

## Creates Product List
product_list = []

## Scrapes Website
i = 1
ScrapeAll()

## Creates DF and Exports to CSV
df_tfm = pd.DataFrame(product_list)
df_tfm.to_csv('TFM_All_Items.csv',index=False)
print(df_tfm)

driver.close()
