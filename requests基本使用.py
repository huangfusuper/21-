import requests

wd = {'wd':'中国'}
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.390'}
#发送请求
response = requests.get('https://www.baidu.com/s?wd=%E4%B8%AD%E5%9B%BD&rsv_spt=1&rsv_iqid=0xa5b8d8cb000bf3f2&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=17&rsv_sug1=14&rsv_sug7=101&rsv_sug2=0&inputT=3366&rsv_sug4=3367',headers=headers)

with open("baidu.html",'w',encoding="utf-8") as fp:
    fp.write(response.content.decode("utf-8"))

#查看相应内容
#print(response.text)
#查看相应内容 二进制
print(response.content.decode("utf-8"))
#查看地址
print(response.url)
#查看字符编码
print(response.encoding)
#查看响应码
print(response.status_code)



for key in wd:
    print(wd.get(key))