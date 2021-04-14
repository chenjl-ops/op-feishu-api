# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import requests

ENV = "dev"
URL = "http://configserver-{env}.chj.cloud/configs/{appName}/default/application"


class ApolloConfig(object):

    ALL_APOLLO_COFNIG = dict()

    def __init__(self, appName):
        self.appName = appName
        self._get_apollo_all_config()

    @classmethod
    def get_apollo_config(cls, k):
        return cls.ALL_APOLLO_COFNIG.get(k, "")

    def _get_apollo_all_config(self):
        env = os.getenv("RUNTIME_ENV") or ENV
        data = requests.get(URL.format(env=env, appName=self.appName))

        if data.status_code == 200:
            print("init config")
            ApolloConfig.ALL_APOLLO_COFNIG = data.json()["configurations"]
            return ApolloConfig.ALL_APOLLO_COFNIG
        else:
            return dict()
