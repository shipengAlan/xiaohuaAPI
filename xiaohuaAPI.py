#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from lxml import html
import re
import random


class XiahuaClient(object):

    """docstring for XiahuaClient"""

    def __init__(self):
        pass

    def __cn_charcode(self, text):
        text = text.encode('latin-1','ignore').decode('GBK', 'ignore').encode('utf-8', 'ignore')
        return text

    def getNum(self):
        url = r'http://www.zbjuran.com/wenzixiaohua/list_1_1.html'
        headers = {
            'Host': 'www.zbjuran.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Connection': 'keep-alive',
        }
        r = requests.get(url, headers=headers)
        text = r.text
        tree = html.fromstring(text)
        match_list = tree.xpath(r'/html/body/div[4]/div[1]/div[7]/a')
        allnum = match_list[-1].get('href')
        pattern = re.compile('list_1_(\d+)\.html')
        match = pattern.match(allnum)
        allnum = match.group(1)
        return int(allnum)

    def getRandomItem(self, allnum=2395, num=1):
        itemnum = []
        pagenum = []
        for i in range(num):
            pagenum.append(random.randint(1, allnum))
            itemnum.append(random.randint(1, 6))
        headers = {
            'Host': 'www.zbjuran.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Connection': 'keep-alive',
        }
        data = []
        for i in range(num):
            url = 'http://www.zbjuran.com/wenzixiaohua/list_1_%d.html' % pagenum[i]
            r = requests.get(url, headers=headers)
            text = r.text
            tree = html.fromstring(text)
            item = itemnum[i] if itemnum[i] != 4 else 6
            match_title = tree.xpath(r'/html/body/div[4]/div[1]/div[%d]/h3/a/b' % item)
            match_href = tree.xpath(r'/html/body/div[4]/div[1]/div[%d]/h3/a' % item)
            temp_match_content = tree.xpath(r'/html/body/div[4]/div[1]/div[%d]/div[1]/p/a' % item)
            match_content = temp_match_content[0].xpath('text()')
            idata = {}
            idata['title'] = self.__cn_charcode(match_title[0].text)
            idata['content'] = self.__cn_charcode(''.join(match_content))
            idata['id'] = match_href[0].get('href')
            if idata['content'] == None or idata['content'] == '':
                str_item = self.getItem(idata['id'])
                dict_item = json.loads(str_item)
                idata['content'] = dict_item[0]['content']
            data.append(idata)
        return json.dumps(data, ensure_ascii=False)

    def getItem(self, htmlid):
        headers = {
            'Host': 'www.zbjuran.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Connection': 'keep-alive',
        }
        data = []
        url = 'http://www.zbjuran.com%s' % htmlid
        r = requests.get(url, headers=headers)
        text = r.text
        tree = html.fromstring(text)
        match_title = tree.xpath(r'/html/body/div[4]/div[1]/div[1]/div[1]/h1')
        temp_match_content = tree.xpath(r'/html/body/div[4]/div[1]/div[1]/div[2]/p')#
        str_match_content = ''
        for j in range(len(temp_match_content)):
            match_content = temp_match_content[j].xpath('text()')
            str_match_content += ''.join(match_content).strip()
        idata = {}
        idata['title'] = self.__cn_charcode(match_title[0].text)
        idata['content'] = self.__cn_charcode(str_match_content)
        idata['id'] = str(htmlid)
        data.append(idata)
        return json.dumps(data, ensure_ascii=False)

if __name__ == '__main__':
    xhc = XiahuaClient()
    #xhc.getRandomItem(1,2)
    xhc.getItem('/wenzixiaohua/201508/31517.html')
