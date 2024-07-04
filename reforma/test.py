import shopify
import os
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
import binascii
import os



# shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)

shop_url = "https://429eef-90.myshopify.com/"
api_version = '2024-01'
state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
redirect_uri = "http://myapp.com/auth/shopify/callback"
scopes = ['read_apps', 'write_files', 'read_files', 'write_products', 'read_products', 'read_content', 'write_content', 'write_product_feeds', 'read_product_feeds', 'write_product_listings', 'read_product_listings']


load_dotenv()
access_token = (os.getenv('access_token'))

session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)
# redirect to auth_url

# with shopify.Session.temp(shop_url, api_version, token):
#     # Find product by product_id
#     id = "8764450046282"
#     sku = "941144"
#     title = "Gel Polish - Adventure, 10ml"
#     products = shopify.Product.all(title=title)  # Replace "Your Product ID" with the actual product_id
#     for product in products:
#         if product:
#             # variants = product.attributes['variants']
#             print(product.attributes )
#             print()
#         else:
#             print("Product not found")
#     print(shopify)


# with shopify.Session.temp(shop_url, api_version, token):
#     # Find product by product_id
#     id = "8764450046282"
#     sku = "941144"
#     product = shopify.Product.find(id)  # Replace "Your Product ID" with the actual product_id
#     if product:
#         for variant_id in product.attributes['variants']:
#             # variant = shopify.Variant.find(variant_id.id)
#             print(variant_id.attributes)
#             if variant_id.attributes['sku'] == sku:  # Accessing the sku attribute of the variant
#                 print("Variant found with SKU:", sku)
#                 # print("Variant:", variant.attributes)
#                 # break  # Exit the loop once the variant with matching SKU is found
#             else:
#                 print("Variant not found with SKU:", sku)
        
#         # print("Product Attributes:", product.attributes)
#     else:
#         print("Product not found")

# with shopify.Session.temp(shop_url, api_version, token):
#     id = "47903988121930"
#     sku = "941144"
#     product_id = '8764450046282'
#     title = 'Default Title'
#     variant = shopify.Variant.all(title=title)
#     print (variant)
#     variant = shopify.Variant.all(title=title)
#     print (variant)
#     if variant:
        
#         test = variant[0]
#         print(test.attributes , test.sku, test.id)

# with shopify.Session.temp(shop_url, api_version, token):
# variant = shopify.Product.find(handle='gel-polish-adventure-10ml')
variant = shopify.Image.find()


Collection = shopify.CustomCollection.create()
Collection.title = "My Collection"
Collection.save()
