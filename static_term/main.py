import requests
from bs4 import BeautifulSoup

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0"}

response = requests.get("https://quotes.toscrape.com", headers = headers)

print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')

quotes = soup.find_all('div',class_='quote')

for quote in quotes:
    text = quote.find('span',class_='text').text
    author = quote.find('small',class_='author').text
    tags = []
    for tag in quote.find_all('a', class_='tag'):
        tags.append(tag.text)

    print(text,'/n-' , author)
    print('Tags: ',' , '.join(tags),'/n')