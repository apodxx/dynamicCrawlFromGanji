# coding=utf=8
from lxml import etree
import requests
import sys
import urllib2
reload(sys)
sys.setdefaultencoding("utf-8")
cookie = '''GANJISESSID=abe790f7f7bc1b03045b3a2ab843fe16; path=/; domain=.ganji.com'''
header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
'Connection': 'keep-alive',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Cookie': cookie
}
crawlUrl = "http://linyi.ganji.com/zpshichangyingxiao"
response = urllib2.urlopen(crawlUrl)
html = response.read();
selector = etree.HTML(html)
# 提取文本
content = selector.xpath(
    "//dl[@class='list-noimg job-list clearfix new-dl']/dt/a[@class='list_title gj_tongji']/@href")
i = 0;
list=[]
for each in content:
    i += 1
    if len(each) > 60:
        url=requests.get(each)
        list.append(url.url)
    else:
        list.append(each)
print len(list)
urlContent=[];
for i in list:
    splits=i.split("/")
    id=splits[len(splits)-1][:-5]
    urlContent.append(id)
for j in range(len(urlContent)):
    url = 'http://www.ganji.com/pub/pub.php?act=pub&method=load&cid=11&jobinfo=237%2C161728&reply=113%3B'+urlContent[j]+'%3B2&fbranch=i&domain=jn&is_iframe=1&from=viewFullPhone&source_position=wanted_detail_tel_pub'
    wbdata = requests.get(url, headers=header).text
    content = etree.HTML(wbdata)
    content1=etree.HTML(urllib2.urlopen(list[j]).read())
    name = content1.xpath("//div[@class='d-c-left-hear']/h1[@class='f24 fc4b h31']/text()")
    tel = content.xpath("//div[@class='apply-pos-v2-tit']/b/text()")
    linkman = content.xpath("//div[@class='apply-pos-v2-tit']/span[@class='font-grey']/text()")
    print name[0]+tel[0]+"\t"+linkman[0]







