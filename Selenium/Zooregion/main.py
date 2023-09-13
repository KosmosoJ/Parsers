import fake_useragent
import requests
from bs4 import BeautifulSoup
import httplib2
import urllib
import http.client
import json, time, glob
import os 


http.client._MAXHEADERS = 1000

def get_headers():
    ua = fake_useragent.UserAgent()
    headers = {
        'User-Agent':ua.random
    }
    return headers
    
def get_page():
    response = requests.get(url='https://zooregion.ru/catalog/sobaki/korm-dlya-sobak/suxoj-korm-dlya-sobak/rk-chixuaxua-28-500g.html',
                            headers=get_headers())
    with open('page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    
def get_categories(url):
    response = requests.get(url=url, headers=get_headers())
    soup = BeautifulSoup(response.text, 'lxml')
    container = soup.find('div', 'blog-d-box')
    categories = container.find_all('div', 'col-md-3')
    for category in categories:
        links = []
        title = category.find('h4').text
        items = category.find_all('li')
        for item in items:
            item_link = item.find('a').get('href')
            links.append('https://zooregion.ru/'+item_link)
        with open(f'categories/{title}.json', 'w', encoding='utf-8') as file:
            json.dump({'title':title, 'links':links}, file, indent=4)
            
def check_pagination(max_pagination, soup):
    pagination_ul = soup.find('ul', 'pagination')
    paginations_li = pagination_ul.find_all('li', 'list-inline-item')
    
    for li in paginations_li:
        if li.text.isdigit():
            if max_pagination < int(li.text):
                max_pagination = int(li.text)
        else:
            continue
        
    return max_pagination
            
def get_category_info():
    categories = glob.glob('categories/*.json')
    for category in categories:
        with open(category, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            for url in data['links']:
                i = 1
                max_pagination = 1
                response = requests.get(url, headers=get_headers())
                if response.status_code == 200:
                    json_items = {'items':[]}
                    soup = BeautifulSoup(response.text, 'lxml')
                    
                    category_title = soup.find('div', 'blog-d-box')
                    category_title = category_title.text.strip().replace('\n','')
                    
                    print(f'Категория {category_title}')
                    max_pagination = check_pagination(max_pagination, soup)
                    if os.path.exists(f'./categories_items/{category_title}.json'):
                        print(f'Пропуск категории {category_title}, сон 3 секунды')
                        time.sleep(3)
                        break
                    soup = None
                    
                    while i <= max_pagination:
                    # for i in range(1,max_pagination+1):
                        if i != 1:
                            response = requests.get(f'{url}/?page={i}', headers=get_headers())
                        soup = BeautifulSoup(response.text, 'lxml')
                        time.sleep(1)
                        items_container = soup.find('div', 'tab-pane')
                        items = items_container.find_all('div', 'ms2_product')
                        max_pagination = check_pagination(max_pagination, soup)
                        for item in items:
                            title_container = item.find('form')
                            title_container_info = title_container.find('div', 'tab-heading')
                            try:
                                item_title = title_container_info.find('a').text.strip()
                            except:
                                continue
                            item_link = title_container_info.find('a').get('href')
                            item_link = 'https://zooregion.ru/' + item_link 
                            item_info = {'item':item_title, 'link':item_link}
                            json_items['items'].append(item_info)
                        print(f'Категория {category_title}\nИнформация со страницы {i}/{max_pagination} собрана. Сон 5 секунд\n')
                        i += 1
                        time.sleep(5)
                else:
                    print('В доступе отказано', response.status_code)        
                    exit()
                print(f'Категория {category_title}\nСбор товаров завершен\n')
                with open(f'categories_items/{category_title}.json', 'w', encoding='utf-8') as file:
                    json.dump(json_items, file, indent=4)
                print(f'Категория {category_title}\nЗапись категории завершена. Сон 10 секунд\n')
                time.sleep(10)
                

# get_page()

# get_categories('https://zooregion.ru/catalog/sobaki/')
get_category_info()

