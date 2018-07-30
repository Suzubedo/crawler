# -*- coding: utf-8 -*-
import scrapy
import re


PHONES_BRANDS = ['samsung', 'iphone', 'huawei', 'lg', 'lenovo', 'sony', 'honor']
#PHONES_BRANDS = ['samsung']

class QuotesSpider(scrapy.Spider):
    name="rueducommerce"
    def start_requests(self):
        for brand in PHONES_BRANDS:
            urls = ['https://www.rueducommerce.fr/marque/' + brand + '?page=1&sort=ventes&universe=MC-3533&area=MC-3604&view=list']
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for product in response.css('article'):

            #Gathering information about name
            list_name = product.css('h2 span::text').extract()
            name = ""
            for word in list_name:
                name = name + word

            price = product.css('div.price::text').extract_first()
            centimes = product.css('div.price sup::text').extract_first()
            if price:
                price = re.sub('[\r\n\t€ ]', '', price)
            yield {
                        'name': name,
                        'price': price,
                        'centimes': centimes
                        } 

        next_page_tmp = response.css('div.pagination a.next::attr(href)').extract_first()
        if next_page_tmp is not None:
            next_page = 'https://www.rueducommerce.fr' + next_page_tmp + '&sort=ventes&universe=MC-3533&area=MC-3604&view=list'
            yield scrapy.Request(next_page, callback=self.parse)
