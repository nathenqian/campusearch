from crawler.crawler import Crawler
from eventlet import monkey_patch

if __name__ == "__main__":
    # monkey_patch()
    crawler = Crawler("/home")
    