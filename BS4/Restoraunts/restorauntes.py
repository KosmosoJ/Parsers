import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pathlib import Path
import os
from typing import Dict
from selenium.webdriver.common.by import By
import glob
from fake_useragent import UserAgent
import json
import random
from seleniumwire import webdriver
import pandas as pd

proxy = {
        # 'http':'http://5.42.82.96:3128',
        # 'http':'http://ingp3030607:2iYbbAyXG4@81.22.44.132:7951',
        'https':'http://ingp3030607:2iYbbAyXG4@81.22.44.132:7951',
        } 

selenium_proxy = [
    # '80.82.55.71:80'
    '81.22.44.132:7951'
    # '91.200.163.190:8088'
]

def get_headers():
    ua = UserAgent()
    headers = {
    'User-Agent': ua.random
    }    
    return headers

def get_browser() -> webdriver.Chrome:
    """ Выдача браузера для обхода динамических страниц """
    print('\nOpen browser')
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--headless')
    options.add_argument(f'--proxy-server={random.choice(selenium_proxy)}')
    browser = webdriver.Chrome(options)
    return browser

def get_show_all_files(url):
    """ Создание файлов для городов с меткой 'показать все' """
    
    browser = get_browser()
    browser.get(url)
    raw_title = browser.find_element(By.CSS_SELECTOR, '.page_title > h1')
    title = raw_title.text.split()[0].replace('"','')
    file_path = f'pages/temp/cities_{title}.html'
    html = browser.page_source
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    browser.quit()
        
    urls = get_show_all_link(file_path)
    return urls
    
def get_show_all_link(path):
    """ Получение ссылок на города из раздела 'посмотреть все' """
    soup = BeautifulSoup(Path(path).read_text(encoding='utf-8'),'lxml')
    cities = []
    city_ul = soup.find('ul', 'cities-list')
    city_lis = city_ul.find_all('a')
    for city_li in city_lis:
        city = {
            'city':city_li.text,
            'href':city_li.get('href')
            }
        cities.append(city)
    return cities
        

def get_cities():
    
    """ Получение всех городов 
        Начало цикла
    """
    
    url = 'https://ru.restaurantguru.com/cities-Georgia-c'
    html_file = 'pages/cities_page.html'    
    cities_links = []
    
    if not os.path.exists(html_file):
        browser = get_browser()
        
        browser.get(url)
        time.sleep(2)
        html = browser.page_source
        with open('pages/cities_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        browser.quit()
        
    soup = BeautifulSoup(Path(html_file).read_text(encoding='utf-8'), 'lxml')
    city_blocks = soup.find_all('div', 'cities_block')
    
    for block in city_blocks[:5]:
        if block.find('a', 'show_all'):
            a = block.find('a', 'show_all')
            link = a.get('href')
            additional_cities = get_show_all_files(link)
            try:
                cities_links = cities_links + additional_cities
            except:
                print('Cities_links:', cities_links)
                print('additional_cities:', additional_cities)
                exit()
        else:
            city_ul = block.find('ul') # список всех городов
            city_link = city_ul.find_all('a') # получение ссылки на город
            for link in city_link:
                city = {
                    'city':link.text.split()[0],
                    'href':link.get('href')
                }
                cities_links.append(city)
    return cities_links

    
    
def get_restaurants(city_links):
    """ Получение всех ресторанов в городе 
        Середина цикла
    """
    for url in city_links:
        browser = get_browser()
        browser.get(url)
        browser.execute_script('window.scrollTo(0,2000);')
        time.sleep(1)
        browser.execute_script('window.scrollTo(0,4000);')
        time.sleep(1)
        title = browser.find_element(By.CLASS_NAME, "filter_block").text
        time.sleep(4)
        last_height = browser.execute_script('return document.body.scrollHeight')
        while True:
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(0.7)
            new_height = browser.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height
            print(last_height)
        html = browser.page_source
        with open(f'ajax_pages/{title}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
    
def get_city_restaurants_links():
    """ Получение ссылок на рестораны"""
    count = 0
    start = time.time()
    htmls = glob.glob('ajax_pages/*.html')
    print(htmls)
    links = {}
    for html in htmls:
        city_name = html.split('\\')[1].replace('.html','').strip()
        soup = BeautifulSoup(Path(html).read_text(encoding='utf-8'), 'lxml')
        titles = soup.find_all('a', 'notranslate title_url')
        
        links['city']= {city_name:[]}
        for title in titles[:50]:
            new_title = title.text.split()    
            link = title.get('href')
            restaurant = {
                'restaurant':' '.join(new_title),
                'link':link,                
            }
            links['city'][city_name].append(restaurant)
            
    print(links)
    with open('restaurants.json', 'w', encoding='utf-8') as file:
        json.dump(links, file, indent=4)
    

    
def get_restaurant_info():
    """ Получение информации по ресторану """
    count = 0
    with open('restaurant.json','r',encoding='utf-8') as file:
        data = json.load(file)
    # print(data['city'])
    restaurants_names = []
    restaurants_urls = []
    restaurants_price = []
    for city in data['city']:
        for restaurant in data['city'][city][:3]:
            if count == 5:
                time.sleep(10)
                count = 0
            # print(restaurant.get('link'))
            link = restaurant.get('link')
            title = restaurant.get('restaurant')
            response = requests.get(link, headers=get_headers())
            if response.status_code == 200:
                
                soup = BeautifulSoup(response.text, 'lxml')
                rest_info = soup.find('div', 'with_avg_price')
                avg_price = soup.find('span', 'nowrap')
                div_address = soup.find('div', 'address')
                address = div_address.find_all('div')[1]

                restaurants_names.append(title)
                restaurants_urls.append(link)
                restaurants_price.append(avg_price.text.strip())
                
                print(title, avg_price.text, address.text)
                count += 1
                time.sleep(5)
                
            else:
                exit()
    restaurant_info = pd.DataFrame(
                    {
                        'name':restaurants_names,
                        'url':restaurants_urls,
                        'one-person-price':restaurants_price
                    }
                )
    restaurant_info.to_excel('./restaurants.xlsx', sheet_name='Batumi', index=False)
            

    
# def check_proxy():
#     browser = get_browser()
#     try:
#         browser.get('https://2ip.ru/')
#         time.sleep(30)
#     finally:
#         browser.quit()
    
# def check_proxy():
#     response = requests.get(url='https://whoer.net/ru', headers=get_headers(), proxies=proxy)
#     with open('proxy.html', 'w', encoding='utf-8') as file:
#         file.write(response.text)
    
        
        
# check_proxy()
        
# get_show_all_links()
# get_cities()
# get_restaurants()
# get_city_restaurants_links()
get_restaurant_info()

    