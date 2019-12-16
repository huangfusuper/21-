#电影天堂
import requests
from lxml import etree
import xlwt
import pymysql


BASE_DOMAIN = "https://www.dytt8.net"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

#获取主界面的所由url
def get_detail_urls(url):
    #url = "https://www.dytt8.net/html/gndy/dyzz/list_23_1.html"
    response = requests.get(url, headers=HEADERS,timeout=60000)
    # gb2312
    text = response.content.decode('gbk', 'ignore')
    # 格式化html
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    #传入url 按照冒号第一个操作 作为后续操作，循环冒号的第二个参数
    detail_urls = map(lambda url:BASE_DOMAIN+url,detail_urls)
    return detail_urls

#解析
def parse_detail_page(url):
    response = requests.get(url,headers=HEADERS)
    text = response.content.decode("gbk","ignore")
    html = etree.HTML(text)
    movie = {}
    #标题
    try:
        title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
        movie['title']=title
    except:
        movie['title'] = "爬取失败"
    try:
        zoom_e = html.xpath("//div[@id='Zoom']")[0]
        #电影信息
        infos = zoom_e.xpath(".//text()")
        index = 0;
        for info in infos:
            info = info.strip()
            if info.startswith("◎译　　名"):
                yiming = parse_info("◎译　　名",info)
                movie['yiming'] = yiming
            # elif info.startswith("◎片　　名"):
            #     pianming = parse_info("◎片　　名", info)
            #     movie['pianming'] = pianming
            elif info.startswith("◎年　　代"):
                niandai = parse_info("◎年　　代", info)
                movie['niandai'] = niandai
            elif info.startswith("◎产　　地"):
                chandi = parse_info("◎产　　地", info)
                movie['chandi'] = chandi
            elif info.startswith("◎类　　别"):
                leibie = parse_info("◎类　　别", info)
                movie['leibie'] = leibie
            elif info.startswith("◎语　　言"):
                yuyan = parse_info("◎语　　言", info)
                movie['yuyan'] = yuyan
            elif info.startswith("◎字　　幕"):
                zimu = parse_info("◎字　　幕", info)
                movie['zimu'] = zimu
            elif info.startswith("◎上映日期"):
                syri = parse_info("◎上映日期", info)
                movie['syri'] = syri
            elif info.startswith("◎IMDb评分"):
                IMDb = parse_info("◎IMDb评分", info)
                movie['IMDb'] = IMDb
            elif info.startswith("◎豆瓣评分"):
                dbpf = parse_info("◎豆瓣评分", info)
                movie['dbpf'] = dbpf
            elif info.startswith("◎文件格式"):
                wjgs = parse_info("◎文件格式", info)
                movie['wjgs'] = wjgs

            elif info.startswith("◎视频尺寸"):
                spcc = parse_info("◎视频尺寸", info)
                movie['spcc'] = spcc
            elif info.startswith("◎文件大小"):
                wjdx = parse_info("◎文件大小", info)
                movie['wjdx'] = wjdx
            elif info.startswith("◎片　　长"):
                pc = parse_info("◎片　　长", info)
                movie['pc'] = pc
            elif info.startswith("◎导　　演"):
                dy = parse_info("◎导　　演", info)
                movie['dy'] = dy
            elif info.startswith("◎编　　剧"):
                bj = parse_info("◎编　　剧", info)
                movie['bj'] = bj
            elif info.startswith("◎主　　演"):
                zy = parse_info("◎主　　演", info)
                zy = zy.strip()+","
                for x in range(index+1,len(infos)):
                    actor=infos[x]
                    actor = actor.strip()+","
                    zy+=actor
                    if actor.startswith("◎"):
                        break
                movie['zy'] = zy
            elif info.startswith("◎标　　签"):
                bq = parse_info("◎标　　签", info)
                movie['bq'] = bq
            elif info.startswith("◎简　　介"):
                jj = parse_info("◎简　　介", infos[index+1])
                movie['jj'] = jj
            index+=1
    except:
        movie['yiming'] = "爬取失败"
        movie['niandai'] = "爬取失败"
        movie['chandi'] = "爬取失败"
        movie['leibie'] = "爬取失败"
        movie['yuyan'] = "爬取失败"
        movie['zimu'] = "爬取失败"
        movie['syri'] = "爬取失败"
        movie['IMDb'] = "爬取失败"
        movie['dbpf'] = "爬取失败"
        movie['wjgs'] = "爬取失败"
        movie['spcc'] = "爬取失败"
        movie['wjgs'] = "爬取失败"
        movie['wjdx'] = "爬取失败"
        movie['pc'] = "爬取失败"
        movie['dy'] = "爬取失败"
        movie['bj'] = "爬取失败"
        movie['zy'] = "爬取失败"
        movie['bq'] = "爬取失败"
        movie['jj'] = "爬取失败"
    # 海报
    try:
        image = zoom_e.xpath(".//img/@src")[0]
        movie['image'] = image
    except:
        movie['image'] = "未知"

    return movie

#解析详情
def parse_info(rule,info):
    return info.replace(rule, "").strip()


def spider(con,titles):
    views = []

    views.append(titles)
    base_url =  "https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
    for x in range(1,2):
        print("----------------第"+str(72)+"页-------------------")
        url = base_url.format(72)
        home_urls = get_detail_urls(url)
        for home_url in home_urls:
            #遍历每一页的所有电影的详情url
            dy_view=parse_detail_page(home_url)
            views.append(dy_view)
            break
    return views

def writeExcel(views):
    book = xlwt.Workbook();
    shell = book.add_sheet("电影天堂电影页")
    line = 0
    for movie in views:
        clo = 0
        for key in movie:
            shell.write(line, clo, movie.get(key))
            clo += 1
        line += 1
    book.save("电影天堂.xls")

def dbMysql(titles,views):
    db = pymysql.connect(host="cdb-obych0ne.bj.tencentcdb.com",port=10214, user="root", password="HUANGfu0110", db="test")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    cols = ", ".join('`{}`'.format(k) for k in titles.keys())
    val_cols = ', '.join('%({})s'.format(k) for k in titles.keys())
    sql="insert into dytt(%s) VALUES (%s)"
    res_sql = sql % (cols, val_cols)
    print(res_sql)
    cursor.executemany(res_sql,views)
    db.commit()
    db.close()

if __name__ == '__main__':
    titles = {
        "title": "电影名称",
        "yiming": "译名",
        "niandai": "年代",
        "chandi": "产地",
        "leibie": "类别",
        "yuyan": "语言",
        "zimu": "字幕",
        "syri": "上映日期",
        "IMDb": "IMDb评分",
        "dbpf": "豆瓣评分",
        "wjgs": "文件格式",
        "spcc": "视频尺寸",
        "wjdx": "文件大小",
        "pc": "片长",
        "dy": "导演",
        "bj": "编剧",
        "zy": "主演",
        "bq": "标签",
        "jj": "简介",
        "image": "海报"
    }
    response = requests.get("https://www.dytt8.net/html/gndy/dyzz/list_23_3.html",headers=HEADERS)
    text = response.content.decode("gbk", "ignore")
    html = etree.HTML(text)
    ys = html.xpath("//select[@name='sldd']/option/@value")
    views = spider(len(ys),titles)
    dbMysql(titles,views)



