from mitmproxy import http
import time
import re
import logging
import os

path = './pipe'

def request(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    
def response(flow: http.HTTPFlow) -> None:
    try:
        if ('html' in flow.response.headers.get('content-type')):
            html = str(flow.response.content)
            url = flow.request.pretty_url
            pw = open(path, 'w')
            print(html)
            print(url)
            pw.write(url + ' '  + html)
            pw.close()
    except Exception as e:
        print(str(e))
