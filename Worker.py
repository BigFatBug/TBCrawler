# -*- coding: utf8 -*-

import time
import re
import json
import requests
import threading
from datetime import datetime
from MongoHandler import MongoHandler


class Worker(threading.Thread):
    def __init__(self, objectUrl):
        super(Worker, self).__init__()
        self.objectUrl = objectUrl
        self.objectId = None
        self.queryId = int(time.time())
        self.mongoHandler = MongoHandler()
        self.mongoHandler.update('status', 'queryId', self.queryId, {'queryId': self.queryId, 'status': 0, 'msg': '开始工作'})

    def run(self):
        objectId = self.getObjectId(self.objectUrl)
        if not objectId:
            self.mongoHandler.update('status', 'queryId', self.queryId, {'queryId': self.queryId, 'status': 1, 'msg': '商品id解析失败'})
            raise Exception('商品Id解析失败')
        self.objectId = objectId
        self.mongoHandler.update('status', 'queryId', self.queryId,
                                 {'queryId': self.queryId, 'status': 2, 'msg': '商品id解析完成'})
        self.getTags(objectId)
        self.getRate(objectId)

    def getObjectId(self, objectUrl):
        try:
            return re.match('.*[&\?]id=([0-9]+)', objectUrl).groups()[0]
        except Exception:
            raise Exception('商品Id解析失败')

    def getJson(self, data):
        return re.search('{.*}', data).group()

    def getTags(self, objectId):
        '''
        {"watershed": 100, "sellerRefundCount": 0, "isRefundUser": true, "showPicRadio": true, "data": {
            "impress": [{"count": 344, "attribute": "620-11", "scm": "", "title": "质量不错", "value": 1},
                        {"count": 95, "attribute": "10120-11", "scm": "", "title": "服务好", "value": 1},
                        {"count": 92, "attribute": "420-11", "scm": "", "title": "物流快", "value": 1},
                        {"count": 46, "attribute": "1020-11", "scm": "", "title": "正品", "value": 1},
                        {"count": 26, "attribute": "20520-11", "scm": "", "title": "性价比很高", "value": 1},
                        {"count": 3, "attribute": "4647-11", "scm": "", "title": "有问必答", "value": 1},
                        {"count": 11, "attribute": "620-13", "scm": "", "title": "质量一般", "value": -1}],
            "count": {"normal": 0, "totalFull": 2623, "total": 2623, "bad": 0, "tryReport": 5, "goodFull": 2623,
                      "additional": 67, "pic": 345, "good": 2623, "hascontent": 0, "correspond": 0}, "attribute": [],
            "newSearch": false, "correspond": "0.0", "spuRatting": []}, "skuFull": false, "isShowDefaultSort": true,
         "askAroundDisabled": true, "skuSelected": false}
        '''
        res = {}
        tagUrl = 'https://rate.taobao.com/detailCommon.htm?auctionNumId={0}'
        r = requests.get(tagUrl.format(objectId))
        if not r.status_code == 200:
            raise Exception('HTTP错误。状态码为' + r.status_code)
        aa = self.getJson(r.text)
        ss = json.loads(self.getJson(aa))
        res['tags'] = ss['data']['impress']
        res['count'] = ss['data']['count']
        self.mongoHandler.update('info', 'objectId', objectId, res)
        return ss

    def getRate(self, objectId):
        '''
        {"qnaDisabled": true, "watershed": 100,
         "search": "http://11.180.249.209:30051/bin/sp?app=pinglun&outfmt=json&seek_timeout=400&gmt_create=1461513600~&rate_risk_limit=0&item_id=18447203638&risk_time_now=1524635794&layer_quota=500000&rate_risk_search=1&no_risk_status=0%7C-1&order=gmt_create:des&s=0&n=1&is_wireless=0&user_id=0&utd_id=2d3eed51c4b0bd1f37e72b98658fbf95&is_click_sku=0",
         "total": 19879, "comments": [{"date": "2018年04月25日 13:36",
                                       "shareInfo": {"lastReplyTime": "", "share": false, "pic": 0, "reply": 0,
                                                     "userNumIdBase64": ""}, "showDepositIcon": false, "o2oRate": null,
                                       "mainTradeId": 0, "raterType": 0, "validscore": 1, "video": null, "photos": [],
                                       "content": "此用户没有填写评价。", "rateId": 1000650095008, "spuRatting": [],
                                       "auction": {"thumbnail": "",
                                                   "link": "//item.taobao.com/auction/item_detail.htm?item_num_id=18447203638",
                                                   "auctionPic": "//img.alicdn.com/bao/uploaded/null_40x40.jpg",
                                                   "sku": "颜色分类:黑色二层宽15CM  尺码:S（2尺1-2尺6）腰围", "title": "",
                                                   "aucNumId": "18447203638"}, "award": "", "rate": "1",
                                       "creditFraudRule": 0, "appendCanExplainable": false, "from": "b2cMapping",
                                       "tag": "", "propertiesAvg": "0.0", "reply": null, "dayAfterConfirm": 0,
                                       "lastModifyFrom": 0, "bidPriceMoney": null, "noQna": true, "promotionType": "",
                                       "vicious": "", "enableSNS": false, "appendList": [], "buyAmount": 0,
                                       "showCuIcon": false, "serviceRate": null, "useful": 0,
                                       "user": {"nick": "寒***炙", "vipLevel": 6, "displayRatePic": "b_red_4.gif",
                                                "nickUrl": "", "anony": false, "rank": 107,
                                                "avatar": "//wwc.alicdn.com/avatar/getAvatar.do?userIdStr=vFkSPFHuXH*evF8LPmHSXHc0vFl-MF8bvmg4MkcLMGh-PClIMCQyPk8GPCZIv8kG&width=40&height=40&type=sns",
                                                "vip": "b_red_1.gif", "userId": "", "rankUrl": ""}, "append": null,
                                       "status": 0}], "currentPageNum": 1, "maxPage": 5}
        '''
        objectId = str(objectId)
        pageNum = 1
        pageMax = 1
        total = -1
        i = 0
        rateUrl = 'https://rate.taobao.com/feedRateList.htm?auctionNumId={0}&currentPageNum={1}&pageSize=20&rateType=&orderType=feedbackdate'
        try:
            maxIndex = self.mongoHandler.getData('info', {'objectId': objectId})['total']
            sku = self.mongoHandler.getData('info', {'objectId': objectId})['sku']
        except:
            maxIndex = 0
            sku = {}
        finish = False
        while pageNum <= pageMax:
            r = requests.get(rateUrl.format(objectId, pageNum))
            if not r.status_code == 200:
                raise Exception('HTTP错误。状态码为' + r.status_code)
            aa = self.getJson(r.text)
            ss = json.loads(self.getJson(aa))
            if total == -1:
                total = ss['total']
                if total == 0:
                    break
                pageMax = (total - 1) // 20 + 1
                self.mongoHandler.update('info', 'objectId', objectId, {'total' :total, 'pageMax': pageMax})

            for comment in ss.get('comments') or []:
                if total - i <= maxIndex:
                    finish = True
                    break
                try:
                    commentDate = datetime.strptime(comment['date'], "%Y年%m月%d日 %H:%M")
                except Exception:
                    commentDate = None
                try:
                    for c in comment['auction']['sku'].split('&nbsp;&nbsp'):
                        if ':' in c:
                            name, key = c.split(':')
                            sku[name][key] = sku.setdefault(name, {}).setdefault(key, 0) + 1
                except Exception:
                    pass
                commentModel = {
                    'objectId': objectId,
                    'tag': comment['tag'],
                    "index": total - i,
                    'comment': comment['content'],
                    'commentId': comment['rateId'],
                    'rateType': comment['rate'],
                    'sku': comment['auction']['sku'],
                    'user': comment['user']['nick'],
                    'commentDate': str(commentDate.date()) if commentDate else '',
                    'commentTime': commentDate.strftime("%Y-%m-%d %H:%M:%S") if commentDate else '',
                    'createTime': datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                    'updateTime': datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.mongoHandler.insertComment(commentModel)
                i += 1
                if i % 3000 == 0:
                    self.mongoHandler.update('status', 'queryId', self.queryId,
                                             {'queryId': self.queryId, 'status': 3, 'msg': '已抓取第%s条评论' % i})

            if finish:
                break

            if pageNum == 1:
                self.mongoHandler.update('status', 'queryId', self.queryId,
                                         {'queryId': self.queryId, 'status': 3, 'msg': '已抓取第一页评论'})
            pageNum += 1
        self.mongoHandler.update('info', 'objectId', objectId, {'sku' :sku})
        self.mongoHandler.update('status', 'queryId', self.queryId,
                                 {'queryId': self.queryId, 'status': 4, 'msg': '完成评论抓取'})


if __name__ == '__main__':
    c = Worker(
        'https://item.taobao.com/item.htm?spm=a230r.1.14.248.914b6443cNP7Wu&id=37900975113&ns=1&abbucket=6#detail',
        'test')
    c.start()
