# -*- coding: utf-8 -*-

import json
import hashlib
import os

class CupLottery:
    def __init__(self, candidates, spell):
        self.candidates = candidates

        # 生成咒语hash
        md5 = hashlib.md5()
        md5.update(spell.encode('utf-8'))
        self.__spell_hash = int(md5.hexdigest(), 16)
        print('咒语hash：%s' % self.__spell_hash)

        # 把用户id升序排列
        self.__mids = []
        for candidate in candidates:
            self.__mids.append(int(candidate['mid']))
        self.__mids.sort()

    def draw(self, count=3):
        # 生成获奖者位置
        # 把咒语hash每5位切片，作为百分比乘以抽奖名单人数，取整获得中奖者在名单上的具体位置
        # 最后一片长度可能不足，舍弃
        hash_string = str(self.__spell_hash)
        hash_slices = [hash_string[p:p+5] for p in range(0, len(hash_string), 5)][:-1]
        print('切片结果：%s' % hash_slices)
        positions = [int(int(slice)*0.00001*len(self.candidates)) for slice in hash_slices]
        # 去重
        positions = self.__deduplicate(positions)
        print('获奖者位置：%s' % positions)

        # 抽奖！
        # 遍历抽奖名单返回获奖者列表
        winners = []
        winners_id = [self.__mids[p] for p in positions]
        print('获奖者id：%s' % winners_id)

        for candidate in self.candidates:
            count = len(winners_id) if count >= len(winners_id) else count
            for id in winners_id[:count]:
                if int(candidate['mid']) == id:
                    winners.append(candidate)
        return winners

    def __deduplicate(self, li):
        # 列表去重且保持原有顺序
        duplicated = list(set(li))
        duplicated.sort(key=li.index)
        return duplicated

def main():
    spell = input('请输入抽奖咒语：')
    spell = '小菠萝才不是毒奶' if not spell else spell

    # 打开评论用户列表文件
    # with open('output.json', 'r') as f:
        # candidates = json.load(f)

    candidates = []

    # 遍历当前目录下的json文件
    paths = os.listdir(os.getcwd())
    for path in paths:
        if os.path.splitext(path)[1] == '.json':
            with open(str(path), 'r') as f:
                candidates.append(json.load(f))

    # 列表取交集
    def get_intersection(candidates):
        if len(candidates) == 1:
            return candidates[0]

        candidate_first = candidates[0]
        candidate_rest = candidates
        candidate_rest.pop(0)
        if len(candidate_rest) == 1:
            intersection = []
            for c1 in candidate_first:
                for c2 in candidate_rest[0]:
                    if int(c1['mid']) == int(c2['mid']):
                        intersection.append(c1)
                        break
            return intersection
        return get_intersection(candidate_rest)

    result = get_intersection(candidates)

    cup = CupLottery(result, spell)
    winners = cup.draw(7)

    print('获奖名单：%s' % winners)

if __name__ == '__main__':
    main()