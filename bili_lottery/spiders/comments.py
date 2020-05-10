# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import BiliLotteryItem
import json


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=883049596&pn=']
    current_page = 1

    def start_requests(self):
        url = self.start_urls[0] + str(self.current_page)
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        res = json.loads(response.body)
        replies = res['data']['replies']
        if type(replies) != list:
            return
        
        for reply in replies:
            user = BiliLotteryItem()
            user['mid'] = reply['member']['mid']
            user['name'] = reply['member']['uname']
            yield user

        self.current_page = self.current_page + 1
        url = self.start_urls[0] + str(self.current_page)
        yield Request(url=url, callback=self.parse)