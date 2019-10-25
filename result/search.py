#!/usr/bin/env python3

import sys
import json
import requests as rq

def search(reg):
    try:
        api = "http://nuresult.megaminds.co/api/search?q=" + str(reg)
        resp = rq.get(api)
        data = json.loads(resp.text)
        name = data['results'][0]['name']
        regn = data['results'][0]['registration_number']
        college = data['results'][0]['college']
        print(name, regn, college)
        return name, regn, college
    except IndexError:
        print("Reg not Found!")
        pass
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit()
