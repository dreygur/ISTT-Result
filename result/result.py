#!/usr/bin/env python3

import sys
import json
import requests as rq

def result(reg):
    try:
        header = {
            "Authorization": "5988dfdd7fc53c255a38f2d4786779a1",
            "Host": "nuresult.megaminds.co",
            "User-Agent": "okhttp/3.12.0"
        }
        api = "http://nuresult.megaminds.co/api/results/" + str(reg)
        resp = rq.get(api, headers=header)
        data = json.loads(resp.text)
        name = data['name']
        regn = data['registration_number']
        college = data['college']
        sems = data['semesters']
        # print(name, regn, college)
        # return name, regn, college
        # return data
        return name, regn, college, sems
    except IndexError:
        print("Reg not Found!")
        pass
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit()
