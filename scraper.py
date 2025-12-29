from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://in.puma.com/in/en/womens/womens-shoes"


def clean_price(price):
    """Convert price string like ₹3,499 to integer 3499"""
    if price:
        return int(price.replace("₹", "").replace(",", "").strip())
    return None


def extract_product_name(a_tag):
    """
    Handle cases like:
    '3 Colors, Galaxis Pro Women's Performance Boost Running Shoes'
    """
    aria = a_tag.get("aria-label", "")
    parts = [p.strip() for p in aria.split(",")]

    if parts and "Colors" in parts[0] and len(parts) > 1:
        return parts[1]
    return parts[0] if parts else None


def main():
    all_products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page_number = 1

        while True:
            print(f"Scraping page {page_number}")

            # Load page (do NOT use networkidle)
            page.goto(f"{BASE_URL}?page={page_number}", timeout=60000)
            page.wait_for_load_state("load")
            time.sleep(2)  # allow JS to finish rendering prices

            soup = BeautifulSoup(page.content(), "html.parser")
            products = soup.select("[data-test-id='product-list-item']")

            if not products:
                print("No more products found. Stopping pagination.")
                break

            for product in products:
                try:
                    a_tag = product.find("a", href=True)
                    if not a_tag:
                        continue

                    url = "https://in.puma.com" + a_tag["href"]
                    name = extract_product_name(a_tag)

                    price_texts = [
                        span.get_text(strip=True)
                        for span in product.find_all("span")
                        if "₹" in span.get_text()
                    ]

                    sale_price = clean_price(price_texts[0]) if len(price_texts) >= 1 else None
                    mrp = clean_price(price_texts[1]) if len(price_texts) >= 2 else None

                    all_products.append({
                        "URL": url,
                        "Product Name": name,
                        "Brand": "Puma",
                        "Sale Price": sale_price,
                        "MRP": mrp
                    })

                except Exception:
                    continue

            page_number += 1
            time.sleep(1)

        browser.close()

    df = pd.DataFrame(all_products)
    df.drop_duplicates(subset="URL", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv("dataset.csv", index=False)

    print("dataset.csv saved successfully")


if __name__ == "__main__":
    main()
