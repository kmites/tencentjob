# -*- coding: utf-8 -*-
import scrapy
from tencentjob.items import TencentjobItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    baseURL = "http://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [baseURL+str(offset)]

    def parse(self, response):
        position_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for position in position_list:
            item = TencentjobItem()
            if len(position.xpath("./td[1]/a/text()")):
                item["positionName"] = position.xpath("./td[1]/a/text()").extract()[0]
            else:
                item["positionName"] = ""
            if len(position.xpath("./td[1]/a/@href")):
                item["positionLink"] = position.xpath("./td[1]/a/@href").extract()[0]
            else:
                item["positionLink"]= ""
            if len(position.xpath("./td[2]/text()")):
                item["positionType"] = position.xpath("./td[2]/text()").extract()[0]
            else:
                item["positionType"] = ""
            if position.xpath("./td[3]/text()"):
                item["positionNum"] = position.xpath("./td[3]/text()").extract()[0]
            else:
                item["positionNum"] = ""
            if len(position.xpath("./td[4]/text()")):
                item["positionPlace"] = position.xpath("./td[4]/text()").extract()[0]
            else:
                item["positionPlace"] = ""
            if len(position.xpath("./td[5]/text()")):
                item["positionTime"] = position.xpath("./td[5]/text()").extract()[0]
            else:
                item["positionTime"] = ""
            yield item

        #方法1：拼接url
        # if self.offset<2260:
        #     self.offset +=10
        #     url = self.baseURL+str(self.offset)
        #     yield scrapy.Request(url,callback=self.parse)

        #方法2：获取下一页的链接
        if len(response.xpath("//div[@class='pagenav']/a[@id='next']")):
            url = "http://hr.tencent.com/"+response.xpath("//div[@class='pagenav']/a[@id='next']/@href").extract()[0]
            #print(url,type(url))
            yield scrapy.Request(url, callback=self.parse)

