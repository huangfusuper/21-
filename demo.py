import threading
import requests
from lxml import etree
import os
import re
from queue import Queue

class Producer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)
        self.page_queue=page_queue
        self.img_queue=img_queue
    def run(self):
        while True:
            if(self.page_queue.empty()):
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}

        response = requests.get(url, headers=headers)
        text = response.text

        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
        for img in imgs:
            im_url = img.get("data-original")
            alt = img.get("alt")
            alt = re.sub(r'[\?\.\*，！“”。？]', '', alt)
            if (im_url != None):
                suff = os.path.splitext(im_url)[1]
                fileName = alt + suff
                print(fileName)
                self.img_queue.put((im_url,fileName))

class Consumer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}

    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer,self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if self.page_queue.empty() and self.img_queue.empty():
                break
        img_url,filename=self.img_queue.get()
        response = requests.get(img_url, headers=self.headers)
        with open("images/" + filename, 'wb') as fp:
            fp.write(response.content)

def main():
    page_queue = Queue(100)
    img_queue = Queue(1000)
    for x in range(1,101):
        url = "http://www.doutula.com/photo/list/?page=%d" %x
        page_queue.put(url)
    for x in range(5):
        t = Producer(page_queue,img_queue)
        t.start()
    for x in range(5):
        t = Consumer(page_queue,img_queue)
        t.start()

if __name__ == '__main__':
    main()