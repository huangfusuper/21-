import requests
from lxml import etree
import xlwt



#写excel
def writeExcel(movies):
    book = xlwt.Workbook();
    shell = book.add_sheet('豆瓣最近上映电影');

    line = 0
    for movie in movies:
        clo = 0
        for key in movie:
            shell.write(line,clo,movie.get(key))
            clo+=1
        line+=1

    book.save("豆瓣电影.xls")

#抓取页面网站
url = "https://movie.douban.com/cinema/nowplaying/beijing/";
headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.390',
                'Host': 'movie.douban.com'
           }

response = requests.get(url=url,headers=headers)
# print(response.text)

# with open('douban.html','w',encoding="utf-8") as fp:
#     fp.write(response.content.decode("utf-8"))
text = response.content.decode("utf-8")
#规则提取
html = etree.HTML(text)
ul = html.xpath("//ul[@class='lists']")[0]
#html_text=etree.tostring(ul,encoding="utf-8").decode("utf-8")
#print(etree.tostring(ul,encoding="utf-8").decode("utf-8"))
lis = ul.xpath("./li")
movies =[]
movie_title = {
        '电影名':'电影名',
        '评分':'评分',
        '上映年度':'上映年度',
        '全片时间':'全片时间',
        '地区':'地区',
        '导演':'导演',
        '主演':'主演',
        '评论数':'评论数',
        '海报地址':'海报地址'
}
movies.append(movie_title)
for li in lis:
    #电影名
    title = li.xpath("@data-title")[0]
    #评分
    score = li.xpath("@data-score")[0]
    #上映年度
    release=li.xpath("@data-release")[0]
    #全片时间
    duration=li.xpath("@data-duration")[0]
    #地区
    region=li.xpath("@data-region")[0]
    #导演
    director=li.xpath("@data-director")[0]
    #主演
    actors=li.xpath("@data-actors")[0]
    #评论数
    subject=li.xpath("@data-subject")[0]
    #海报
    image = li.xpath(".//img/@src")[0]
    movie = {
        '电影名':title,
        '评分':score,
        '上映年度':release,
        '全片时间':duration,
        '地区':region,
        '导演':director,
        '主演':actors,
        '评论数':subject,
        '海报地址':image
    }
    movies.append(movie)

writeExcel(movies)




