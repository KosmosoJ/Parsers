import requests
from bs4 import BeautifulSoup
import time
cookies = {
    'identId': '6600000100000',
    'identName': '%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3',
    'PHPSESSID': 'rd6o1nqtk9gkpknl3lo7li4pg6',
    'show_dayx_pop': '1',
    '98defd6ee70dfb1dea416cecdf391f58': '576ca455199a9b40f94bbf5f7ffb0c31',
    '_ym_uid': '1690535485697684406',
    '_ym_d': '1690535485',
    '_ga': 'GA1.2.190244011.1690535485',
    '_gid': 'GA1.2.271146372.1690535485',
    '_ym_isad': '1',
    'kId': '6600000100000',
    'kName': '%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3',
    'reg_sex': '1',
    '_gat': '1',
    'carrotquest_session': 'vqs9w1trl7w7w91h59iakpawck73nqzs',
    '_ga_0W7BJF1N1P': 'GS1.2.1690535485.1.1.1690535823.60.0.0',
}

headers = {
    'authority': 'fireboxstore.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'identId=6600000100000; identName=%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3; PHPSESSID=rd6o1nqtk9gkpknl3lo7li4pg6; show_dayx_pop=1; 98defd6ee70dfb1dea416cecdf391f58=576ca455199a9b40f94bbf5f7ffb0c31; _ym_uid=1690535485697684406; _ym_d=1690535485; _ga=GA1.2.190244011.1690535485; _gid=GA1.2.271146372.1690535485; _ym_isad=1; kId=6600000100000; kName=%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3; reg_sex=1; _gat=1; carrotquest_session=vqs9w1trl7w7w91h59iakpawck73nqzs; _ga_0W7BJF1N1P=GS1.2.1690535485.1.1.1690535823.60.0.0',
    'referer': 'https://fireboxstore.ru/catalogue/obuv/muzhskaya/butsy-puma-future-ultimate-fg-blue-orange_23513.html',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183',
}


def parse_main_page():
    response = requests.get('https://fireboxstore.ru/', cookies=cookies, headers=headers)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, 'lxml')
    gender_container = soup.find('div', 'bl-sub_menu--wrapper')
    male_div = gender_container.find_all('div')[0]
    female_div = gender_container.find_all('div')[1]
    
    male_links = male_div.find_all('a')[0]
    female_links = female_div.find_all('a')[0]
    start = time.time()
    parse_products('male', male_links)
    print(round(time.time() - start))
    # parse_products('female', female_links)
    
    
def parse_products(gender ,link):
    
    i = 1
    pagination = 1
    product_link = link.get('href')
    url = f'https://fireboxstore.ru{product_link}?page={i}'
    response = requests.get(url , cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    pagination_div = soup.find('div', 'pag-wrapper')    
    pagination_num = int(pagination_div.find_all('a')[-2].text)
    collected_product = 0
    print(i)
    # while i <= pagination:
    while i <= 2:
        response = requests.get(url , cookies=cookies, headers=headers)
        response.encoding='utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        products_div = soup.find('div','icat')
        products_link = products_div.find_all('a')
        for product_link in products_link:
            parse_product(product_link.get('href'))
            collected_product += 1
        
        i += 1
    print(collected_product)
    
def parse_product(link):
    response = requests.get(f'https://fireboxstore.ru{link}' , cookies=cookies, headers=headers)
    response.encoding='utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    item_div = soup.find('div', 'bl-control--card')
    item_name = item_div.find('h1', 'maker')
    item_article = item_div.find('span','article')
    item_prices = item_div.find_all('div','bl-complect_price__cart--item')
    opt_price = item_prices[0]
    drop_price = item_prices[1]
    
    size_ul = soup.find('ul', 'ex-size')
    size_list = size_ul.find_all('li')
    sizes = ', '.join(size.text.strip().replace('\n','') for size in size_list)
    # print(sizes)
            

parse_main_page()
        
        
        
        
        