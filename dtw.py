import requests
from lxml import etree

import os
import re

def fromat_str(url):
    pass

def main():
    url = "http://www.doutula.com/photo/list/?page=1";
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}

    response = requests.get(url,headers=headers)
    text = response.text

    html = etree.HTML(text)
    imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
    for img in imgs:
        im_url = img.get("data-original")
        alt = img.get("alt")
        alt = re.sub(r'[\?\.\*，！“”。？]','',alt)
        if(im_url!=None):
            suff = os.path.splitext(im_url)[1]
            fileName = alt+suff
            print(fileName)
            response = requests.get(im_url,headers=headers)
            with open("images/"+fileName,'wb') as fp:
                fp.write(response.content)
if __name__ == '__main__':
    main()