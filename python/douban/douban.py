#!/usr/bin/env python
   
import urllib
import urllib2
import sys, re
import cookielib
import hashlib
import httplib
import StringIO

DEBUG = 1

def Connect2Web(addr):
   aResp = urllib2.urlopen(addr);
   web_pg = aResp.read();
   if DEBUG:
      print addr
      #print web_pg
   return web_pg

def getReviewList(url):
   reviews = []
   index = 0
   addr = url
   while True:
      web_pg = Connect2Web(addr)

      for line in StringIO.StringIO(web_pg):
        if ("http://book.douban.com/review/" in line):
          matchObj = re.search(r'a title="(.*)" href="(http://book.douban.com/review/[0-9]+/)', line)
          if matchObj:
             if DEBUG:
                print matchObj.group(1)
                print matchObj.group(2)
             reviews.append(matchObj.group(1))
             reviews.append(matchObj.group(2))

      # next page
      index = index + 10
      addr = url+'?start='+str(index)
      if addr not in web_pg:
         #print addr
         break

   return reviews  
   
def fetchContent(fp, review):
   web_pg = Connect2Web(review)
   # date
   matchObj = re.search(r'class="mn">([0-9 \-:]+)</span>', web_pg)
   if matchObj:
      print "date", matchObj.group(1)
      fp.write('<span class="mn">'+matchObj.group(1)+'</span><br>\n')

   # from which book
   matchObj = re.search(r'(<a href="http://book.douban.com/subject/[0-9]+/"><span property="v:itemreviewed">.*</span></a>)', web_pg)
   if matchObj:
      print matchObj.group(1)
      fp.write(matchObj.group(1)+'<br>\n')
   
   # the content
   matchObj = re.search(r'<span property="v:description" class="">(.*)<div class="clear"></div></span>', web_pg)
   if matchObj:
      #print matchObj.group(1)
      fp.write('<p>'+matchObj.group(1)+'</p><br>\n')
      fp.write('<a href="#top">Return<br></a>\n')

   return

def writeIndex(fp, reviews):
   fp.write('<div id="menu">\n')

   i = 1
   for review in reviews:
      if "http:" not in review:
         fp.write('<a href="#review'+str(i)+'">'+review+'</a><br>\n')
         i = i + 1

   fp.write("</div>\n")
   return

def main(argv):
   if argv:
      id = argv[0]
      url = "http://www.douban.com/people/"+id+"/reviews"
   else:   
      return

   reviews = getReviewList(url)
   # open the output file: blog.html
   outf = "reviews.html"
   fp = open(outf, 'w')

   # put html head
   fp.write("<html>\n")
   fp.write("<head>\n")
   fp.write("<title>My douban reviews page</title>\n")
   fp.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
   fp.write('<link rel="stylesheet" type="text/css" href="styles.css" />\n')
   #fp.write("<style>\n")
   #fp.write("body {background-color:lightgray}\n")
   #fp.write("h2   {color:blue}\n")
   #fp.write("p    {color:green;padding:20px;margin:100px;border:1px solid black;}\n")
   #fp.write("</style>\n")
   fp.write("</head>\n")
   fp.write('<body><div id="wrapper">\n')
   fp.write('<a name="top"></a><h1>My Douban Book Reviews</h1>\n')
   
   writeIndex(fp, reviews)
   
   fp.write('<div id="context">\n')
   i = 1
   for review in reviews:
      if "http:" in review:
         fetchContent(fp, review)
         fp.write('-------------------------------------<br><br><br><br>\n')
      else:
         fp.write('<a name="review'+str(i)+'"></a><h2>'+review+'</h2><br>\n')
         i = i+1
   fp.write("</div>\n")


   fp.write("</div></body></html>\n")
   fp.close


if __name__ == '__main__':
   usage = '''Usage:
   douban.py <person-id>
   '''
   print usage
   main(sys.argv[1:])
 
