#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from typing import Union, TYPE_CHECKING

from ..collection.arraylist import ArrayList
from ..maps import Dictionary

if TYPE_CHECKING:
    from ._hook import HookSendBefore, HookSendAfter
else:
    class HookSendBefore:
        pass

    class HookSendAfter:
        pass

_HTTP_RE = re.compile(f"^http|https?:/{2}\\w.+$")
re.purge()

_OPTIONAL_ARGS_KEYS = ["params", "data", "json", "headers", "cookies", "files", "auth", "timeout", "allow_redirects",
                       "proxies", "verify", "stream", "cert", "stream"]

ResponseBody = Union[Dictionary, ArrayList]
Hooks = Union[list[Union[HookSendBefore, HookSendAfter]], Union[HookSendBefore, HookSendAfter]]


class _Constant:
    HTTPS = "https"
    SERVER_NAME = "serverName"
    SERVER_HOST = "serverHost"
    OPTS = "opts"
    APIS = "apis"
    API_NAME = "apiName"
    API_PATH = "apiPath"
    DESC = "desc"
    HTTP_METHOD = "httpMethod"
    HEADERS = "headers"
    CONTENT_TYPE = "Content-Type"
    ALLOW_REDIRECTS = "allow_redirects"
    CONTENT_TYPE_DEFAULT = "application/x-www-form-urlencoded"
    CONTENT_TYPE_JSON = "application/json"
    RESPONSE = "response"
    RESTFUL = "restful"
