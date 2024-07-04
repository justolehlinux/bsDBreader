# %%
import requests
import shopify
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import logging
import re
from multiprocessing import Pool
from functools import partial


logging.basicConfig(level=logging.ERROR)

shop_url = "https://429eef-90.myshopify.com/"
api_version = '2024-01'
# state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
# redirect_uri = "http://myapp.com/auth/shopify/callback"
# scopes = ['read_apps', 'write_files', 'read_files', 'write_products', 'read_products', 'read_content', 'write_content', 'write_product_feeds', 'read_product_feeds', 'write_product_listings', 'read_product_listings']


load_dotenv()
access_token = (os.getenv('access_token'))

session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)


# %%
class Product:
    def __init__(self, name, spu, imgs, url, detail=None):
        self.name = name
        self.detail = ""
        if detail:
            self.detail = detail
        self.spu = spu
        self.imgs = imgs
        self.url = url
        if '8 ml' in name:
            self.price = '9.00'
            self.compare_at_price = '12.00'
            self.grams = 12
            self.weight = 0.012
        else:
            self.price = '15.00'
            self.compare_at_price = '17.00'
            self.grams = 20
            self.weight = 0.020
        self.vendor = 'Komilfo'
        self.product_type = 'Gel Polish'

    def __str__(self):
        return f"Product: {self.name}, SPU: {self.spu}"


# %%
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


