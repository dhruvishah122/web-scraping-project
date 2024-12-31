import scrapy
from pymongo import MongoClient 
from pathlib import Path
import datetime
client = MongoClient("mongodb+srv://dhruvi:123@webscraping.jzl82.mongodb.net/")
db=client.scrapy
def insertToDb(page ,title,rating,image,price,inStock):
    collection = db[page]
    doc = {"title":title,"rating":rating,"image":image,"price":price,"inStock":inStock,"date":datetime.datetime.now()}
    inserted=collection.insert_one(doc)
    return inserted.inserted_id
class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://books.toscrape.com/index.html"]

    def start_requests(self):
        urls=[
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
       
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        # Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        cards=response.css(".product_pod")
        
        for card in cards:
            title=card.css("h3 a::text").get()
            print(title)
            rating=card.css(".star-rating").attrib["class"].split(" ")[1]
            image = card.css(".image_container img")
            price=card.css(".price_color::text").get()
            availability=card.css(".availability")
            if len(availability.css(".icon-ok")) >0:
                inStock=True
            else:
                inStock=False
            insertToDb(page,title,rating,image.attrib["src"],price,inStock)