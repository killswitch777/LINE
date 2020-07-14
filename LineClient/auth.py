# -*- coding: utf-8 -*-
from loguru import logger
from typing import Optional

import urllib, base64, os
import axolotl_curve25519 as curve

from .server import Server
from .callback import Callback
from .thrift import THttpClient

from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL

from LineThrift.ttypes import *
from LineThrift import TalkService, CallService, LiffService, SecondaryQrCodeLoginService, SecondaryQrCodeLoginPermitNoticeService

def create_message(*args):
    return "\n".join(args)


class Auth(object):
    isLogin = False

    accessToken: str = None
    certificate: str = None

    def __init__(self, appType: Optional[str] = None, secondary: bool = False):
        if appType == 'IOS':
            self.appName = ApplicationType.IOS
            self.secondary = True
        elif appType == 'IOSIPAD':
            self.appName = ApplicationType.IOSIPAD
            self.secondary = False
        elif appType == 'ANDROIDLITE':
            self.appName = ApplicationType.ANDROIDLITE
            self.secondary = True
        elif appType == 'DESKTOPWIN':
            self.appName = ApplicationType.DESKTOPWIN
            self.secondary = False
        elif appType == 'DESKTOPMAC':
            self.appName = ApplicationType.DESKTOPMAC
            self.secondary = False
        elif appType == 'CHROMEOS':
            self.appName = ApplicationType.CHROMEOS
            self.secondary = False
        self.server = Server(self.appName, self.secondary)
        self.callback = Callback(self.__defaultCallback)
        self.systemName = None

        self.__concurrency = 30
        url = URL(self.server.LINE_HOST_DOMAIN)
        self.__client = HTTPClient(url.host,
                                   url.port,
                                   concurrency=self.__concurrency,
                                   ssl=True,
                                   connection_timeout=180.0,
                                   network_timeout=180.0)

    def __loadSession(self):
        self.call     = self.createSession(self.server.CALL_SERVICE_HOST, CallService.Client,
                                          self.__client)
        self.talk     = self.createSession(self.server.TALK_SERVICE_HOST, TalkService.Client,
                                          self.__client)
        self.poll     = self.createSession(self.server.POLL_SERVICE_HOST, TalkService.Client,
                                          self.__client)
        self.liff     = self.createSession(self.server.LIFF_SERVICE_HOST, LiffService.Client,
                                          self.__client)
        self.revision = self.poll.getLastOpRevision()
        self.isLogin  = True
    
    def loginWithQrCode(self):
        if self.systemName is None:
            self.systemName = self.server.systemName
        self.tauth = self.createSession(self.server.LINE_LOGIN_REQUEST_V1,
                                   SecondaryQrCodeLoginService.Client, self.__client)
        sessionId   = self.tauth.createSession(CreateQrSessionRequest()).authSessionId
        callbackURL = self.tauth.createQrCode(CreateQrCodeRequest(sessionId)).callbackUrl
        secret      = self.genE2EESecret()
        self.callback.QrUrl(create_message(f'{callbackURL}{secret}'))
        self.server.set_accessToken('')
        self.checkVerified = self.createSession(self.server.LINE_LOGIN_CHECK_V1,
                                         SecondaryQrCodeLoginPermitNoticeService.Client,
                                         self.__client)
        self.checkVerified.checkQrCodeVerified(CheckQrCodeVerifiedRequest(sessionId))
        try:
            self.tauth.verifyCertificate(VerifyCertificateRequest(sessionId, None))
            return
        except SecondaryQrCodeException:
            pinCode = self.tauth.createPinCode(CreatePinCodeRequest(sessionId)).pinCode
            self.callback.PinVerified(create_message(pinCode))
            self.checkVerified.checkPinCodeVerified(CheckPinCodeVerifiedRequest(sessionId))
        lReq = self.tauth.qrCodeLogin(QrCodeLoginRequest(sessionId, self.systemName, True))
        self.loginWithAuthToken(lReq.accessToken)

    def loginWithAuthToken(self, authToken=None):
        if authToken is None:
            raise Exception('Please provide Auth Token')
        if self.appName is None:
            self.appName=self.server.appName
        self.server.set_accessToken(authToken)
        self.accessToken = authToken
        self.__loadSession()

    def genE2EESecret(self):
        private_key = curve.generatePrivateKey(os.urandom(32))
        public_key = curve.generatePublicKey(private_key)

        secret = urllib.parse.quote(base64.b64encode(public_key).decode())
        version = 1
        return f"?secret={secret}&e2eeVersion={version}"
    
    def createTransport(self,
                        url: str,
                        client: Optional[HTTPClient] = None) -> THttpClient:
        if client:
            return THttpClient(url,
                               self.server.Headers(),
                               self.__concurrency,
                               client=client)
        else:
            return THttpClient(url, self.server.Headers(),
                               self.__concurrency)
        
    def createSession(self,
                       url: str,
                       service_client,
                       http_client: Optional[HTTPClient] = None):
        self.trans = self.createTransport(url, http_client)
        self.proto = TCompactProtocolAcceleratedFactory().getProtocol(self.trans)
        return service_client(self.proto)
    
    def __defaultCallback(self, str):
        logger.info(str)