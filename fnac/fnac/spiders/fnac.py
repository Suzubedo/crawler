# -*- coding: utf-8 -*-
import scrapy
import re


PHONES_BRANDS = ['samsung', 'iphone', 'huawei', 'lg', 'lenovo', 'sony', 'honor']

class QuotesSpider(scrapy.Spider):
    name="fnac"
    def start_requests(self):
        for brand in PHONES_BRANDS:
            urls = ['https://www.fnac.com/SearchResult/ResultList.aspx?SCat=34!1%2c34002!2&Search=' + brand + '&sft=1&sl']
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for product in response.css('div.Article-itemGroup'):
            price = product.css('a.userPrice::text').extract_first()
            centimes = product.css('a.userPrice sup::text').extract_first()
            if not price:
                price = product.css('strong.userPrice::text').extract_first()
                centimes = product.css('a.userPrice sup::text').extract_first()
            if price:
                price = re.sub('[\r\n\t€ ]', '', price)
            yield {
                        'name': product.css('p.Article-desc a.js-minifa-title::text').extract_first(),
                        'price': price,
                        'centimes': centimes
                        } 

        next_page = response.css('li.nextLevel1 a::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

