# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import requests

ENV = "dev"
URL = "http://configserver-{env}.chj.cloud/configs/{appName}/default/application"
ALL_APOLLO_COFNIG = dict()

def get_apollo_config(k, appName):
    return ALL_APOLLO_COFNIG(k, "")


def get_apollo_all_config(appName):
    env = os.getenv("RUNTIME_ENV") or ENV
    data = requests.get(URL.format(env=env, appName=appName))

    if data.status_code == 200:
        ALL_APOLLO_COFNIG = data.json()["configurations"]
        return ALL_APOLLO_COFNIG
    else:
        return dict()
