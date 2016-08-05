```
# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib

url = 'http://www.cjcv.org.cn'
anti_leech = 'http://www.cjcv.org.cn'
timeout = 10
# 设置保存cookie的文件，同级目录下的cookie.txt
filename = 'cookie.txt'
headers = { 
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:29.0) Gecko/20100101 Firefox/29.0',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Referer': anti_leech, # 反盗链，跳过 您访问的链接存在安全风险。若果您接受此风险，请点击"继续,我接受此风险."按钮继续访问。
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }   

request = urllib2.Request(url, None, headers)
# cookie
'''
# 不保存cookie到文件
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
'''

# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
# 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
# 通过handler来构建opener
opener = urllib2.build_opener(handler)

try:
  response = opener.open(request, timeout=timeout)
  for item in cookie:
    print item.name + "   =========>   " + item.value
  print response.read()
  # 保存cookie到文件
  # cookie.save(ignore_discard=True, ignore_expires=True)
except urllib2.HTTPError, e:
  print '='*20 + 'Error' + '='*20
  print e.code
  print e.reason
  print e.fp.read()
```
