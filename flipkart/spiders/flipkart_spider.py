import scrapy
from ..items import FlipkartItem

class FlipkartSpider(scrapy.Spider):
    search_item = input("Enter the item you want:")
    max_page_number = int(input("Enter the pages you want to search:"))
    name = "flipkart"
    page_number = 2
    start_urls = [f"https://www.flipkart.com/search?q={search_item}"]

    def parse(self, response):
        items = FlipkartItem()
        results = response.css('div._2kHMtA')

        for result in results:
            li = result.css('a._1fQZEK::attr(href)').extract_first()
            name = result.css('div._4rR01T::text').extract_first()
            rating = result.css('._2_R_DZ').css('::text').extract_first()
            price = result.css('div._30jeq3._1_WHN1::text').extract_first()
            link = f'https://www.flipkart.com{li}'

            items["Product_Name"] = name
            items['Product_Price'] = price
            items['Link'] = link
            items['Product_Rating'] = rating
            yield items

        next_page = f"https://www.flipkart.com/search?q={FlipkartSpider.search_item}&page={FlipkartSpider.page_number}"
        if (FlipkartSpider.page_number <= FlipkartSpider.max_page_number):
            FlipkartSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)