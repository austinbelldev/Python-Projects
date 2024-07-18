import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sql_query

def scrape_aldi_products(url):
    
    combined_names = []
    prices = []

    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all product containers
        product_containers = soup.find_all('div', class_='product-tile')
        
        # Extract product name and price for each product
        for container in product_containers:
            product_brand = container.find('div', class_= 'product-tile__brandname').text.strip()
            product_name = container.find('div', class_='product-tile__name').text.strip()
            combined_name = f"{product_brand} {product_name}"
            product_price = container.find('span', class_='base-price__regular').text.strip()

            print("Product Brand and Name: ", combined_name)
            print("Product Price:", product_price)

            combined_names.append(combined_name)
            prices.append(product_price)
    else:
        print("Failed to retrieve the webpage.")

    return combined_names, prices

def scrape_all_pages():
    base_url = "https://new.aldi.us/products?page="
    total_pages = 153

    all_combined_names = []
    all_prices = []
    
    for page_num in range(1, total_pages + 1):
        url = base_url + str(page_num)
        print("Scraping page:", url)
        combined_names, prices = scrape_aldi_products(url)
        all_combined_names.extend(combined_names)
        all_prices.extend(prices) 

        time.sleep(1)

    return all_combined_names, all_prices

if __name__ == "__main__":
    combined_names, prices = scrape_all_pages()

    zipcode = sql_query.zipcode()

    df_aldi = pd.DataFrame({
        'area_code': zipcode,
        'store': 'Aldi',
        'item_name': combined_names,
        'item_price: ': prices
    })

    df_aldi.to_csv('Aldi_All_items.csv',index=False)
    print(df_aldi)

