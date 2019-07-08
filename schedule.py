from multiprocessing import Process
import crawlxici
import test
import time
import threading
from settings import *
class Schedule(object):
    def __init__(self):
        self.getter=crawlxici.Getter()
        self.tester=test.Tester()


    def schedule_get(self):
        while True:
            self.getter.run()
            time.sleep(50)
    def schedule_test(self):
        while True:
            self.tester.run()
            time.sleep(50)
    def run(self):

        if GET_ENABLE:
            get=threading.Thread(target=self.schedule_get)
            #get = Process(target=self.schedule_get)
            get.start()

        if TEST_ENABLE:
            test=threading.Thread(target=self.schedule_test)
            #test = Process(target=self.schedule_test)
            test.start()