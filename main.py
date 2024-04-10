import requests
from bs4 import BeautifulSoup
from collections import Counter



# Отправляем запрос на страницу
SPU = "941423"
# SPU = input("SPU?")
url = 'https://reforma.top/instantsearch/result/?q=' + SPU
response = requests.get(url)
product_links = []

# Проверяем успешность запроса
if response.status_code == 200:
    # Парсим HTML-код страницы
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Находим элементы с классом "product-item-link" и добавляем их ссылки в список
    links = soup.find_all('a', class_='product-item-link')
    for link in links:
        product_links.append(link['href'])

    # Если список содержит хотя бы одну ссылку
    if product_links:
        # Используем первую ссылку
        first_link = product_links[0]
        
        # Отправляем запрос на первую ссылку
        print("Отправляем запрос на:", first_link)
        response = requests.get(first_link)
        
        # Проверяем успешность запроса
        if response.status_code == 200:
            # Здесь вы можете продолжить обработку страницы
            # Например, парсить HTML-код и извлекать нужную информацию
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Находим элемент <span> с классом "value" и атрибутом itemprop="sku"
            h1 = soup.find('h1')
            print("Name:", h1.text)

            sku_element = soup.find('span', class_='value', itemprop='sku')
            print("SKU:", sku_element.text)

            img_elements = soup.find_all('img', class_='img-responsive')
            
            # Создаем список для хранения URL-адресов изображений
            img_urls = []
            
            # Извлекаем URL-адрес каждого изображения и добавляем его в список
            for img in img_elements:
                img_src = img.get('src')
                img_urls.append(img_src)
            

            
            # print("Список URL-адресов изображений:")
            # for img_url in img_urls:
            #     print(img_url)

            duplicates_count = Counter(img_urls)
    
    # Выводим результат
            print("Подсчет дубликатов:")
            for img_url, count in duplicates_count.items():
                if count > 1:
                    # print(f"URL: {img_url}, Количество дубликатов: {count}")
                    print(f"{img_url}")

        else:
            print("Ошибка при получении страницы:", response.status_code)
    else:
        print("Список ссылок пуст")
else:
    print("Ошибка при получении страницы:", response.status_code)