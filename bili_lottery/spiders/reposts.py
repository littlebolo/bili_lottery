# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import BiliLotteryItem
import json


class RepostsSpider(scrapy.Spider):
    name = 'reposts'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id=391296525970312169']

    def start_requests(self):
        url = self.start_urls[0]
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        res = json.loads(response.body)
        reposts = res['data']['items']
        if type(reposts) != list:
            return

        for repost in reposts:
            card = json.loads(repost['card'])
            user = BiliLotteryItem()
            user['mid'] = card['user']['uid']
            user['name'] = card['user']['uname']
            yield user

        if res['data']['has_more'] == 1:
            offset = '&offset=' + str(res['data']['offset'])
            url = self.start_urls[0] + offset
            yield Request(url=url, callback=self.parse)