import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name="fnac"

#    def start_requests(self):
#        urls = [ 'https://www.fnac.com/Tous-les-ordinateurs-portables/Ordinateurs-portables/nsh154425/w-4#bl=MICOrdinateurs-portablesARBO'
 #       for url in urls:
 #           yield scrapy.Request(url=url, callback=self.parse)

    start_urls = ['https://www.fnac.com/SearchResult/ResultList.aspx?SCat=0%211&Search=samsung&sft=1&sa=0']
    #start_urls = ['http://quotes.toscrape.com/page/1/']


    def parse(self, response):
        for product in response.css('div.Article-itemGroup'):
            price_tmp = product.css('a.userPrice::text').extract_first()
            if not price_tmp:
                price_tmp = product.css('strong.userPrice::text').extract_first()
            if price_tmp:
                price_tmp = re.sub('[\r\n\t€ ]', '', price_tmp)
            yield {
                        'name': product.css('p.Article-desc a.js-minifa-title::text').extract_first(),
                        'price': price_tmp }

        next_page = response.css('li.nextLevel1 a::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
