#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import hashlib
import random
import string
from datetime import time, datetime
from os import access
from typing import Callable

import requests
from addict import Dict
from jsonschema.validators import validate, Draft202012Validator


class Api(object):
    """
    微网通联短息API Class

    @see https://www.lmobile.cn/ApiPages/index.html
    """

    def __init__(
            self,
            base_url: str = "https://api.51welink.com/",
            account_id: str = "",
            password: str = "",
            product_id: int = 0,
            smms_encrypt_key: str = "SMmsEncryptKey",
    ):
        validate(instance=base_url, schema={"type": "string", "minLength": 1, "format": "uri"})
        validate(instance=account_id, schema={"type": "string", "minLength": 1})
        validate(instance=password, schema={"type": "string", "minLength": 1})
        validate(instance=product_id, schema={"type": "integer", "minimum": 1})
        validate(instance=smms_encrypt_key, schema={"type": "string", "minLength": 1})
        self._base_url = base_url
        self._account_id = account_id
        self._password = password
        self._product_id = product_id
        self._smms_encrypt_key = smms_encrypt_key

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        self._product_id = product_id

    @property
    def smms_encrypt_key(self):
        return self._smms_encrypt_key

    @smms_encrypt_key.setter
    def smms_encrypt_key(self, smms_encrypt_key):
        self._smms_encrypt_key = smms_encrypt_key

    def timestamp(self):
        return int(datetime.now().timestamp())

    def random_digits(self, length=10):
        return int("".join(random.sample(string.digits, length)))

    def password_md5(self):
        return hashlib.md5(f"{self.password}{self.smms_encrypt_key}".encode('utf-8')).hexdigest()

    def sha256_signature(self, data: dict = {}):
        data = Dict(data)
        temp = f"AccountId={data.AccountId}&PhoneNos={str(data.PhoneNos).split(",")[0]}&Password={self.password_md5().upper()}&Random={data.Random}&Timestamp={data.Timestamp}"
        return hashlib.sha256(temp.encode("utf-8")).hexdigest()

    def send_sms(
            self,
            phone_nos: str = "",
            content: str = "",
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None

    ) -> bool:
        """
        提交短信

        用于提交发送短信的常规方法

        @see https://www.lmobile.cn/ApiPages/index.html
        :param phone_nos: 接收号码间用英文半角逗号“,”隔开，触发产品一次只能提交一个,其他产品一次不能超过10万个号码
        :param content: 短信内容：不超过1000字符
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response,request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/EncryptionSubmit/SendSms.ashx")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("json", Dict())
        request_func_kwargs.json.setdefault("AccountId", self.account_id)
        request_func_kwargs.json.setdefault("Timestamp", self.timestamp())
        request_func_kwargs.json.setdefault("Random", self.random_digits())
        request_func_kwargs.json.setdefault("ProductId", self.product_id)
        request_func_kwargs.json.setdefault("PhoneNos", phone_nos)
        request_func_kwargs.json.setdefault("Content", content)
        request_func_kwargs.json.setdefault("AccessKey", self.sha256_signature(request_func_kwargs.json))
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "Result": {
                        "type": "string",
                        "minLength": 1,
                        "const": "succ"
                    }
                },
                "required": ["Result"]
            }).is_valid(response.json()):
                return True
        return False
