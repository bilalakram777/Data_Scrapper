import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch webpage content
def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

# Function to parse HTML and extract data
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    books = []

    # Extracting book titles and prices
    for article in soup.find_all('article', class_='product_pod'):
        title = article.h3.a['title']  # Get the title attribute
        price = article.find('p', class_='price_color').get_text(strip=True)  # Get the price text
        books.append({"title": title, "price": price})

    return books

# Function to save data to a CSV file
def save_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "price"])
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

# Main function
def main():
    url = "http://books.toscrape.com/"
    html_content = fetch_webpage(url)

    if html_content:
        books = parse_html(html_content)
        if books:
            save_to_csv(books, "scraped_books.csv")
        else:
            print("No data found on the webpage.")
    else:
        print("Failed to fetch webpage content.")

if __name__ == "__main__":
    main()
