from flask import Flask, request, render_template, redirect, url_for
from db import SessionLocal, init_db
from models import Product, Offer, TrackedProduct
from sqlalchemy.exc import IntegrityError
import httpx
import logging
import csv
from extruct.jsonld import JsonLdExtractor
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Twilio SMS function
def send_sms(to_phone, message):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_phone = os.getenv('TWILIO_PHONE_NUMBER')
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_=from_phone,
        to=to_phone
    )

# Get URLs from CSV file
def get_urls():
    with open("urls.csv", "r") as f:
        reader = csv.reader(f)
        urls = [url[0] for url in reader]
        return urls

# Get HTML data from URL
def get_html(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = httpx.get(url, headers=headers)
    if resp.status_code == 200:
        jslde = JsonLdExtractor()
        data = jslde.extract(resp.text)
        logging.info(f"Extracted data: {data}")
        return data
    else:
        logging.info(f"url {url} responded with bad status code {resp.status_code}")

# Load product data into the database
def load_product(session, data):
    sku = data.get("sku")
    if not sku:
        logging.warning(f"SKU is missing in the data: {data}")
        return None
    
    new_product = Product(
        name=data.get("name"),
        url=data.get("url"),
        description=data.get("description"),
        sku=sku,
        brand=data.get("brand", {}).get("name"),
    )
    try:
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return new_product
    except IntegrityError as err:
        logging.warning(f"Failed to load product due to: {err}")
        session.rollback()
        return None

# Load offer data into the database
def load_offers(session, data):
    product = session.query(Product).filter(Product.sku == data["sku"]).first()
    if not product:
        logging.warning(f"Product with SKU {data['sku']} not found.")
        return

    offers = data.get("offers")
    if isinstance(offers, list):
        for offer in offers:
            if offer.get("sku") == product.sku:
                new_offer = Offer(
                    price=offer["price"],
                    availability=offer.get("availability"),
                    product_id=product.id,
                )
                try:
                    session.add(new_offer)
                    session.commit()
                except IntegrityError as err:
                    logging.warning(f"Failed to load offer due to: {err}")
                    session.rollback()
    elif isinstance(offers, dict):
        new_offer = Offer(
            price=offers.get("price"),
            availability=offers.get("availability"),
            product_id=product.id,
        )
        try:
            session.add(new_offer)
            session.commit()
        except IntegrityError as err:
            logging.warning(f"Failed to load offer due to: {err}")
            session.rollback()

# Home route (index page)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle product URL submissions
@app.route('/track-url', methods=['POST'])
def track_url():
    url_to_track = request.form.get('productUrl')
    if url_to_track:
        session = SessionLocal()
        new_tracked_product = TrackedProduct(url=url_to_track)
        try:
            session.add(new_tracked_product)
            session.commit()
            session.close()
            # Redirect back to the home page with a success message
            return redirect(url_for('index', message="Product URL successfully added for tracking!"))
        except IntegrityError as err:
            session.rollback()
            session.close()
            logging.warning(f"Failed to add URL for tracking due to: {err}")
            # Redirect back with an error message
            return redirect(url_for('index', error="Failed to add product URL for tracking."))
    else:
        # Redirect back with an error if URL is missing
        return redirect(url_for('index', error="URL is required."))

# Initialize database and run the app
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
