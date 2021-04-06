# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import requests

ENV = "dev"
URL = "http://configserver-{env}.chj.cloud/configs/{appName}/default/application"

env = os.getenv("RUNTIME_ENV") or ENV

def get_apollo_config(k, appName):
    data = requests.get(URL.format(env=env, appName=appName))

    if data.status_code == 200:
        return data.json()["configurations"][k]
    else:
        return ""
