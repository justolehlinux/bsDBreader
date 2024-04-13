import csv
import requests
from bs4 import BeautifulSoup
from collections import Counter
import logging

logging.basicConfig(level=logging.ERROR)

def get_search_results(url):
    """
    Получает результаты поиска для заданного URL.
    """
    try:
        with requests.get(url) as response:
            if response.status_code == 200:
                return response.text
            else:
                logging.error("Ошибка при получении страницы с результатами поиска: %d", response.status_code)
                return None
    except requests.RequestException as e:
        logging.error("Ошибка при запросе страницы: %s", str(e))
        return None

def extract_product_links(url):
    """
    Извлекает ссылки на продукты из HTML-кода страницы с результатами поиска.
    """
    html = get_search_results(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', class_='product-item-link')
        return [link['href'] for link in links]
    return None
        
def extract_product_data(url):
    """
    Извлекает данные о продукте из HTML-кода страницы товара.
    """
    Handle = url.split('/')[-1].replace('.html','')
    colorname = Handle.split('-')[-2]
    print(url)
    print(Handle)
    html = get_search_results(url)
    if html:
        # extracted_setring = html.split('/')[-1].replace('.html', '')
        soup = BeautifulSoup(html, 'html.parser')
        spu = soup.find('span', class_='value', itemprop='sku').text
        detail = soup.find('div', class_='value').text
        # print(Handle)
        # colorName = str(Handle).split('-')[-1]
        name = soup.find('h1').text
        # imgs = count_duplicates([img.get('src') for img in soup.find_all('img', class_='img-responsive', alt=name)], spu, colorname)
        imgs = [img.get('src') for img in soup.find_all('img', class_='img-responsive', alt=name)]
        data = {
            'Handle': Handle,
            'spu': spu,
            'spu': spu,
            'name': name,
            'img_urls': imgs,
            'detail': detail,
        }
        # print(data)
        return data
    return None

def count_duplicates(img_urls, name, Handle):
    """
    Подсчитывает дубликаты URL-адресов изображений.
    """
    duplicates_count = Counter(img_urls)

    return [img_url for img_url, count in duplicates_count.items() 
            if count > 1 
            # and name in img_url 
            # or Handle in img_url
            # and "jpeg" not in img_url
            ]

def write_to_csv(products):
    """
    Записывает данные о продуктах в CSV-файл.
    """
    with open('products3.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags',
                      'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value',
                      'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker',
                      'Variant Inventory Qty', 'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                      'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode',
                      'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
                      'Google Shopping / Google Product Category', 'Google Shopping / Gender', 'Google Shopping / Age Group',
                      'Google Shopping / MPN', 'Google Shopping / AdWords Grouping', 'Google Shopping / AdWords Labels',
                      'Google Shopping / Condition', 'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0',
                      'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3',
                      'Google Shopping / Custom Label 4', 'Variant Image', 'Variant Weight Unit', 'Variant Tax Code',
                      'Cost per item', 'Price / International', 'Compare At Price / International', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        for product in products:
            writer.writerow(product)

def main():
    # SPU = "941977"
    # letsgo(SPU)

    # Пример использования функции
    file_path = "example.txt"  # Путь к вашему файлу

    lines = read_lines_from_file    (file_path)
    # Пройдемся по каждой строке файла и напечатаем ее
    for index, line in enumerate(lines, start=1):
        letsgo(line)
        print(f"{index}/{len(lines)}")
        print("Good\n")

def read_lines_from_file(filename):
    """
    Читает файл построчно и возвращает список строк.

    Args:
    filename (str): Имя файла для чтения.

    Returns:
    list: Список строк из файла.
    """
    lines = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append(line.strip())  # Удаляем символы перевода строки и пробелы
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print("Произошла ошибка при чтении файла:", str(e))
    return lines
    

def letsgo(SPU):
    print(SPU)

    url = 'https://reforma.top/instantsearch/result/?q=' + SPU

    product_links = extract_product_links(url)
    if product_links:
        products = []
        product_data = extract_product_data(product_links[0])
        # print(product_data)
        if product_data and product_data['img_urls']:            # Создание записи о продукте для CSV
            product_record = {
                # 'Handle': product_links[0].split('/')[-1].replace('.html', ''),
                'Handle': product_data['Handle'],
                'Title': product_data['name'],
                'Body (HTML)': product_data['detail'],
                'Vendor': 'Reforma',
                'Product Category': 'Salud y belleza > Cuidado personal > Cosméticos',
                'Type': 'Gel Polish',
                'Published': 'true',
                'Option1 Name': 'Title',
                'Option1 Value': 'Default Title',
                'Variant SKU': product_data['spu'],
                'Variant Grams': '15.0',
                'Variant Inventory Tracker': 'shopify',
                'Variant Inventory Qty': '0',
                'Variant Inventory Policy': 'deny',
                'Variant Fulfillment Service': 'manual',
                'Variant Price': '10.00',
                'Cost per item': '3.50',
                'Variant Compare At Price': '13.00',
                'Variant Requires Shipping': 'true',
                'Variant Taxable': 'true',
                'Image Src':  product_data['img_urls'][0],
                'Image Position': '1',
                'Gift Card': 'false',
                'Google Shopping / Gender': 'g',
                'Google Shopping / Custom Product': 'true',
                'Status': 'active'
            }
            products.append(product_record)
            for img_index, img_url in enumerate(product_data['img_urls'], start=2):
                img_record = {
                    'Handle': product_data['Handle'],
                    'Image Src': img_url,
                    'Image Position': str(img_index)
                }
                products.append(img_record)

            # Запись данных в CSV
            write_to_csv(products)
            print("Данные успешно записаны в файл 'products.csv'")
    else:
        write_to_csv_NotFound(SPU)
        print("Не найдены ссылки на товары.")
        # print(data["handle"])

        # # print(data["detail"])
        # # print(extract_product_data(product_links[0]))

def write_to_csv_NotFound(SPU):
    with open('notFined.cvs', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(SPU)

# Example usage:


if __name__ == "__main__":
    main()
