# -*- coding: utf-8 -*-
from LineThrift.ttypes import *
import requests, json

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            raise Exception('You want to call the function, you must login to LINE')
    return checkLogin

class Liff(object):

    isLogin = False

    def __init__(self):
        self.liffUrl = 'https://api.line.me/message/v3/share'
        self.isLogin = True
        self.__loginLiff()

    @loggedIn
    def __loginLiff(self):
        url = 'https://access.line.me/dialog/api/permissions'
        data = {
            'on': [
                'P',
                'CM'
            ],
            'off': []
        }
        headers = {
            'X-Line-Access': self.accessToken,
            'X-Line-Application': self.server.appName,
            'X-Line-ChannelId': '1606644641',
            'Content-Type': 'application/json'
        }
        return requests.post(url, headers=headers, data=json.dumps(data))