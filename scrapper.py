import csv
import json
import requests
from bs4 import BeautifulSoup





url = "https://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to load page.')
        return []
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text,"html.parser")
    books = soup.find_all("article", class_="product_pod")

    book_list = []

    for book in books:
        title = book.h3.a['title']
        
        price_text = book.find('p', class_='price_color').text 

        currency = price_text[0]
        price = float(price_text[1:])
        
        book_list.append(
            {
                "title":title,
                "currency":currency,
                "price":price
            }
        )

    return book_list


all_books = scrape_books(url)


with open("books.json" , 'w' , encoding='utf-8') as f:  # encoding= 'utf-8' and ensure_ascii=False is done so the symbol of the currency comes 
    books = json.dump(all_books,f , indent=4 , ensure_ascii=False)


with open("book.csv" , 'w' , newline="" , encoding='utf-8') as f:
    writer = csv.DictWriter(f , fieldnames=['title','currency','price'])
    writer.writeheader()
    writer.writerows(all_books)