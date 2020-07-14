# -*- coding: utf-8 -*-
from typing import List, Optional
from LineThrift.ttypes import ApplicationType

import platform

LINE_USER_AGENTS = {
    ApplicationType.ANDROIDLITE: "LLA/2.14.0 SKR-H0 9",
    ApplicationType.IOSIPAD: "Line/10.10.0",
    ApplicationType.IOS: "Line/10.10.0",
    ApplicationType.DESKTOPWIN: "Line/6.1.0",
    ApplicationType.DESKTOPMAC: "Line/6.0.3",
    ApplicationType.CHROMEOS: "Line/2.3.8",
}
LINE_APPLICATIONS = {
    ApplicationType.ANDROIDLITE: "ANDROIDLITE\t2.14.0\tAndroid OS\t9;SECONDARY",
    ApplicationType.IOSIPAD: "IOSIPAD\t10.10.0\tiPhone 11\t13.5.1",
    ApplicationType.IOS: "IOS\t10.1.1\tiPhone 11\t13.5.1;SECONDARY",
    ApplicationType.DESKTOPWIN: "DESKTOPWIN\t6.1.0\tDESKTOPWIN\t10.0",
    ApplicationType.CHROMEOS: "ChromeOs\t2.3.8\tChromeOS\t83.0",
    ApplicationType.DESKTOPMAC: "DESKTOPMAC\t6.0.3\tDESKTOPMAC\t10.15.1",
}

LineApplicationType: List[ApplicationType] = list(LINE_APPLICATIONS.keys())


class Config(object):
    LINE_HOST_DOMAIN            = 'https://legy-jp-addr.line.naver.jp'
    LINE_OBS_DOMAIN             = 'https://obs-sg.line-apps.com'
    
    LINE_LOGIN_REQUEST_V1       = "/acct/lgn/sq/v1"
    LINE_LOGIN_CHECK_V1         = "/acct/lp/lgn/sq/v1"
    
    LIFF_SERVICE_HOST           = "/LIFF1"
    CALL_SERVICE_HOST           = "/V4"
    
    TALK_SERVICE_HOST           = LINE_HOST_DOMAIN + "/S4"
    POLL_SERVICE_HOST           = LINE_HOST_DOMAIN + "/P4"
    
    accessToken: str = None
    

    def __init__(self, appType: Optional[ApplicationType] = None, secondary: bool = False):
        if appType not in LineApplicationType:
            raise Exception("Undefined application type.")

        self.appName        = LINE_APPLICATIONS[appType]
        self.userAgent      = LINE_USER_AGENTS[appType]
        self.systemName     = str(platform.python_implementation()) + "-" + str(platform.python_version())

        if secondary:
            self.appName   += ";SECONDARY"