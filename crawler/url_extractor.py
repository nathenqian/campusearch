from BeautifulSoup import BeautifulSoup
import urllib2
import re

filter_words = [
    '[\S]*166.111.120.[\S]*',
    #'.*(?i)\.(mso|tar|txt|asx|asf|bz2|mpe?g|MPE?G|tiff?|gif|GIF|png|PNG|ico|ICO|css|sit|eps|wmf|zip|pptx?|xlsx?|gz|rpm|tgz|mov|MOV|exe|jpe?g|JPE?G|bmp|BMP|docx?|DOCX?|pdf|PDF|rar|RAR|jar|JAR|ZIP|zip|gz|GZ|wma|WMA|rm|RM|rmvb|RMVB|avi|AVI|swf|SWF|mp3|MP3|wmv|WMV|ps|PS)$',
    '.*(?i)\.(mso|tar|txt|asx|asf|bz2|mpe?g|MPE?G|tiff?|gif|GIF|png|PNG|ico|ICO|css|sit|eps|wmf|zip|gz|rpm|tgz|mov|MOV|exe|jpe?g|JPE?G|bmp|BMP|rar|RAR|jar|JAR|ZIP|zip|gz|GZ|wma|WMA|rm|RM|rmvb|RMVB|avi|AVI|swf|SWF|mp3|MP3|wmv|WMV|ps|PS)$',
]
filters = [re.compile(s) for s in filter_words]

def _filter(lst):
    for f in filters:
       lst = [x for x in lst if f.search(x) is None]
    return lst


def extract_urls(html):
    soup = BeautifulSoup(html)
    url_lst = []
    for a in soup.findAll('a'):
        l = a.get('href')
        if l is not None:
            print l
            url_lst.append(l)
    return _filter(url_lst)
