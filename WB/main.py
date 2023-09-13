from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from datetime import datetime
import wget
import os 

def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')    
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    return browser
    
data = {
    'title': [],
    'descr': [],
    'sale_price':[],
    'act_price':[],
    'quantity':[],
    'rate':[],
    'art':[],
    'product_img':[],
}

def get_item(articles):
    browser = get_browser()
    for article in articles:
        url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx'
        browser.get(url)
        time.sleep(2)
        page_data = browser.page_source    
        soup = BeautifulSoup(page_data, 'lxml')
        title = soup.find('div', 'product-page__header').text.strip()
        descr = soup.find('p', 'collapsable__text').text.strip()
        sale_price = soup.find('ins', 'price-block__final-price').text.strip()
        act_price = soup.find('del', 'price-block__old-price').text.strip()
        quantity = soup.find('p', 'product-order-quantity').text.strip()
        
        img_container = soup.find('ul', 'swiper-wrapper')
        imgs = img_container.find_all('img')
        
        imgs_path = ''
        for k,img in enumerate(imgs):
            img_file = download_image(title, k, img)
            
            if imgs_path == '':
                imgs_path = img_file
        
        if len(quantity) == 0:
            quantity = 'Нет покупок'
        rate = soup.find('span', 'address-rate-mini').text.strip()
        art = soup.find(name='span',id='productNmId').text.strip()
            
        data['title'].append(title)
        data['descr'].append(descr)
        data['sale_price'].append(sale_price)
        data['act_price'].append(act_price)
        data['quantity'].append(quantity)
        data['rate'].append(rate)
        data['art'].append(art)
        data['product_img'].append(imgs_path)
      
def download_image(product, k, img_obj):
    url = img_obj.get('src')
    
    if not os.path.exists('imgs'):
        os.mkdir('imgs')
    if not os.path.exists(f'imgs/{product}'):
        os.mkdir(f'imgs/{product}')
        
    filename = f'img_{k}.jpg'
    
    if not os.path.exists(f'imgs/{product}/{filename}'):
        wget.download('https:'+url, f'imgs/{product}/{filename}')
    return f'imgs/{product}'
        
    
    
def get_urls():
    
    with open('articles.txt','r', encoding='utf-8') as file:
        items = file.read()
        articles = items.split('\n')
        
    get_item(articles)
    save_to_excel(data)
    
    
def save_to_excel(items_data):
    df = pd.DataFrame(
        {
            'Название': items_data['title'],
            'Артикул': items_data['art'],
            'Описание': items_data['descr'],
            'Цена по скидке': items_data['sale_price'],
            'Цена без скидки': items_data['act_price'],
            'Купили раз': items_data['quantity'],
            'Оценка': items_data['rate'],
            'Папка с изображениями':data['product_img'],
        }
    )
    df.to_excel(f'result_{round(time.time())}.xlsx', index=False)

start = time.time()
get_urls()
print(time.time() - start)
