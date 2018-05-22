# -*- coding: utf-8 -*-
import scrapy
from Quotes.items import QuotesItem


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def start_requests(self):
        print('test')
        print('merge')
        print('modify in dev')

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotesItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next_uri = response.css('.pager .next a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_uri)
        yield scrapy.Request(url=next_page_url, callback=self.parse)
