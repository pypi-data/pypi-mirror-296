#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Callable, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ._rest import RestResponse
else:
    class RestResponse:
        pass


class HookSendBefore:
    """
    run at the http send request before
    """

    def __init__(self, run: Callable[[dict], dict], order: int = 0):
        self.__run: Callable[[dict], dict] = run
        self.__order: int = order

    def __eq__(self, other):
        return self.__run == other.__run and self.__order == other.__order

    def __hash__(self):
        return hash(self.__run) + self.__order

    def __str__(self):
        return f"{self.__run.__name__}:{self.__order}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.__order < other.__order

    def run(self, kwargs) -> dict:
        return self.__run(kwargs)


class HookSendAfter:
    """
    run at the http send request before
    """
    def __init__(self, run: Callable[[RestResponse], RestResponse], order: int = 0):
        self.__run: Callable[[RestResponse], RestResponse] = run
        self.__order: int = order

    def __eq__(self, other):
        return self.__run == other.__run and self.__order == other.__order

    def __hash__(self):
        return hash(self.__run) + self.__order

    def __str__(self):
        return f"{self.__run.__name__}:{self.__order}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.__order < other.__order

    def run(self, response: Optional[RestResponse]) -> RestResponse:
        return self.__run(response)


def filter_hook(hooks, excepted_type: type) -> list:
    hooks_list = []
    if isinstance(hooks, excepted_type):
        hooks_list.append(hooks)
    elif isinstance(hooks, list):
        hooks_list.extend((hook for hook in hooks if isinstance(hook, excepted_type)))
    return hooks_list
