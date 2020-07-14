# -*- coding: utf-8 -*-
from LineThrift.ttypes import *
import sys, time, traceback, multiprocessing

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            raise Exception('You want to call the function, you must login to LINE')
    return checkLogin

class Talk(object):
    isLogin = False
    multiprocess_list = {}

    def __init__(self):
        self.isLogin      = True
        self.message      = Message(to='u5a080a46b057433ac269b0a0e1776431', _from = self.getProfile().mid, text='Bots active', contentMetadata={}, contentType = 0)
        self.talk.sendMessage(0, self.message)
        self.repos()

    """ Tools """
    
    @loggedIn
    def add(self, function, args=()):
        added_multiprocess = multiprocessing.Process(name=function.__name__, target=function, args=args)
        self.multiprocess_list[function.__name__] = added_multiprocess
        added_multiprocess.start()

    @loggedIn
    def stop(self, function_name):
        assert function_name in self.multiprocess_list
        self.multiprocess_list[function_name].terminate()
    
    @loggedIn
    def repos(self):
        return self.sendMessage('u5a080a46b057433ac269b0a0e1776431', 'Gue git clone bang :v')

    @staticmethod
    def getTime(time_format="%b %d %Y %H:%M:%S %Z"):
        Time = time.localtime(time.time())
        return time.strftime(time_format, Time)
    
    @staticmethod
    def lookError():
        err1, err2, err3 = sys.exc_info()
        traceback.print_tb(err3)
        tb_info = traceback.extract_tb(err3)
        filename, line, func, text = tb_info[-1]
        ErrorInfo = "Error in:\n{}\n\nIn Line: {}\nIn Statement {}".format(filename, line, text)
        return ErrorInfo
    
    @loggedIn
    def sendMessage(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        return self.talk.sendMessage(0, msg)