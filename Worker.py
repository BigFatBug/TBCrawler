# -*- coding: utf8 -*-
'''
评论url: https://rate.taobao.com/feedRateList.htm?auctionNumId=557643935853&userNumId=285630199&currentPageNum=1&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=099%23KAFEWGEKEyGEIETLEEEEE6twScwYV6NTSr3En60qS9lqC6gHZcn4S6fTDX9oC6fcJGFETRpCD6xlE7EFL2xhGW4TEHIThX9mi1m0D4DBKsT2cmf3kfMQ%2B1V%2BhN%2BoShxA0FEf1Nvkcrmop7P0DbAkWhj2iNfKwxXGkLHBiDvkcIYboSt6w4QluBfrkg4Iww1ZMJK01Fa6O7FEpcZdtqwlluAysyaAa3llsqiP%2F36alllzgcZdddallu8osyaAa3llWy%2B%2FE7EhssaZt6iFJ7FE1cZdt2U9F%2BrsgGFTIORRDhQScblcL4wsDR7W1GStasB2qy163Me6r02ScYb63oCYa0uVaYST1ryBvw4ta7nEQtoB8RdtlLnLY0ColGOuxrC%2B%2FTU71abqbIZ28vdl%2FnsPnzUolnQsi2X28Tqpx4U3PtCCcYFlaquYSR4f9BZc32wTPaFpLiZprt2B6YCcaQhvDs2X1LsuxOrmhjLu9aSuV65ohnlta7CWSy8k%2FLDu3X3xhK4EGwQRL6ZDOIQwcGszaT82Eals3rhYIVIulGT1doc2U%2Fls3%2FlPnKI0lGIuuuyiUzOs3%2Fd1Qq508YEluasgzKex3%2Fd1llJw8zAlcQs3OohCvUPcwq%2FCYyIZa7Pc%2B2w0cRITaGe6PPXnFQOcLYhPCR4i%2BYO3EXJj8TYulnsETGFETrZSt3illV5TEEiP%2F3BG&_ksTS=1510897731330_1429&callback=jsonp_tbcrate_reviews_list
核心参数  auctionNumId=557643935853,currentPageNum=1,pageSize=20

物品url: https://detail.tmall.com/item.htm?id=40372254105
标签url: https://rate.tmall.com/listTagClouds.htm?itemId=563885044581&isAll=true&isInner=true&t=1524198195979&_ksTS=1524198195979_1306&callback=jsonp1307
'''
import re
import json
import requests
import threading


class Worker(threading.Thread):

    def __init__(self, objectUrl, queryId):
        super(Worker,self).__init__()
        self.objectUrl = objectUrl
        self.queryId = queryId

    def run(self):
        objectId = self.getObjectId(self.objectUrl)
        tagList = self.getTags(objectId)
        res = self.getRate(objectId)

    def getObjectId(self, objectUrl):
        return re.match('.*id=([0-9]+)', objectUrl).groups()[0]

    def getJson(self, data):
        return re.search('{.*}', data).group()

    def getTags(self, objectId):
        tagUrl = 'https://rate.taobao.com/detailCommon.htm?auctionNumId={0}'
        r = requests.get(tagUrl.format(objectId))
        aa = self.getJson(r.text)
        ss = json.loads(self.getJson(aa))
        return ss

    def getRate(self, objectId):
        objectId = str(objectId)
        pagenum = 1
        results = {}
        rateUrl = 'https://rate.taobao.com/feedRateList.htm?auctionNumId={0}&currentPageNum={1}&pageSize=100&rateType=&orderType=feedbackdate'
        while 1:
            r = requests.get(rateUrl.format(objectId, pagenum))
            aa = self.getJson(r.text)
            ss = json.loads(self.getJson(aa))
            lastpage = ss['paginator']['lastPage']
            contents = [i['rateContent'] for i in ss['rateList']]
            results[pagenum] = contents
            if pagenum != lastpage:
                pagenum += 1
                continue
            else:
                break
        with open('ratetmall_single.json', 'w') as f:
            f.write(
                json.dumps(results, sort_keys=True, indent=4, separators=(',', ': ')))
        print('Finished')
        return 'ok'


if __name__ == '__main__':
    c = Worker('https://item.taobao.com/item.htm?spm=a230r.1.14.248.914b6443cNP7Wu&id=41464813277&ns=1&abbucket=6#detail', 'test')
    c.start()
    # c.getrate_tmall(558540134751)