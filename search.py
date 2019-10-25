#!/usr/bin/env python3

import sys
import json
import requests as rq

f = open("reslt.txt", "a")


def result(reg):
    try:
        api = "http://nuresult.megaminds.co/api/search?q=" + str(reg)
        resp = rq.get(api)
        data = json.loads(resp.text)
        name = data['results'][0]['name']
        regn = data['results'][0]['registration_number']
        college = data['results'][0]['college']
        print(name, regn, college)
        f.write(f'{name} - {regn} - {college}\n')
    except IndexError:
        print("Reg not Found!")
        pass
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit()


reg = int(sys.argv[1])
stop = int(sys.argv[2])
# print(reg, stop)
while reg <= stop:
    result(reg)
    reg += 1

f.close()
