import pandas as pd 
from typing import List, Dict
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import os 


data = {
    'modelname':[],
    'brand':[],
    'category':[],
    'pdfname':[],
    'pdflink':[],
}

def get_excel_data() -> Dict:
    excel_data = pd.read_excel('Категории для парсинга.xlsx')    
    category = excel_data['category'].to_list()
    links = excel_data['links'].to_list()
    items_dict = {}
    for i in range(len(links)):
        items_dict[category[i]] = links[i]
    return items_dict

proxies = {
    'http':'http://de3030703:EUFtBFILLU@212.107.27.55:7955',
    'https':'http://de3030703:EUFtBFILLU@212.107.27.55:7955',
    # 'http':'http://ingp3030607:2iYbbAyXG4@81.22.44.132:7951',
    # 'https':'http://ingp3030607:2iYbbAyXG4@81.22.44.132:7951',
}

def get_headers():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
    }
    return headers

def get_category(url):
    response = requests.get(url=url, headers=get_headers(), proxies=proxies)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup
    
def get_guides(url, category, brand):
    response = requests.get(url, headers=get_headers(), proxies=proxies)
    soup = BeautifulSoup(response.text, 'lxml')
    guides = soup.find_all('div', 'instruction_list-section_wrapper')
    for guide in guides:
        link_to_guide = guide.find('a').get('href')
        item_title = guide.find_all('span')
        file, guide_link = download_guide(link_to_guide)
        
        for title in item_title:
            data['modelname'].append(title.text.strip())
            data['brand'].append(brand)
            data['category'].append(category)
            data['pdfname'].append(file)
            data['pdflink'].append(guide_link)
        
        
def save_to_excel(data_result):
    df = pd.DataFrame(
        {
            'modelname':data_result['modelname'],
            'brand': data_result['brand'],
            'category':data_result['category'],
            'pdfname':data_result['pdfname'],
            'pdflink':data_result['pdflink'],
        }
    )
    print(data_result)
    df.to_excel('result.xlsx', index=False)
    
def main():
    items_links = get_excel_data()
    for item_category, item_link in items_links.items():
        category:BeautifulSoup = get_category(item_link) 
        try:
            guides = category.find_all('a', 'instruction_brands-section_title')
        except Exception:
            guides = None
            
        if guides is not None:
            for guide in guides:
                guide_link = guide.get('href')
                try:
                    brand_img:BeautifulSoup = guide.find('div', 'instruction_brands-section_image')
                    brand = brand_img.find('img').get('alt')
                except:
                    brand = guide_link.replace('/', ' ').split()[-1]
                print(brand)
                guide_item = get_guides(guide_link, item_category, brand)
        else:
            print(f'Пропуск {item_category}:{item_link}\n') 
    save_to_excel(data)
    print('Вся информация собрана.')
    
def download_guide(link):
    item_code = link.replace('/',' ').split()[-1]
    filename = f'{item_code}.pdf'
    url = f'https://www.moyo.ua/pub/files/instructions/{item_code}.pdf'
    pdf_folder = f'pdfs/{item_code}.pdf'
    if not os.path.exists(pdf_folder):
        print('Началось скачивание файла. Ожидайте... Может занять от 5 сек до 2х минут')
        
        response = requests.get(url=url, headers=get_headers(), proxies=proxies)
        with open(f'pdfs/{filename}','wb') as file:
            file.write(response.content)
    else:
        print(f'Файл {filename} уже существует, пропуск скачивания')
            
    return filename, url
    
    
    
# download_guide()
main()
# print(get_excel_data())