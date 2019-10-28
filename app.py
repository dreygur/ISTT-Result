import os
import sys
import json
import requests
from flask import Flask
from flask import request
from flask import jsonify

# My custom functions
from result.search import search
from result.intro import welcome
from result.result import result
from birthday import wish

app = Flask("ISTT NU Result")

@app.route('/')
def main():
    return "Hola amigo!!!"


@app.route('/result/', methods=["GET"])
def reslt():
    try:
        year = request.args.get('year')
        regn = request.args.get('reg')
        res = result(regn)
        print(year, regn)
        # return json.dumps({"messages": res})
        return jsonify({"messages": res})
    except:
        return 'An Internal Error Occured!'

@app.route('/api/<regn>')
def api(regn):
    res = search(regn)
    return json.dumps(res)

try:
    @app.route('/bday/')
    def bday():
        return wish()
except Exception:
    pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(port=port)
