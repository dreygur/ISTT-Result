from flask import Flask, request
from main import welcome, get_result, data, getData
from pprint import pprint
import sys, os, json, requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def admin():
    data = request.args.to_dict()
    log(data)
    c = request.args.get('c')
    if c == '1':
        first_name = request.args.get('first name')
        last_name = request.args.get('last name')
        name = first_name + ' ' + last_name if first_name != last_name else last_name
        return json.dumps({'messages': welcome(name)})
    elif c == '2':
        regNum = request.args.get('regNum')
        semester = request.args.get('semester')
        return json.dumps({'messages': get_result(regNum, semester)})


@app.route('/api', methods=['GET'])
def api():
    receivedData = request.args.to_dict()
    log(receivedData)
    regNum,semester=receivedData['regNum'], receivedData['semester']
    d=str(regNum)[:2]+'_'+str(semester.lower())
    if d in data.keys():
        r=getData(regNum, data[d][0], data[d][1])
    else:
        r=requests.get('http://iku.pythonanywhere.com/result/api/{}/{}'.format(semester, regNum)).json()
    log(r)
    return json.dumps(r)


def log(data):
    pprint(data)
    sys.stdout.flush()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    # app.run(debug=True)
