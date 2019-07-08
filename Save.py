import pymongo
import random
from settings import *
import csv

class MyMongoClient(object):
    #增删查改


    def __init__(self):
        self.mongo_url=MONGO_URL
        self.mongo_db=MONGO_DB
        self.db_name=DB_NAME
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def save_data(self, data):
        #data为字典形式
        try:
            self.db[self.db_name].insert(data)
        except:
            print('Unknown Error')

    def delete_data(self, proxy):
        condition = {'ip': proxy}
        return self.db[self.db_name].remove(condition)

    def find_data(self,data):
        return self.db[self.db_name].find(data)

    def decrease_data(self,proxy):
        condition={'ip':proxy}
        data=self.db[self.db_name].update(condition,{'$inc':{'score':-1}})
    def max_data(self,proxy):
        condition={'ip':proxy}
        return self.db[self.db_name].update(condition,{'$set':{'score':100}})

    def get_all_ip(self):
        #生成器
        all_ip=self.db[self.db_name].find()
        for ip in all_ip:
            yield ip
    def batch(self,start,end):
        all_ip = self.db[self.db_name].find()
        all_iplist=[dict['ip'] for dict in all_ip]
        return all_iplist[start:end]

    def get_max_ip(self):
        '''
            API
        '''
        if self.db[self.db_name].find({'score':100}):
            max_ip_list=[ip['ip'] for ip in self.db[self.db_name].find()]
            max_ip=random.choice(max_ip_list)
            return max_ip
        else:
            max_ip=self.db[self.db_name].find().sort('score',pymongo.DSCENDING)[0]
            return max_ip
    def count(self):
        return self.db[self.db_name].find().count()


class FileSave(object):
    def __init__(self):
        self.path='data3.txt'

    def save_all_data(self,iplist):

        with open(self.path,'w') as file:
            file.writelines([ip.strip()+'\n' for ip in iplist])
