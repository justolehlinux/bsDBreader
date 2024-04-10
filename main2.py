import requests
from bs4 import BeautifulSoup
from collections import Counter

def get_search_results(url):
    """
    Получает результаты поиска для заданного SPU.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Ошибка при получении страницы с результатами поиска:", response.status_code)
        return None

def extract_product_links(html):
    url = get_search_results(html)
    """
    Извлекает ссылки на продукты из HTML-кода страницы с результатами поиска.
    """
    product_links = []
    soup = BeautifulSoup(url, 'html.parser')
    links = soup.find_all('a', class_='product-item-link')
    for link in links:
        product_links.append(link['href'])
        print(link)
    return extract_product_data(product_links[0])
        
def extract_product_data(html):
    """
    Извлекает данные о продукте из HTML-кода страницы товара.
    """
    url = get_search_results(html)
    soup = BeautifulSoup(url, 'html.parser')
    imgs = count_duplicates([img.get('src') for img in soup.find_all('img', class_='img-responsive')])
    data = {
        'spu': soup.find('span', class_='value', itemprop='sku').text,
        'name': soup.find('h1').text,
        'img_urls': imgs,

    }

    return data

def count_duplicates(img_urls):
    """
    Подсчитывает дубликаты URL-адресов изображений.
    """
    duplicates_count = Counter(img_urls)
    imgs = []
    for img_url, count in duplicates_count.items():
        if count > 1:
            imgs.append(f"{img_url}")
    return imgs

def main():
    # SPU = input("Введите SPU товара: ")
    SPU = "941423"
    url = 'https://reforma.top/instantsearch/result/?q=' + SPU
    print(url)

    print(extract_product_links(url))

if __name__ == "__main__":
    main()
