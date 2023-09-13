import requests
from bs4 import BeautifulSoup

url = 'https://scrapingclub.com/exercise/list_basic/?page=1'

def get_links(url):
    base_url = 'https://scrapingclub.com/exercise/list_basic/'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.find('ul', 'pagination')
    urls = []
    links = pages.find_all('a', 'page-link')
    
    for link in links:
        page_num = int(link.text) if link.text.isdigit() else None 
        if page_num != None:
            hrefval = link.get('href')
            
            urls.append(f'{base_url}{hrefval}')
    return urls
    

def get_items(urls):
    item_list = []
    print(urls)
    for item_url in urls:
        response = requests.get(item_url)
        soup = BeautifulSoup(response.text, 'lxml')    
        items = soup.find_all('div', 'card-body')
        for n,i in enumerate(items):
            if i is not None:
                try:
                    itemName = i.find('h4', 'card-title').text.strip()
                    itemPrice = i.find('h5').text 
                    item_list.append(f'Товар: {itemName}, за {itemPrice}')      
                except:
                    continue
    return item_list
        
item_urls = get_links(url)
items = get_items(item_urls)
for item in items:
    print(item)