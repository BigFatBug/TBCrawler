# -*- coding: utf8 -*-
'''
评论url: https://rate.taobao.com/feedRateList.htm?auctionNumId=557643935853&userNumId=285630199&currentPageNum=1&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=099%23KAFEWGEKEyGEIETLEEEEE6twScwYV6NTSr3En60qS9lqC6gHZcn4S6fTDX9oC6fcJGFETRpCD6xlE7EFL2xhGW4TEHIThX9mi1m0D4DBKsT2cmf3kfMQ%2B1V%2BhN%2BoShxA0FEf1Nvkcrmop7P0DbAkWhj2iNfKwxXGkLHBiDvkcIYboSt6w4QluBfrkg4Iww1ZMJK01Fa6O7FEpcZdtqwlluAysyaAa3llsqiP%2F36alllzgcZdddallu8osyaAa3llWy%2B%2FE7EhssaZt6iFJ7FE1cZdt2U9F%2BrsgGFTIORRDhQScblcL4wsDR7W1GStasB2qy163Me6r02ScYb63oCYa0uVaYST1ryBvw4ta7nEQtoB8RdtlLnLY0ColGOuxrC%2B%2FTU71abqbIZ28vdl%2FnsPnzUolnQsi2X28Tqpx4U3PtCCcYFlaquYSR4f9BZc32wTPaFpLiZprt2B6YCcaQhvDs2X1LsuxOrmhjLu9aSuV65ohnlta7CWSy8k%2FLDu3X3xhK4EGwQRL6ZDOIQwcGszaT82Eals3rhYIVIulGT1doc2U%2Fls3%2FlPnKI0lGIuuuyiUzOs3%2Fd1Qq508YEluasgzKex3%2Fd1llJw8zAlcQs3OohCvUPcwq%2FCYyIZa7Pc%2B2w0cRITaGe6PPXnFQOcLYhPCR4i%2BYO3EXJj8TYulnsETGFETrZSt3illV5TEEiP%2F3BG&_ksTS=1510897731330_1429&callback=jsonp_tbcrate_reviews_list
核心参数  auctionNumId=557643935853,currentPageNum=1,pageSize=20

物品url: https://detail.tmall.com/item.htm?id=40372254105
'''
import flask
import requests
import re
from xlwt import Workbook
import xlrd
import time


def key_name(number):
    # 获取页面的内容并返回
    name = '手机'
    URL_1 = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20170905&stats_click=search_radio_all%3A1&js=1&imgfile=&q="
    URL_2 = "&suggest=0_1&_input_charset=utf-8&wq=u&suggest_query=u&source=suggest&p4ppushleft=5%2C48&s="
    URL = (URL_1 + name + URL_2 + str(number))
    # print(URL)
    res = requests.get(URL)
    return res.text


def find_date(text):
    # 根据整个页面的信息，获取商品的数据所在的HTML源码并放回
    reg = r',"data":{"spus":\[({.+?)\]}},"header":'
    reg = re.compile(reg)
    info = re.findall(reg, text)
    return info[0]


def manipulation_data(info, N, sheet):
    # 解析获取的HTML源码，获取数据
    Date = eval(info)

    for d in Date:
        T = " ".join([t['tag'] for t in d['tag_info']])
        # print(d['title'] + '\t' + d['price'] + '\t' + d['importantKey'][0:len(d['importantKey'])-1] + '\t' + T)

        sheet.write(N, 0, d['title'])
        sheet.write(N, 1, d['price'])
        sheet.write(N, 2, T)
        N = N + 1
    return N


def main():
    book = Workbook()
    sheet = book.add_sheet('淘宝手机数据')
    sheet.write(0, 0, '品牌')
    sheet.write(0, 1, '价格')
    sheet.write(0, 2, '配置')
    book.save('淘宝手机数据.xls')
    # k用于生成链接，每个链接的最后面的数字相差48.
    # N用于记录表格的数据行数，便于写入数据
    k = 0
    N = 1
    for i in range(10 + 1):
        text = key_name(k + i * 48)
        info = find_date(text)
        N = manipulation_data(info, N, sheet)

        book.save('淘宝手机数据.xls')
        print('下载第' + str(i) + '页完成')


if __name__ == '__main__':
    main()