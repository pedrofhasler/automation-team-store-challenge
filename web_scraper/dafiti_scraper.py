import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.dafiti.com.br/'

productlinks = []

for i in range(1,4):
    r = requests.get(f'https://www.dafiti.com.br/special-price-masculino/roupas-masculinas/?cat-pwa=0&campwa=0&page={i}')
    soup = BeautifulSoup(r.content, 'lxml')

    productlist = soup.find_all('div', class_='product-box')

    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(link['href'])

#Cleaning the data
productlinks=set(productlinks)
productlinks.remove('')
productlinks.remove('Javascript:;')

products_meta = []
for link in productlinks:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    name = soup.find('h1', class_='product-name').text.strip()
    brand = soup.find('div', class_='product-brand hide-mobile').text.strip()
    price = soup.find('span', class_='catalog-detail-price-value').text.strip()
    image = soup.find('div', class_='gallery-preview')
    description = soup.find('p', class_='product-information-description').text.strip()
    product = {
        'name': name,
        'brand': brand,
        'price': price,
        'img': image['data-img-zoom'],
        'description': description
    }
    products_meta.append(product)

df = pd.DataFrame(products_meta)
print(df.head(5))
df.to_csv('dafiti.csv', index=False)