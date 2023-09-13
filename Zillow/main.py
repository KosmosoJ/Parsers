import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
cookies = {
    'zguid': '24|%249ff9f8f7-418e-429f-a856-02748e355cec',
    'zgsession': '1|2500343b-b3f1-467a-b37e-a024173cedcb',
    '_ga': 'GA1.2.2102336911.1690227109',
    '_gid': 'GA1.2.1684757318.1690227109',
    'zjs_anonymous_id': '%229ff9f8f7-418e-429f-a856-02748e355cec%22',
    'zjs_user_id': 'null',
    'zg_anonymous_id': '%226ec68e4e-c330-4833-a2d9-ef4a341afe1a%22',
    'JSESSIONID': 'D857D5024EFDB77AB42580918423DA6E',
    'pxcts': 'bc57b4b5-2a58-11ee-90d3-53556e707841',
    '_pxvid': 'bc57a14b-2a58-11ee-90d3-cd7e3d758fc1',
    '_gcl_au': '1.1.599436329.1690227112',
    'DoubleClickSession': 'true',
    '__pdst': '7efb62d158424333b6fbc4705912eeda',
    '_pin_unauth': 'dWlkPVl6YzVaV05qTWpJdE5EWTFOQzAwTVRCaUxUazVNbUV0WTJZeE9HVXhaR05sWWpVNA',
    '_clck': '58x9eh|2|fdk|0|1300',
    '_px3': 'bb5c08ac182c11357c1494ff04687f9819e023a69b3c4e2f6b098c178903cee7:BsyoZBjjYs5UdTq7IdY6ODzoyihRkmMoQK65jLKaCeRvdA31hbSSTsEjbrXOZ0wbuxfY2Nx/3o1+53BTw1Dfkg==:1000:A1wctwvZF3SiUX4TuOgFenmjyWc4yIoXPQH5u+cgyBDmC4F/G70qBOAmY50EoCGFrhy1AVl9jxgo/b30acU92FcG9IbQeuqxPg8NkLkPXCxRMNALgI0jRUFDmsCIYB21jDXfOLcwiNE5wJEve/ZiyCjmMam+/7vuYFbQMHJuiGPgtpPG0J8WQr1QI4iJCgWeTNyXV7WCEJQxUOxpP4oUKA==',
    'AWSALB': 'Ksjxytq11a4gdE25Q84W0lCvk/t2ccLAAXHYY8qM1kNzYSQFMp44q9UgeNOpaunzYs4/iUDmlyE1CB/7gpMpA1DsQ8aZpN2IJW2H+SNCkjaKg/5gftjfW66I8F6d',
    'AWSALBCORS': 'Ksjxytq11a4gdE25Q84W0lCvk/t2ccLAAXHYY8qM1kNzYSQFMp44q9UgeNOpaunzYs4/iUDmlyE1CB/7gpMpA1DsQ8aZpN2IJW2H+SNCkjaKg/5gftjfW66I8F6d',
    '_uetsid': 'bdbc11a02a5811eeb02fb7ed2d71868e',
    '_uetvid': 'bdbc61e02a5811ee8279558502127fe0',
    '_clsk': 'y5lmqz|1690227936398|8|0|x.clarity.ms/collect',
    '_gat': '1',
}

headers = {
    'authority': 'www.zillow.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'zguid=24|%249ff9f8f7-418e-429f-a856-02748e355cec; zgsession=1|2500343b-b3f1-467a-b37e-a024173cedcb; _ga=GA1.2.2102336911.1690227109; _gid=GA1.2.1684757318.1690227109; zjs_anonymous_id=%229ff9f8f7-418e-429f-a856-02748e355cec%22; zjs_user_id=null; zg_anonymous_id=%226ec68e4e-c330-4833-a2d9-ef4a341afe1a%22; JSESSIONID=D857D5024EFDB77AB42580918423DA6E; pxcts=bc57b4b5-2a58-11ee-90d3-53556e707841; _pxvid=bc57a14b-2a58-11ee-90d3-cd7e3d758fc1; _gcl_au=1.1.599436329.1690227112; DoubleClickSession=true; __pdst=7efb62d158424333b6fbc4705912eeda; _pin_unauth=dWlkPVl6YzVaV05qTWpJdE5EWTFOQzAwTVRCaUxUazVNbUV0WTJZeE9HVXhaR05sWWpVNA; _clck=58x9eh|2|fdk|0|1300; _px3=bb5c08ac182c11357c1494ff04687f9819e023a69b3c4e2f6b098c178903cee7:BsyoZBjjYs5UdTq7IdY6ODzoyihRkmMoQK65jLKaCeRvdA31hbSSTsEjbrXOZ0wbuxfY2Nx/3o1+53BTw1Dfkg==:1000:A1wctwvZF3SiUX4TuOgFenmjyWc4yIoXPQH5u+cgyBDmC4F/G70qBOAmY50EoCGFrhy1AVl9jxgo/b30acU92FcG9IbQeuqxPg8NkLkPXCxRMNALgI0jRUFDmsCIYB21jDXfOLcwiNE5wJEve/ZiyCjmMam+/7vuYFbQMHJuiGPgtpPG0J8WQr1QI4iJCgWeTNyXV7WCEJQxUOxpP4oUKA==; AWSALB=Ksjxytq11a4gdE25Q84W0lCvk/t2ccLAAXHYY8qM1kNzYSQFMp44q9UgeNOpaunzYs4/iUDmlyE1CB/7gpMpA1DsQ8aZpN2IJW2H+SNCkjaKg/5gftjfW66I8F6d; AWSALBCORS=Ksjxytq11a4gdE25Q84W0lCvk/t2ccLAAXHYY8qM1kNzYSQFMp44q9UgeNOpaunzYs4/iUDmlyE1CB/7gpMpA1DsQ8aZpN2IJW2H+SNCkjaKg/5gftjfW66I8F6d; _uetsid=bdbc11a02a5811eeb02fb7ed2d71868e; _uetvid=bdbc61e02a5811ee8279558502127fe0; _clsk=y5lmqz|1690227936398|8|0|x.clarity.ms/collect; _gat=1',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183',
}


