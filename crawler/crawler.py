from url import Url, g_uid, g_uid2url, g_url2uid
from os.path import join
from json import loads
from threading import Thread
from time import sleep
from .logger import Logger
from .green_downloader import GreenDownloader
from eventlet import monkey_patch, GreenPool
from select import select
from sys import stdin
class Crawler:
    def __init__(self, file_dir):
        self.thread_number = 10
        # file_dir must be a absolute dir
        self.file_dir = file_dir
        """
        init gid -> url
        init unfinished queue 
        """
        g_uid = 0
        g_uid2url = {}
        g_url2uid = {}

        try:        
            with open(join(file_dir, "gid_url.txt")) as f:
                buff_dict = loads(f.read())
                for i in buff_dict:
                    g_uid = max(g_uid, i)
                    g_uid2url[i] = buff_dict[i]
                    g_url2uid[buff_dict[i]] = i
        except Exception:
            g_uid = 0
            g_uid2url = {}
            g_url2uid = {}
            print "load gid_url failed."


        self.unfinished = []
        try:
            with open(join(file_dir, "unfinished.txt")) as f:
                buff_list = loads(f.read())
                for entry in buff_list:
                    self.unfinished.append(Url().parseDict(entry))
        except Exception:
            self.unfinished = []
            print "load unfinished task failed."

        self.doing_url = 0
        self.downloader = GreenDownloader(None, self.thread_number)
        self.todo_url = ["http://www.126.com" for i in range(1000)]
        self.logger = Logger.create("log")
        # monkey_patch()
        self.run()


    def run(self):
        try:
            while True:
                rlist, _, _ = select([stdin], [], [], 0.1)
                if rlist:
                    stdin_input = stdin.readline()
                    if stdin_input[0] == "i":
                        index = 1
                        while stdin_input[index] == ' ':
                            index += 1
                        self.todo_url.append(stdin_input[index:])

                while self.doing_url < self.thread_number:
                    if len(self.todo_url) == 0:
                        break
                    url = self.todo_url[0]
                    print "start doing " + url
                    self.todo_url = self.todo_url[1:]
                    self.downloader.input_queue.put({
                        "url" : url
                    })
                    self.doing_url += 1

                dispatcher = self.downloader.run()

                while not self.downloader.output_queue.empty():
                    obj = self.downloader.output_queue.get()
                    url = obj["url"]
                    print "end doing " + url
                    if "error_code" not in obj:
                        # correct
                        url = Url.create(url, obj["content"], {}, "DONE")
                    else:
                        # error
                        url = Url.create(url, None, {}, "ERROR")
                    self.logger.debug(url.url + ' ' + url.status + ' ' + url.content)
                    # todo parse url and add new url
                print "todo = " + str(len(self.todo_url))



        except KeyboardInterrupt:
            pass
        except Exception, e:
            print str(e)


    
