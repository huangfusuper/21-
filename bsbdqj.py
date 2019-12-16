import requests
import re
from lxml import etree
import csv
import threading
from queue import Queue

HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    "Host":"duanziwang.com",
    "Upgrade-Insecure-Requests":"1"
}


class Pro(threading.Thread):
    def __init__(self,page_queue,ac_queue,*args,**kwargs):
        super(Pro,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.ac_queue = ac_queue
    def run(self) :
        while True:
            if self.page_queue.empty():
                break
            page_url = page_queue.get()
            self.format_page(page_url)

    def format_page(self,url):
        response = requests.get(url=url, headers = HEADERS)
        text = response.text
        html = etree.HTML(text)
        posts = html.xpath("//article[@class='post']")
        for post in posts:
            title = post.xpath(".//h1[@class='post-title']/a/text()")[0]
            time = post.xpath(".//div[@class='post-meta']/time/text()")[0]
            self.ac_queue.put((title,time))
        print("="*30+"完成1页"+"="*30)

class Clm(threading.Thread):
    def __init__(self,ac_queue,write,gLock,*args,**kwargs):
        super(Clm,self).__init__(*args,**kwargs)
        self.ac_queue = ac_queue
        self.write = write
        self.gLock = gLock

    def run(self) :
        while True:
            try:
                title, time = self.ac_queue.get(40)
                self.gLock.acquire()
                self.write.writerow((title, time))
                self.gLock.release()
            except Exception as e:
                print(str(e))
                print("====异常")
                break




if __name__ == '__main__':
    page_queue = Queue(71)
    ac_queue = Queue(200)
    gLock = threading.Lock()
    fp = open('dz.csv','a',newline='',encoding='gbk')
    writer = csv.writer(fp)
    writer.writerow(('content','date'))
    #response = requests.get(,headers=HEADERS)
    for x in range(1,71):
        url = "http://duanziwang.com/category/%E4%B8%80%E5%8F%A5%E8%AF%9D%E6%AE%B5%E5%AD%90/"+str(x)
        page_queue.put(url)

for x in range(10):
    t = Pro(page_queue,ac_queue).start()
for x in range(10):
    t1 = Clm(ac_queue,writer,gLock).start()
