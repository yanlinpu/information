## win7-64 python urllib2 selenium phantomjs 动态网站爬虫

- 前提工作
  
  - python  https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi
  - pip https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz#md5=87083c0b9867963b29f7aba3613e8f4a
  - selenium `easy_install selenium` || `pip install selenium`
  - phantomjs(这里没有引用) https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip 
  - chromedriver(win7 只存在32，都可用) http://chromedriver.storage.googleapis.com/2.9/chromedriver_win32.zip
  
- 代码parse.py

  ```
  #coding=utf-8                                                                                                                                         
  import re
  import urllib
  import urllib2
  # http://stackoverflow.com/questions/9926023/handling-rss-redirects-with-python-urllib2
  # enable Cookies
  from cookielib import CookieJar
  
  from selenium import webdriver
  import time
  
  url_index = "http://mp.weixin.qq.com/s?__biz=MzI4MzAxOTMwMQ==&mid=2650083294&idx=4&sn=8bd9aef3b2f5266260bbdc7b002fc127&scene=23&srcid=0725z9egcLa6wKBuGeVi8Jmv#rd"
  
  def getHtml(url):
      cj = CookieJar()
      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
      page = opener.open(url)
      html = page.read()
      return html
  
  def getIndexUrl(html):
      reg = r'>(http\:\/\/medline\.org\.cn\/clinic\/subjectDetail\.do\?subjectId=.{2})<'
      urlre = re.compile(reg)
      urllist = re.findall(urlre, html)
      return urllist
  
  def getSubjectIdUrl(html):
      reg = r"href='(http\:\/\/.*)' target="
      urlre = re.compile(reg)
      urllist = re.findall(urlre, html)
      return urllist
  
  html_index = getHtml(url_index)
  indexs = getIndexUrl(html_index)
  #print len(indexs) #42
  driver = webdriver.Chrome('C:\chromedriver')
  file_object = open('download_url.txt', 'w')
  file_warn = open('download_warn_url.txt', 'w')
  try:
      for url_subjectid in indexs:
          print url_subjectid
          html_subject = getHtml(url_subjectid)
          for pdf_url in getSubjectIdUrl(html_subject):                
              try:
                  driver.get(pdf_url)
                  time.sleep(4)
                  id = pdf_url.split("/")[-1].split('.')[0]+"0"
                  e = driver.find_element_by_id(id)
              except:
                  file_warn.write(pdf_url)
                  file_warn.write("\n")                
                  print "Error: " + pdf_url
              else:
                  try:
                      file_object.write(e.get_attribute("href"))
                      file_object.write("\n")
                  except:
                      print "file write error: " + pdf_url
   
  
  finally:
      file_object.close()
      file_warn.close()
  ```

- 资料
  
  - [Python爬虫利器五之Selenium的用法](http://cuiqingcai.com/2599.html)
  - [抓取分析页面时，如何获取 JavaScript 动态产生内容？](http://www.zhihu.com/question/20269555)
  - [enable Cookies](http://stackoverflow.com/questions/9926023/handling-rss-redirects-with-python-urllib2)
  - [静觅--Python爬虫学习系列教程](http://cuiqingcai.com/1052.html)
  - [慕课网--Python开发简单爬虫](http://www.imooc.com/learn/563)
  - [基础爬虫](http://www.cnblogs.com/buptmuye/p/3462844.html)
  
