# -*- coding: utf-8 -*-
import scrapy
from quotetutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com/']
    start_urls = ['http://quotes.toscrape.com//']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()     # '.text::text'表获取.text类的文本部分
            author = quote.css('.author::text').extract_first() # extract_first提取一个内容
            tags = quote.css('.tags .tag::text').extract()      # extract提取多个内容，'.tags .tag::text'表获取tags类下tag类的文本部分
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
        #实现翻页，首先获取翻页的值
        next = response.css('.pager .next a::attr(href)').extract_first()
        #拼接URL
        url = response.urljoin(next)
        #反复调用URL
        yield scrapy.Request(url=url,callback=self.parse)

