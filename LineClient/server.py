# -*- coding: utf-8 -*-
from .config import Config
from typing import Dict
import json, requests, urllib

class Server(Config):
    _session        = requests.session()
    timelineHeaders = {}

    def __init__(self, appType=None, secondary=False):
        self.timelineHeaders = {}
        Config.__init__(self, appType, secondary)

    def set_accessToken(self, accessToken: str):
        self.accessToken = accessToken

    def unset_accessToken(self):
        self.accessToken = None

    def Headers(self) -> Dict[str, str]:
        headers = {
            "User-Agent": self.userAgent,
            "X-Line-Application": self.appName,
            "x-lal": "id_ID",
        }

        if self.accessToken is not None:
            headers["X-Line-Access"] = self.accessToken

        return headers

    def urlEncode(self, url, path, params=[]):
        return url + path + '?' + urllib.parse.urlencode(params)

    def getJson(self, url, allowHeader=False):
        if allowHeader is False:
            return json.loads(self._session.get(url).text)
        else:
            return json.loads(self._session.get(url, headers=self.Headers).text)

    def setHeadersWithDict(self, headersDict):
        self.Headers().update(headersDict)

    def setHeaders(self, argument, value):
        self.Headers()[argument] = value

    def setTimelineHeadersWithDict(self, headersDict):
        self.timelineHeaders.update(headersDict)

    def setTimelineHeaders(self, argument, value):
        self.timelineHeaders[argument] = value

    def setLiffHeadersWithDict(self, headersDict):
        self.liffHeaders.update(headersDict)

    def setLiffHeaders(self, key, value):
        self.liffHeaders[key] = value

    def additionalHeaders(self, source, newSource):
        headerList={}
        headerList.update(source)
        headerList.update(newSource)
        return headerList

    def optionsContent(self, url, data=None, headers=None):
        if headers is None:
            headers = self.Headers()
        return self._session.options(url, headers=headers, data=data)

    def postContent(self, url, data=None, files=None, headers=None):
        if headers is None:
            headers = self.Headers()
        return self._session.post(url, headers=headers, data=data, files=files)

    def getContent(self, url, headers=None):
        if headers is None:
            headers = self.Headers()
        return self._session.get(url, headers=headers, stream=True)

    def deleteContent(self, url, data=None, headers=None):
        if headers is None:
            headers = self.Headers()
        return self._session.delete(url, headers=headers, data=data)

    def putContent(self, url, data=None, headers=None):
        if headers is None:
            headers = self.Headers()
        return self._session.put(url, headers=headers, data=data)