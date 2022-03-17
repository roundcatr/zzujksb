#!/usr/bin/env python3
# coding=utf-8

import requests
from urllib import parse

def push(title, body, device_key, level, group):
    requests.get("https://api.day.app/"+device_key+"/"+parse.quote(title)+"/"+parse.quote(body), params={'level': parse.quote(level), 'group': parse.quote(group)})
