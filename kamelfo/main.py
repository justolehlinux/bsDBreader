import requests
from bs4 import BeautifulSoup
import requests

def search_product(keyword):
    url = "https://komilfo.ua/en/"
    params = {
        's': keyword,
        'lang': 'en',
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Request successful!")
            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = soup.find_all(title=True, rel='bookmark',href=lambda href: href and keyword in href)
            for result in product_links:
                product_name = result.text.strip()
                product_link = result['href']
                print(f'Product Name: {product_name}')
                print(f'Product Link: {product_link}\n')        
        else:
            print("Error: Failed to make request")
    except requests.exceptions.RequestException as e:
        print("Error:", e)


search_product('d033')
