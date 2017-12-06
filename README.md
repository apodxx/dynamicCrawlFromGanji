# 动态爬取赶集网招聘信息
> 最近闲得很,所以趁这段时间重拾关于爬虫的一些东西 教程的内容就是利用Python将赶集网中动态信息爬取下来

### 我们的需求
1.我们先看下[赶集网招聘](http://linyi.ganji.com/zpshichangyingxiao/),也就是我们要爬取的内容
![index首页](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/%E9%A6%96%E9%A1%B51.png)

我们需要的名称
![招聘名称](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/name.png)
![招聘联系人和电话](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/phone_linkman.png)


### 需要的内容
1. Python环境及配置pip源
	* 这些东西网上都有自行百度即可
2. requests
	* [request的安装及方法](http://blog.csdn.net/shanzhizi/article/details/50903748)
3. urllib2
	* [urilib2的相关内容总结](https://www.cnblogs.com/wly923/archive/2013/05/07/3057122.html)
4. xpath
	* [xpath的相关内容总结](https://www.cnblogs.com/fdszlzl/archive/2009/06/02/1494836.html)
	* 这个部分需要好好理解一下 如果你学过正则表达式或者beatuifulsoup 那么代码中的部分替换即可  

### 第一步
![第一步图片](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/name1.png)
![第二步图片](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/name2.png)
找到我们要爬取的代码,然后使用`urllib2`来获取网页内容, 得到网页内容然后使用`xpath`提取到每个招聘信息的网址

	crawlUrl = "http://linyi.ganji.com/	zpshichangyingxiao"
	response = urllib2.urlopen(crawlUrl)
	html = response.read();
	selector = etree.HTML(html)
	# 提取文本
	content = selector.xpath(
    "//dl[@class='list-noimg job-list clearfix new-dl']/dt/a[@class='list_title gj_tongji']/@href")
    
    
  ![代码结果](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/result2.png)
   
### 第二步
我们发现上面代码结果 有的是

	http://linyi.ganji.com/zpshichangyingxiao/2583479190x.htm
	
有的是
   
	http://aozdclick.ganji.com/gjadJump?gjadType=3&target=pZwY0jCfsvQGUM-GshI6UhGGshPfUiql0ZPCpyPCmyOMXy-8uL6GmytfnW9LPW0OPHcdng98pZwVFhc3PWc3PA7bsyFWnvmVPjT3nzdBPjTksHbdnANzuW93m1DknamLn19dPHmOnjDhnHNQnWTYn1ndPjcYPHbzFWc3P1mLrHNzPHDhn1TLxadtsimzxjnkxadtsiuBnW9YrjNdPaYvrA7BsHEdnjbVmH9OnBdBuWDQn1NYPHP6nHmhnHNQnWNYP19OPWEznzuMphQG0LwluamQnzukmgF6UimkFhOdUAkhNZ-YpAq8sgRzUAQGmBtzsW0hnHT8nHnvsWckna33nzu8IyQ_FWDhFhOdUAk&end=end
	
而如果我们打开上面的长的连接,发现网址栏却是

	http://linyi.ganji.com/zpshichangyingxiao/2876795251x.htm
这个就说明网页发生了重定向 类似于JavaEE中的 response.sendRedirect()这个方法 因此 我们需要使用`request`得到得到我们真正要跳转到的网址,并保存到list中,代码如下:

	i = 0;
	list=[]
	for each in content:
    	i += 1
    	if len(each) > 60:
        	url=requests.get(each)
        	list.append(url.url)
    	else:
        	list.append(each)
        
部分代码结果:

	![代码结果](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/result1.png)
	
      
        	
### 第三步
将第二步中的结果遍历然后切割字符串得到后面的的数字,例如:

	http://linyi.ganji.com/zpshichangyingxiao/2705159292x.htm
通过截取得到

	2705159292
至于为什么要这么做 我在后面会讲述,在此处先埋一个坑.

	urlContent=[];
	for i in list:
    	splits=i.split("/")
    	id=splits[len(splits)-1][:-5]
    	urlContent.append(id)
将截取的内容保存到urlContent中    	
   
### 第四步
这也是最重要的一步,我们先在此处贴出代码然后一步步分析

	cookie = '''GANJISESSID=abe790f7f7bc1b03045b3a2ab843fe16; path=/; domain=.ganji.com'''
我们知道 一般我们在登录了一个网站后,网页便会产生一个cookie,什么是cookie?当然不是小甜饼,简单地说就是登录访问地址后留下的记录,详细的可以参考的百度百科,如果我们没有添加cookie而是直接添加访问那么后面操作得不到手机号和联系人信息,爬取的页面也会重定向首页
	
		
	header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
	'Connection': 'keep-alive',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Cookie': cookie
	}
header的作用就是模仿浏览器进行操作,并将cookie添加到请求头中,否则浏览器会认为是程序在抓取,继而浏览器报500的错误

	for j in range(len(urlContent)):
    	requesturl = 'http://www.ganji.com/pub/pub.php?act=pub&method=load&cid=11&jobinfo=237%2C161728&reply=113%3B'+urlContent[j]+'%3B2&fbranch=i&domain=jn&is_iframe=1&from=viewFullPhone&source_position=wanted_detail_tel_pub'
    	wbdata = requests.get(requesturl, headers=header).text
    	content = etree.HTML(wbdata)					content1=etree.HTML(
    	urllib2.urlopen(list[j]).read())
    	name = content1.xpath("//div[@class='d-c-left-hear']/h1[@class='f24 fc4b h31']/text()")
    	tel = content.xpath("//div[@class='apply-pos-v2-tit']/b/text()")
    	linkman = content.xpath("//div[@class='apply-pos-v2-tit']/span[@class='font-grey']/text()")
    	print name[0]+tel[0]+"\t"+linkman[0]    
接下来就是重点了,敲黑板!!! 当我们打开保存在list中的存放的链接的时候,我们发现在网页源代码中并没有发现我们需要的手机号,哪去那里了呢?
这其实就是前面说的页面的动态加载,手机号等信息是使用js动态渲染出来的,所以 这时我们需要右键`检查`,找到`network`中的`all`,然后点击`查看完成电话`,会发现下方列表中会出现很多信息,如图
 
 ![动态网页](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/QQ20171206-175527%402x.png)
 ![动态网页1](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/js1.png)
 ![动态网页2](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/js1.png)
 
找到上面的图片中那一项 我们发现我们请求的真正的url,在代码也就是requesturl,这里面有两个键值对是需要我们注意的是reply,jobinfo和domain,我们会发现jobinfo这个信息,毫无规律可言,事实上,后面如果不写这个键值对也是可以的,因此可以忽略,reply如果我们仔细发现应该是
307%3B+请求url的中的数字(也就是我们第三步中截取的内容)+3%3B2&,domain是什么 就不说了.
	
	请求的url:
	http://linyi.ganji.com/zpshichangyingxiao/2898829283x.htm
	动态加载的url:
	http://www.ganji.com/pub/pub.php?act=pub&
	method=load&
	cid=11&
	jobinfo=237%2C2610&
	reply=307%3B2898829283%3B2&
	fbranch=i&
	domain=linyi&
	is_iframe=1&
	from=viewFullPhone&
	source_position=wanted_detail_tel_pub
	
	请求的url:
	http://linyi.ganji.com/zpshichangyingxiao/2869001712x.htm
	动态加载的url:
	http://www.ganji.com/pub/pub.php?act=pub&method=load&
	cid=11&
	jobinfo=237%2C161728&
	reply=307%3B2869001712%3B2&
	fbranch=i&
	domain=linyi&
	is_iframe=1&
	from=viewFullPhone&
	source_position=wanted_detail_tel_pub
	
	

这里,同时看到`Set-Cookie`这个键,这就是上面我们需要填充的cookie信息,同时看到`response`这个选项,里面的html内容会找到我们需要的手机号和联系人,所以就如上方的代码一样 ,遍历list中所有的链接然后得到所有手机号

### 第五步
经历上面几步的操作 我们最终看到输出结果

![代码结果](https://github.com/apodxx/dynamicCrawlFromGanji/blob/master/image/result.png)

最后附上代码地址:
	[gitbub地址](https://github.com/apodxx/dynamicCrawlFromGanji/tree/master/code/ganji)
	
### 总结
正如前言,这个代码就是在闲的蛋疼的情况下而写,此代码存在很多的不足,第一就是抓取页面单单只是第一页中招聘信息,第二是并没有实现页面的模拟登陆,而是次而选择cookie导致每过一段时间,session回话无效时需要更换,故而程序不健壮,最后整体代码是以面向过程的方式写出来,部分代码的重用性很垃圾,所以写此教程以供以后查看 如果你有比较好的建议可以向我发起issiue或者request,也可以在下方评论区给我评论
	
    	
    	 	
    



	
	
	

