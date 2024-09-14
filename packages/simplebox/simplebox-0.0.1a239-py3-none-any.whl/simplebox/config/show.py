#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
temp show all config run as python command line
~: python -m simplebox.config.show
"""
from inspect import currentframe, getframeinfo
from pathlib import Path

stack = getframeinfo(currentframe().f_back)
if stack.function != "_run_code" and Path(stack.filename).name != "runpy.py":
    raise ImportError("not found module")
else:
    import os
    from simplebox.config.log import LogConfig
    from simplebox.config.rest import RestConfig
    from simplebox.config.property import PropertyConfig
    from simplebox.config.json import JsonConfig
    from simplebox.config.serialize import SerializeConfig
    os.environ['SB_BANNER_OFF'] = 'False'
    LogConfig.off_banner = True
    LogConfig.off = True
    print(LogConfig)
    print(RestConfig)
    print(PropertyConfig)
    print(JsonConfig)
    print(SerializeConfig)
