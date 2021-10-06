from flask import Flask, request, Response
from urllib.parse import urlparse
import requests
import sys

app = Flask('main', static_folder=None)
WEBSITE = 'example.com'


@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
def malproxy(path):
    # TODO
    global WEBSITE
    parsed = urlparse(WEBSITE)
    if(not parsed.scheme):
        WEBSITE = f'https://{WEBSITE}'
    print(WEBSITE)
    print(path)
    try:
        r = requests.request(request.method, f'{WEBSITE}{path}')
        return r.content
    except Exception:
        pass

@app.route('/<path:path>', methods=['POST', 'GET'])
def proxycont(path):
    print(request.headers)
    myheader = request.headers
    myheader["Referer"] = f'{WEBSITE}'
    print(myheader)
    try:
        return requests.request(request.method, f'{WEBSITE}{path}', dict(request.headers), request.form).content
    except Exception:
        pass

    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERROR: Website not provided.')
        exit(1)

    WEBSITE = sys.argv[1]
    app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')


