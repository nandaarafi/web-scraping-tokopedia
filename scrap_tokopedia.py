import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys


def slow_scroll_down(driver, scroll_amount=600, delay=0.5):
    """
    Scroll down the webpage gradually in smaller increments.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        scroll_amount (int): The amount to scroll down in pixels.
        delay (float): The delay (in seconds) between scroll actions.
    """
    current_height = driver.execute_script("return window.pageYOffset;")
    max_height = driver.execute_script("return document.body.scrollHeight;")

    while current_height < max_height:
        new_height = current_height + scroll_amount
        if new_height > max_height:
            new_height = max_height

        driver.execute_script(f"window.scrollTo(0, {new_height});")
        time.sleep(delay)
        current_height = new_height


if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_term = ' '.join(sys.argv[1:])
    else:
        search_term = "Raspberry Pi 4"

    url = "https://www.tokopedia.com/"
    print("[INFO] Memulai Browser...")
    driver = webdriver.Chrome()
    print("[INFO] Browser berhasil dibuka.")
    driver.get(url)

    try:
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=search]')))
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.ENTER)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-1asz3by')))
        print("[INFO] Laman produk yang disearch ready!")
        print("[INFO] Scroll Web ...")

        #Scroll Down
        slow_scroll_down(driver)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        data = []
        for index, item in enumerate(soup.find_all('div', class_='css-1asz3by')):
            product_name_element = item.find('div', class_='prd_link-product-name css-3um8ox').text
            product_price = item.find('div', class_='prd_link-product-price css-h66vau').text

            product_location = item.find('span', class_='prd_link-shop-loc css-1kdc32b flip')
            product_location = product_location.text if product_location else np.nan

            product_shop_name = item.find('span', class_='prd_link-shop-name css-1kdc32b flip')
            product_shop_name = product_shop_name.text if product_shop_name else np.nan

            rate = item.find('span', class_='prd_rating-average-text css-t70v7i')
            rate = rate.text if rate else np.nan

            sold = item.find('span', class_='prd_label-integrity css-1sgek4h')
            sold = sold.text if sold else 0

            data.append({
                'Product': product_name_element,
                'Price': product_price,
                'Location': product_location,
                'Seller': product_shop_name,
                'Rating': rate,
                'Sold': sold
            })
            print(f"[INFO] Produk ke-{index}")

        df = pd.DataFrame(data)
        df.to_csv("produk.csv", index=False)
        print("[INFO] Data saved successfully to 'produk.csv'.")

    except TimeoutException:
        print("Loading took too much time or element not found.")

    finally:
        driver.quit()