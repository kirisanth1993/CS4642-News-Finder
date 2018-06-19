# -*- coding: utf-8 -*-
import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['https://www.news.lk/news']
    start_urls = ['http://https://www.news.lk/news/']
    
    

    def parse(self, response):
        self.log("The site "+response.url+" has been visited")
        