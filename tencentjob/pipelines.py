# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import json
import pymysql

class TencentjobPipeline(object):
    def __init__(self):
        # self.f = open("tencentjob.json","w")
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='xxxx', db='tencentjob',charset='utf8')
    def process_item(self, item, spider):
        # content = json.dumps(dict(item),ensure_ascii=False)+",\n"
        # self.f.write(content)
        p_name = item["positionName"]
        p_link = item["positionLink"]
        p_type = item["positionType"]
        p_num = item["positionNum"]
        p_place = item["positionPlace"]
        p_time = item["positionTime"]
        #print(type(p_name),p_name)
        sql = "insert into jobinfo (p_name,p_link,p_type,p_num,p_place,p_time) values (%s,%s,%s,%s,%s,%s)"
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql,[p_name,p_link,p_type,p_num,p_place,p_time])
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item
    def close_spider(self,spider):
        # self.f.close()
        self.cursor.close()
        self.conn.close()
