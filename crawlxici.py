import threading
# 队列
from settings import *
#from Queue import Queue
# 解析库
from lxml import etree
# 请求处理
from Save import MyMongoClient
from Save import FileSave
import requests
# json处理
import json
import time
class ProxyMetaClass(type):
    def __new__(cls,name,bases,attrs):
        count=0
        attrs['__CrawlFunc__']=[]
        for k,v in attrs.items():
            if "crawl_" in k:
                attrs['__CrawlFunc__'].append(k)
                count+=1
        attrs['__CrawlFuncCount__']=count
        return type.__new__(cls,name,bases,attrs)
    #将方法存入类属性

class Crawler(object,metaclass=ProxyMetaClass):

        #异步检测代理
        #持续运行
        #//*[@id="ip_list"]/tbody/tr[@class="odd"]
        #爬取ip,url存入队列
    def get_proxies(self,callback):
        proxies=[]
        for proxy in eval('self.{}()'.format(callback)):
            proxies.append(proxy)
        return proxies

    def crawl_89(self):
        base_url='http://www.89ip.cn/'

        for page in range(2):
            url=base_url+'index_{}.html'.format(page)
            try:
                response=requests.get(url,headers=HEADERS)
                if response.status_code == 200:
                    print('89第{}页爬取成功'.format(page))
                else:
                    print('89第{}页爬取失败，状态码{}'.format(page, response.status_code))

                html=etree.HTML(response.text)
                nodelist=html.xpath("//div[@class='layui-col-md8']//table//tbody//tr/td[1]/text()")
                for node in nodelist:
                    yield node
            except:
                print('89本页Failed')


    def crawl_xici(self):
        base_url='https://www.xicidaili.com/nn/'
        for page in range(BATCH_CRAWL_SIZE):
            if page>1:
                url=base_url+str(page)
            else:
                url=base_url
            #遍历每页
            try:
                response=requests.get(url,headers=HEADERS)
                time.sleep(4)
            #解析网页
                if response.status_code == 200:
                    print('xici第{}页爬取成功'.format(page))
                else:
                    print('xici第{}页爬取失败，状态码{}'.format(page,response.status_code))
                html = etree.HTML(response.text)
            #result = etree.tostring(html).decode('utf-8')
                nodelist=html.xpath('//*[@id="ip_list"]//tr//td[2]/text()')
                for node in nodelist:
                    yield node
            except:
                print('西刺本页Failed')



    def crawl_kuaidaili(self):

        base_url = 'https://www.kuaidaili.com/free'
        for page in range(2*BATCH_CRAWL_SIZE,3*BATCH_CRAWL_SIZE):
            if page > 1:
                url = base_url +'/inha/'+str(page)+'/'
            else:
                url = base_url

            try:
                response = requests.get(url, headers=HEADERS)
                time.sleep(3)
                # 解析网页
                #if response.status_code == 200:
                    #print('快代理第{}页爬取成功'.format(page))
                #else:
                    #print('快代理第{}页爬取失败，状态码{}'.format(page, response.status_code))
                html = etree.HTML(response.text)
                # result = etree.tostring(html).decode('utf-8')
                nodelist = html.xpath("//*[@id='list']/table/tbody/tr/td[@data-title='IP']/text()")
                for node in nodelist:
                    yield node
            except:
                print('快代理本页Failed')

class Getter(object):
    def __init__(self):
        self.db=MyMongoClient()
        #在
        self.local=FileSave()
        self.crawler=Crawler()
    def run(self):
        #t=threading.Thread
        print('一共有{}个爬虫'.format(len(self.crawler.__CrawlFunc__)))
        for func in self.crawler.__CrawlFunc__:
            iplist=self.crawler.get_proxies(func)
            self.local.save_all_data(iplist)
            for ip in iplist:

                ipdict={
                    'ip':ip.strip(),
                    'score':10
                }
                self.db.save_data(ipdict)
            print('ALL DONE')







