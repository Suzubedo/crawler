# -*- coding: utf-8 -*-
import scrapy
import re


PHONES_BRANDS = ['samsung', 'iphone', 'huawei', 'lg', 'lenovo', 'sony', 'honor']

#PHONES_BRANDS = ['huawei']

class QuotesSpider(scrapy.Spider):
    name="darty"
    def start_requests(self):
        for brand in PHONES_BRANDS:
            urls = ['https://www.darty.com/nav/recherche?p=200&s=relevence&text=' + brand + '&fa=693']
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for product in response.css('div.product_detail'):
            name = product.css('div.prd-name a::text').extract_first()
            price_tmp = product.css('span.darty_prix::text').extract_first()
            centimes = product.css('span.darty_cents::text').extract_first()
            if not price_tmp:
                price_tmp = product.css('strong.userPrice::text').extract_first()
            if price_tmp:
                price_tmp = re.sub('[\r\n\t€ ]', '', price_tmp)
            yield {
                        'name': name,
                        'price': price_tmp,
                        'centimes': centimes
                        } 

        next_page_text = response.css('div.darty_product_list_pages_list a::text').extract()
        next_page = response.css('div.darty_product_list_pages_list a::attr(href)').extract()
        if len(next_page_text) != 0 and "Page suivante" in next_page_text[-1]:
            yield response.follow(next_page[-1], callback=self.parse)

