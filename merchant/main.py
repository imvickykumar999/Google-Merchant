from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Merchant Center credentials and configurations
MERCHANT_ID = '5516640400'
KEY_FILE = 'credentials.json'  # Path to your service account key file
BASE_URL = "https://blogforge.pythonanywhere.com/"  # Base URL of your website

# Sample product data
PRODUCTS = [
    {
        "id": "1",
        "name": "Product 1",
        "description": "Description of Product 1",
        "price": 499.99,
        "image": "images/product1.jpg",
        "availability": True
    },
    {
        "id": "2",
        "name": "Product 2",
        "description": "Description of Product 2",
        "price": 299.99,
        "image": "images/product2.jpg",
        "availability": False
    }
]

def get_google_service():
    """Authenticate with the Google API."""
    SCOPES = ['https://www.googleapis.com/auth/content']
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE, scopes=SCOPES)
    return build('content', 'v2.1', credentials=credentials)

def format_product_data(product):
    """Prepare the product data in the format expected by the API."""
    return {
        'offerId': product['id'],
        'title': product['name'],
        'description': product['description'],
        'link': f"{BASE_URL}product/{product['id']}/",
        'imageLink': f"{BASE_URL}{product['image']}",
        'contentLanguage': 'en',
        'targetCountry': 'IN',
        'channel': 'online',
        'availability': 'in stock' if product['availability'] else 'out of stock',
        'condition': 'new',
        'price': {
            'value': str(format(product['price'], '.2f')),
            'currency': 'INR'
        }
    }

def upload_products():
    """Upload products to Google Merchant Center."""
    service = get_google_service()
    for product in PRODUCTS:
        product_data = format_product_data(product)
        try:
            response = service.products().insert(
                merchantId=MERCHANT_ID, body=product_data).execute()
            print(f"Successfully uploaded product ID {product['id']}: {response}")
        except Exception as e:
            print(f"Failed to upload product ID {product['id']}: {str(e)}")

def delete_products():
    """Delete all products from Google Merchant Center."""
    service = get_google_service()
    try:
        response = service.products().delete(merchantId=MERCHANT_ID).execute()
        print(f"Successfully deleted all products: {response}")
    except Exception as e:
        print(f"Failed to delete all products: {str(e)}")

if __name__ == "__main__":
    upload_products()
    # delete_products()
