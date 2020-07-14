# -*- coding: utf-8 -*-
from .auth import Auth
from .server import Server
from .talk import Talk
#from .line import LineTalk
from .liff import Liff
from .models import Models
#from .database import Database
from LineThrift.ttypes import SyncReason

class LINE(Auth, Talk, Liff, Models):
    def __init__(self, idOrAuthToken=None, passwd=None, **kwargs):
        self.certificate = kwargs.pop('certificate', None)
        self.systemName = kwargs.pop('systemName', None)
        self.appType = kwargs.pop('appType', None)
        self.appName = kwargs.pop('appName', None)
        self.secondary = kwargs.pop('secondary', False)
        self.concurrency = kwargs.pop('concurrency', 30)
        Auth.__init__(self, self.appType, self.secondary)
        if not (idOrAuthToken or idOrAuthToken and passwd):
            self.loginWithQrCode()
        elif idOrAuthToken and not passwd:
            self.loginWithAuthToken(idOrAuthToken)
        self.__initAll()

    def __initAll(self):
        self.profile = self.talk.getProfile(SyncReason().FULL_SYNC)
        Talk.__init__(self)
        #LineTalk.__init__(self)
        Liff.__init__(self)
        Models.__init__(self)
        #Database.__init__(self, path=f'./{self.profile.mid}.db')