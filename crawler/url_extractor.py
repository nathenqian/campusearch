from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import re

filter_words = [
    '[\S]*166.111.120.[\S]*',
    #'.*(?i)\.(mso|tar|txt|asx|asf|bz2|mpe?g|MPE?G|tiff?|gif|GIF|png|PNG|ico|ICO|css|sit|eps|wmf|zip|pptx?|xlsx?|gz|rpm|tgz|mov|MOV|exe|jpe?g|JPE?G|bmp|BMP|docx?|DOCX?|pdf|PDF|rar|RAR|jar|JAR|ZIP|zip|gz|GZ|wma|WMA|rm|RM|rmvb|RMVB|avi|AVI|swf|SWF|mp3|MP3|wmv|WMV|ps|PS)$',
    '.*(?i)\.(mso|tar|txt|asx|asf|bz2|mpe?g|MPE?G|tiff?|gif|GIF|png|PNG|ico|ICO|css|sit|eps|wmf|zip|gz|rpm|tgz|mov|MOV|exe|jpe?g|JPE?G|bmp|BMP|rar|RAR|jar|JAR|ZIP|zip|gz|GZ|wma|WMA|rm|RM|rmvb|RMVB|avi|AVI|swf|SWF|mp3|MP3|wmv|WMV|ps|PS)$',
]
filters = [re.compile(s) for s in filter_words]
validator = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def _filter(orig_url, lst):

    def fix(url):
        if not url.startswith('http'):
            if  not url.startswith('/'):
                return None
            url = urljoin(orig_url, url)
            if validator.search(url) is None:
                return None
        return url

    for f in filters:
       lst = [x for x in lst if f.search(x) is None]
    lst = [fix(x) for x in lst]
    lst = [x for x in lst if x is not None]
    return lst


def extract_urls(url, html):
    soup = BeautifulSoup(html, 'lxml')
    url_lst = []
    for a in soup.findAll('a'):
        l = a.get('href')
        if l is not None:
            print l
            url_lst.append(l)
    return _filter(url, url_lst)
