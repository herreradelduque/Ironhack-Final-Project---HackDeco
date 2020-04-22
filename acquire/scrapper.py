import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import *
import urllib.request as ulib
from bs4 import BeautifulSoup

import os


# Function to save scrapped images:
def save_img(url, directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)

    for i, link in enumerate(url):
        path = os.path.join(directory, '{:04}.jpg'.format(i))
        try:
            ulib.urlretrieve(link, path)
        except:
            print('Failed saving images')
    print(f'Saved all the images at {directory}')


# Function to scrap Ikea furnitures
def ikea_scrapper():
    product_lst = ['Sillas']#,'Sofás']  # List of available products
    ## Driver
    # it is necessary to add the driver to the PATH variable
    os.environ['PATH'] = f'{os.environ["PATH"]}:{os.getcwd()}/drivers'

    # Dict of urls
    urls_dict = {'ikea': 'https://www.ikea.com/es/es/cat/productos-products/'}

    url = urls_dict.get('ikea')

    # Products tags:
    prod_tags_dict = {'Sillas': 'Todas las sillas','Sofás': 'Todos los sofás'}

    for index, product in enumerate(product_lst):
        directory = '../data/img_ikea_' + product_lst[index]  # Directory of images
        print(f'Selected product: {product.upper()}')


        # Launch driver:
        driver = webdriver.Firefox(executable_path=r'drivers/geckodriver')
        driver.get(url)

        product_tag = prod_tags_dict.get(product)

        try:

            link = driver.find_element_by_link_text(product_tag)
            link.click()
        except:
            print('We couldn\'t find the product in the website')

        time.sleep(1)

        try:
            count = 0
            while True:
                continue_link = driver.find_element_by_partial_link_text('Cargar más')
                continue_link.click()
                time.sleep(1)
                count += 1
                print(f'Load more: {count}')
            pass

        except:
            print('---------')
            pass

        finally:
            print('Loaded all the elements')
            pass


        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        image_list = []
        for link in soup.find_all('img'):
            src = link.get('src')
            if src.startswith('https://www.ikea.com/es/es/images/products/'):  # check src starts with...
                image_list.append(src)

        buy_url_list = []
        buy_url_list_unique = []
        all_a = soup.select('.product-compact__spacer a')
        for a in all_a:
            buy_url_list.append(a['href'])

        for i in buy_url_list:
            if i not in buy_url_list_unique:
                if 'openPopup=fiche' not in i:
                    buy_url_list_unique.append(i)

        images_path_list = []

        imgs_path = soup.select('div.product-compact__spacer span.product-compact__name')
        for i, img_path in enumerate(imgs_path):
            path = os.path.join(directory, '{:04}.jpg'.format(i))
            images_path_list.append(path)


        product_names_list = []
        names = soup.select('div.product-compact__spacer span.product-compact__name')
        for name in names:
            product_names_list.append(name.text)


        product_types_list = []
        types = soup.select('div.product-compact__spacer span.product-compact__type')
        for type in types:
            product_types_list.append(((type.text).replace('\n', '')).strip().replace('         ', ''))


        product_price_list = []
        prices = soup.select('div.product-compact__spacer span.product-compact__price__value')
        for price in prices:
            product_price_list.append(price.text)

        # Create DataFrame:
        scraped_dict = {'Type': product_types_list, 'Name': product_names_list, 'Price': product_price_list, 'Image_url': image_list, 'Buy_url': buy_url_list_unique,'Local_Path':images_path_list}

        furnitures_df = pd.DataFrame(scraped_dict)

        #furnitures_df_filtered = furnitures_df[furnitures_df['Type'].str.startswith(product[:-1])]

        # Save images filtered:
        save_img(furnitures_df['Image_url'], directory)

        # Save csv:

        furnitures_df.to_csv(f'../data/{product}.csv', index=False)

        # Close web browser:
        driver.close()

ikea_scrapper()