data = {
    'url':[],
    'person_name':[],
    'team_name':[],
    'premier':[],
    'review_grade':[],
    'total_reviews':[],
    'total_sales':[],
    'address':[],
    'phone':[],
    'total_members':[]  
}

def parse_page(url):
    response = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    members_list = soup.find('ul', 'Flex-c11n-8-91-4__sc-n94bjd-0 MrIkl')
    
    try:
        members = members_list.find_all('li') # Люди
        if len(members) < 4:
            print('Людей меньше 4')
            return
    except:
        print('Это не командный профиль.')
        return
    
    
    sold = soup.find('section', id='pastSales') # Последние продажи
    sum = 0
    sold_items = sold.find('table', attrs={'aria-label':'Past sales table'}) # Последние продажи
    # print(sold_items)
    
    items = sold_items.find_all('td', 'cmzsCx')
    for i in range(1, len(items)-4,4 ):
        sum += int(items[i].text.strip().replace('$','').replace(',',''))
    if sum <= 400000:
        print('Сумма менее 400000$')
        return
    
    sales = int(soup.find('p', 'eZdVqg').text.strip().split()[0])
    if sales <= 20:
        print('Продаж меньше 20')
        return 
    
    
    person_name = soup.find('h1', 'jnoIGe').text.strip() # 
    team_name = ' '.join(soup.find('div', 'huQSxs').text.strip().split()[2:]) # 
    
    company_title = soup.find('div', 'ctcd-title')
    premier_block = company_title.find_all('div', 'dHzWJt')
    
    try:
        premier_check = premier_block[1].text.strip()
        premier = True # 
    except:
        premier = False #
    
    reviews_block = soup.find('span', 'egEemq')
    reviews_link = reviews_block.find('a').text.strip().split()
    review_grade = reviews_link[0] #
    total_reviews = reviews_link[2] #
    
    company_info_block = soup.find('div','eyGHKF')
    company_info_list = company_info_block.find_all('span','dOtWDO')
    address = company_info_list[0].text.strip() # 
    phone = company_info_list[1].text.strip() # 
    total_members = len(members) # 
    
    data['url'].append(url)
    data['person_name'].append(person_name)
    data['team_name'].append(team_name)
    data['premier'].append(premier)
    data['review_grade'].append(review_grade)
    data['total_reviews'].append(total_reviews)
    data['total_sales'].append(sales)
    data['address'].append(address)
    data['phone'].append(phone)
    data['total_members'].append(total_members)
    
    
def save_to_csv():
    df = pd.DataFrame(
        {
            'url':data['url'],
            'person_name':data['person_name'],
            'team_name':data['team_name'],
            'premier':data['premier'],
            'review_grade':data['review_grade'],
            'total_reviews':data['total_reviews'],
            'total_sales':data['total_sales'],
            'address':data['address'],
            'phone':data['phone'],
            'total_members':data['total_members'],
        }
    )
    df.to_csv(f'result{round(time.time())}.csv', index=False)

def main():
    with open('urls.txt', 'r', encoding='utf-8') as file:
        urls_data = file.read()
        urls = urls_data.split('\n')
    for url in urls:
        parse_page(url)
    save_to_csv()
    
    
start = time.time()
main()
print(round(time.time() - start),'Секунд')