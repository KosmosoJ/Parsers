import requests
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
tags = soup.find_all('div', class_='tags')

for i in range(len(quotes)):
    print(quotes[i].text)
    print('----', authors[i].text)
    
    
    item_tags = tags[i].find_all('a', class_='tag')
    tags_str = ', '.join(tag.text for tag in item_tags)
    print(tags_str)
    
    
    