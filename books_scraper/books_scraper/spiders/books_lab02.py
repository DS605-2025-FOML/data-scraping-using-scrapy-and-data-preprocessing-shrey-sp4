import scrapy
from ..items import BooksScraperItem
class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        'http://books.toscrape.com',
    ]
    def parse(self, response):
        all_books = response.css('article.product_pod')
        for book in all_books:
            items = BooksScraperItem()
            name = book.css('.product_pod h3 a::attr(title)').extract_first()
            price = book.css('.price_color::text').extract_first()
            availability = book.css('.availability::text').extract()[-1].strip()
            link = book.css('.thumbnail::attr(src)').extract_first()
            rating = book.css('.star-rating::attr(class)').extract_first().split()[-1]

            items['title'] = name
            items['price'] = price
            items['stock_availability'] = availability
            items['url_picture'] = link
            items['rating'] = rating

            yield items

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
