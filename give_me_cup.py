# -*- coding: utf-8 -*-

import json
import hashlib

class CupLottery:
    def __init__(self, candidates, spell):
        self.candidates = candidates

        # 生成咒语hash
        md5 = hashlib.md5()
        md5.update(spell.encode('utf-8'))
        self.__spell_hash = int(md5.hexdigest(), 16)

        # 把用户id升序排列
        self.__mids = []
        for candidate in candidates:
            self.__mids.append(int(candidate['mid']))
        self.__mids.sort()

    def draw(self):
        # 生成获奖者位置
        # 把咒语hash每5位切片，作为百分比乘以抽奖名单人数，取整获得中奖者在名单上的具体位置
        # 最后一片长度可能不足，舍弃
        hash_string = str(self.__spell_hash)
        hash_slices = [hash_string[p:p+5] for p in range(0, len(hash_string), 5)][:-1]
        positions = [round(int(slice)*0.00001*len(self.candidates)) for slice in hash_slices]

        # 抽奖！
        # 遍历抽奖名单返回获奖者列表
        winners = []
        winners_id = [self.__mids[id] for id in positions]
        for candidate in self.candidates:
            for id in winners_id:
                if candidate['mid'] == str(id):
                    winners.append(candidate)
        return winners

def main():
    spell = input('请输入抽奖咒语：')
    spell = '小菠萝不是毒奶' if not spell else spell

    # 打开评论用户列表文件
    with open('output.json', 'r') as f:
        candidates = json.load(f)
    
    cup = CupLottery(candidates, spell)
    winners = cup.draw()[:3]

    print('获奖名单：%s' % winners)

if __name__ == '__main__':
    main()