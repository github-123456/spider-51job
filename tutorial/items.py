# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.selector import Selector
from openpyxl import Workbook
import re


class PostItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    post = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    publish_time = scrapy.Field()
    formalized_salary = scrapy.Field()
    post_href = scrapy.Field()
    instances = []

    def create(html, keys):
        selector = Selector(text=html)
        # print(html)
        instance = PostItem()
        instance["post"] = str(selector.css(".t1 ").xpath("./span/a/text()").extract_first()).strip()
        if PostItem.__match_key(instance["post"], keys) is False:
            print(instance["post"], " dost not match key", keys)
            return None
        instance["company_name"] = str(selector.css(".t2").xpath("./a/text()").extract_first()).strip()
        instance["location"] = str(selector.css(".t3").xpath("./text()").extract_first()).strip()
        instance["salary"] = str(selector.css(".t4").xpath("./text()").extract_first()).strip()
        instance["publish_time"] = str(selector.css(".t5").xpath("./text()").extract_first()).strip()
        instance["formalized_salary"] = PostItem.__formalize_salary(instance["salary"])
        instance["post_href"] = str(selector.css(".t1 ").xpath("./span/a").css("::attr(href)").extract_first()).strip()

        PostItem.instances.append(instance)

        if instance["salary"] == "None":
            instance["salary"] = ""

        return instance

    def save_excel(items, path):
        print("writing to excel...")
        s = set()
        company_set = set()
        s_len = 0
        list = []
        repeat_count = 0
        for i in items:
            s.add(i["post_href"])
            company_set.add(i["company_name"])
            if s.__len__() > s_len:
                list.append(i)
            else:
                repeat_count = repeat_count + 1
            s_len = s.__len__()
        items = list
        print("filtered", repeat_count, "repeated items.  post count:", items.__len__(), "company count:",
              company_set.__len__())
        wb = Workbook()
        ws = wb.active
        ws.append(["职位数量：{0},企业数量：{1}".format(items.__len__(), company_set.__len__())])
        ws.append(['职位名', '公司名', '工作地点', '薪资', '发布时间', 'FS(最低月薪/元)', '职位链接'])
        for item in items:
            row = [item[v] for v in item.keys()]
            ws.append(row)
        wb.save(path)
        print("finished writing")

    def __str__(self):
        return str(self.items())

    def __formalize_salary(salary):
        group1 = re.match("^\d+", salary)
        group2 = re.match("\d+(\.\d+)", salary)
        if group1 is None:
            return None
        group = group1.group()
        if group2 is not None:
            group = group2.group()
        n = float(group)

        if salary.__contains__("千"):
            n = n * 1000
        elif salary.__contains__("万"):
            n = n * 10000
        if salary.__contains__("年"):
            n = n / 12
        elif salary.__contains__("天"):
            n = n * 30
        elif salary.__contains__("时"):
            n = n * 30 * 8

        return int(n)

    @staticmethod
    def __match_key(literal, keys):
        upper_literal = str(literal).upper()
        for i in keys:
            upper_key = str(i).upper()
            if upper_key in upper_literal:
                return True
        return False
