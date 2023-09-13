import requests
from bs4 import BeautifulSoup
import json
import time

cookies = {
    'CTK': '1h6dhr7duk7up800',
    'ctkgen': '1',
    '__cf_bm': 'PglSIFVf2tIu9x3M4LiWHTBBToZnQQKYFLtXkZJax48-1690524556-0-AfuOxEHtlI9zGdfmFLxaIeADwiPKiDsmVVlMtKBAtXv0IpjDT9BmsLudTJTmFU+AIRFr/q9loZ8ezuRPVYcmyM8=',
    '_cfuvid': 'gKHvSNTD0BLUbA4tr0oN9tcp2IHJ5wHjUAUJlRvbIZI-1690524556818-0-604800000',
    'cf_clearance': 'oy2hrWCdIlCu4T.LW_giDsZ4uvHrDwVnCdNxm1qkmak-1690524557-0-250.2.1690524557',
    'PTK': 'tk=1h6dhvl1bk7up800',
    'JSESSIONID': 'node0ekio76wnfja2bim95oy5h7kp47448.node0',
}

headers = {
    'authority': 'www.indeed.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'CTK=1h6dhr7duk7up800; ctkgen=1; __cf_bm=PglSIFVf2tIu9x3M4LiWHTBBToZnQQKYFLtXkZJax48-1690524556-0-AfuOxEHtlI9zGdfmFLxaIeADwiPKiDsmVVlMtKBAtXv0IpjDT9BmsLudTJTmFU+AIRFr/q9loZ8ezuRPVYcmyM8=; _cfuvid=gKHvSNTD0BLUbA4tr0oN9tcp2IHJ5wHjUAUJlRvbIZI-1690524556818-0-604800000; cf_clearance=oy2hrWCdIlCu4T.LW_giDsZ4uvHrDwVnCdNxm1qkmak-1690524557-0-250.2.1690524557; PTK=tk=1h6dhvl1bk7up800; JSESSIONID=node0ekio76wnfja2bim95oy5h7kp47448.node0',
    'referer': 'https://kwork.ru/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183',
}

data = []

def get_all_categories():
    response = requests.get('https://www.indeed.com/browsejobs', cookies=cookies, headers=headers)
    
    soup = BeautifulSoup(response.text, 'lxml')
    categories = soup.find('ul', id='categories')
    categories_title = categories.find_all('a', 'text_level_3')
    for link in categories_title:
        category_name = link.text.strip()
        full_link = f'https://www.indeed.com{link.get("href")}'
        subcategories = get_category_info(full_link)
        category_info = {
            'name':category_name,
            'url': full_link,
            'subcategories': subcategories,
        }
        data.append(category_info)
        
def get_category_info(link):
    response = requests.get(link, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    subcategory_info = []
    subcategories = soup.find('ul', id='categories')
    subcategories_title = subcategories.find_all('a', 'text_level_3')
    
    for subcategory in subcategories_title:
        full_link = f'https://www.indeed.com{subcategory.get("href")}'
        subcategory_title = subcategory.text.strip()
        
        subcategory_dict={
            'name':subcategory_title,
            'url':full_link,
        }
        subcategory_info.append(subcategory_dict)
    return subcategory_info

def save_to_json():
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def main():
    start = time.time()
    get_all_categories()
    save_to_json()
    print(round(time.time() - start))
    
if __name__ == '__main__':
    main()