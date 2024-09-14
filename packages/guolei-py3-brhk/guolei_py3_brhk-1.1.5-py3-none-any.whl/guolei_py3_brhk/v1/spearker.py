#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
博瑞皓科 Speaker Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_brhk
=================================================
"""
from typing import Callable

import requests
from addict import Dict
from jsonschema.validators import validate, Draft202012Validator


class Api(object):
    """
    博瑞皓科 Speaker Api Class
    """

    def __init__(
            self,
            base_url: str = "https://speaker.17laimai.cn",
            token: str = "",
            id: str = "",
            version: str = "1"
    ):
        """
        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd
        :param base_url:
        :param token:
        :param id:
        :param version:
        """
        self._base_url = base_url
        self._token = token
        self._id = id
        self._version = version

    @property
    def base_url(self):
        """
        base url
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    def notify(
            self,
            message: str = "",
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd#yG8IS
        :param message:
        :param request_func_kwargs:
        :param request_func_response_callable:
        :return:
        """
        validate(instance=message, schema={"type": "string", "minLength": 1})
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/notify.php")
        request_func_kwargs.setdefault("method", "POST")
        request_func_kwargs.setdefault("data", {})
        request_func_kwargs.data.setdefault("token", self.token)
        request_func_kwargs.data.setdefault("id", self.id)
        request_func_kwargs.data.setdefault("version", self.version)
        request_func_kwargs.data.setdefault("message", message.encode("utf-8"))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "errcode": {
                                "oneOf": [
                                    {"type": "integer", "const": 0},
                                    {"type": "string", "const": "0"},
                                ],
                            },
                            "errmsg": {
                                {"type": "string", "enums": ["ok", "OK", "Ok", "oK"]},
                            },
                        },
                    }
            ).is_valid(response.json()):
                return True
        return False