# %%
def extract_product_links(url):
    """
    Извлекает ссылки на продукты из HTML-кода страницы с результатами поиска.
    """
    html = get_search_results(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('h4')
        return [h3.find('a')['href'] for h3 in links if h3.find('a')]
    return None


# %%
def extract_data_from_url(url):
    """
    Extracts product data from the provided URL.
    """
    try:
        # Extract data from the URL
        html = get_search_results(url)
        if not html:
            raise ValueError("Failed to fetch HTML content from the URL.")

        soup = BeautifulSoup(html, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            del a_tag['href']        
        description_div = soup.find('div', id='tab-description')

        # Remove h3 and li elements with data attribute 'data-number-of-phrases="9"'
        if description_div:
            for element in description_div.find_all(['h3', 'li']):
                if 'data-number-of-phrases="9"' in str(element):
                    element.extract()

        # Convert the remaining div element to a string
        detail = str(description_div) if description_div else ""
        spu = soup.find('span', class_='sku').text
        name = soup.find('h1',class_='product_title entry-title').text
        imgs = [img.get('data-large_image') for img in soup.find_all('img',decoding="async")]
        # imgs =soup
        
        return Product(name, spu, imgs, url, detail=detail)
    except Exception as e:
        logging.error(f"Failed to extract data from URL: {str(e)}")
        return None

# %%
def create_product(product):
    """
    Creates a new product on Shopify with the provided data, 
    handling creation, updates, and errors.
    """
    try:
        Handle = product.url.split('/')[-2]
        shopify_product = shopify.Product.find(handle=Handle)
        new_title = product.name.replace("Komilfo ", "").replace("ML","ml").replace(" ml","ml").replace("Liquid Glam Gel","Gel Polish Liquid Glam Gel")
        new_handle = re.sub(r"\[.*?\]|\(.*?\), ", "", new_title).lower().replace(" ","-")

        if not shopify_product:
            
            shopify_product = shopify.Product.find(handle=new_handle)
            # Create a new product instance
            if not shopify_product:
                shopify_product = create_new_product(product, new_title, new_handle)
                logging.info(f"Product created successfully! (ID: {shopify_product.id})")
                print("Product created successfully!")
            else:
                shopify_product = shopify_product[0]
                logging.info(f"Product already exists with matching title: {shopify_product.title} (ID: {shopify_product.id})")
                print(shopify_product.title)
                print("Product already exists!")
        else:
            # Update existing product if titles differ
            shopify_product = shopify_product[0]
            # print(shopify_product.title)
            if shopify_product.title != product.name.replace("Komilfo ", ""):
                update_product(shopify_product, new_title, new_handle)
                logging.info(f"Product updated successfully! (ID: {shopify_product.id})")
                print(shopify_product.title)
                print("Product updated successfully!")
            else:
                logging.info(f"Product already exists with matching title: {shopify_product.title} (ID: {shopify_product.id})")
                print(shopify_product.title)
                print("Product already exists!")

        return shopify_product

    except Exception as e:
        logging.error(f"Failed to create product: {str(e)}")
        return None

def create_new_product(product, new_title, new_handle):
    """
    Creates a new Shopify product with details and default variant.
    """

    shopify_product = shopify.Product.create({
        'title': new_title,
        'handle': new_handle,
        'body_html': product.detail,
        'vendor': product.vendor,
        'product_type': product.product_type
    })

    default_variant = {
        'title': 'Default Title',
        'price': product.price,
        'sku': product.spu,
        'compare_at_price': product.compare_at_price,
        'inventory_policy': 'deny',
        'fulfillment_service': 'manual',
        'inventory_management': 'shopify',
        'option1': 'Default Title',
        'taxable': True,
        'grams': product.grams,
        'weight': product.weight,
        'weight_unit': 'kg',
        'requires_shipping': True
    }

    variant = shopify.Variant(default_variant)
    shopify_product.variants = [variant]

    half_len = len(product.imgs) // 2
    
    shopify_product.images = [{'src': img_url, 'position': index, 'alt': product.name} for index, img_url in enumerate(product.imgs[:half_len], start=1)]
    shopify_product.save()
    return shopify_product

def update_product(shopify_product, new_title, new_handle):
    """
    Updates an existing Shopify product with new title and handle if needed.
    """

    print(new_title)
    print(shopify_product.title)

    shopify_product.title = new_title
    shopify_product.handle = new_handle
    shopify_product.save()

# %%
def create_or_get_collection(col_handle, col_name):
    # Find the collection by handle
    collections = shopify.SmartCollection.find(handle=col_handle)

    # If the collection doesn't exist, create a new one
    if not collections:
        collection = shopify.SmartCollection.create({
    'title': col_name,
    'handle': col_handle,
    'rules': [
        {
            "column": "title",
            "relation": "contains",
            "condition": col_name.split(' ')[0]
        },
        {
            "column": "vendor",
            "relation": "equals",
            "condition": 'Komilfo'
        }
        ]
        })

        print(f"Collection {col_name} created")
        print()
    else:
        # Get the first collection from the PaginatedCollection
        collection = collections[0]
        collection.title = col_name.capitalize()
        collection.save()
        print(f"Collection {col_name} mody")
    return collection


def add_product_to_collection(collection, product):
    new_collect = shopify.Collect.create({
        "collection_id": collection.id,
        "product_id": product.id
    })
    print(f"Product added to collection")

def process_product(col_name, prod_link):
    # Extract data from the product link
    data = extract_data_from_url(prod_link)

    # Add product to the collection
    create_product(data)
    print(f"{col_name}: Processed product - {prod_link}")


# %%
def allProdCol(colURL):
    # Get the collection name
    col_handle = colURL.split('/')[-2].replace('-en', '')
    col_name = col_handle.replace('-', ' ').upper()
    

    # Create or get the collection
    create_or_get_collection(col_handle, col_name)

    # Loop through pages
    for i in range(1, 31):    
        url = f"{colURL}/page/{i}"

        # Extract product links from the page
        prod_links = extract_product_links(url)

        if prod_links:
            print(f'{col_name}: Page {i}: {len(prod_links)} products')
            print()
            
            # Add each product to the collection
            for index, prod_link in enumerate(prod_links, start=1):
                data = extract_data_from_url(prod_link)
                create_product(data)
                print(f"{index}/{len(prod_links)}\n")
        else:
            print(f'{col_name}: Page {i}: No products')
            break

def process_page(colURL, page_number):
    url = f"{colURL}/page/{page_number}"

    # Extract product links from the page
    product_links = extract_product_links(url)

    if product_links:
        print(f'{col_name}: Page {page_number}: {len(product_links)} products')
        print()

        # Use a pool of workers to process product links concurrently
        with Pool() as pool:
            # Map the create_product function to each product link
            pool.starmap(create_product, zip(product_links))

def allProdCol_multiprocess(colURL):
    # Get the collection name
    col_handle = colURL.split('/')[-2].replace('-en', '')
    col_name = col_handle.replace('-', ' ').upper()

    # Create or get the collection
    create_or_get_collection(col_handle, col_name)
    
    process_page_partial = partial(process_page, colURL=colURL)

    # Use process_page_partial with Pool
    with Pool() as pool:
        pool.map(process_page_partial, range(1, 31))  # Adjust range for desired number of pages


listCol = [

 'https://komilfo.ua/en/product-category/komilfo-gel-polish/neon-collection/'
           ]

for colURL in listCol:

    allProdCol(colURL)


