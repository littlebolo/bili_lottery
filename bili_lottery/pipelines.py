# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class BiliLotteryPipeline:
    def __init__(self):
        self.mid_seen = set()

    def process_item(self, item, spider):
        if item['mid'] in self.mid_seen:
            raise DropItem('见过这个人了：%s' % item)
        else:
            self.mid_seen.add(item['mid'])

        return item
