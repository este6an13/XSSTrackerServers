#import requests
#from bs4 import BeautifulSoup
# import re
from urllib.parse import urlparse
import esprima


class Parser():

    keywords = ['XSS', 'banking', 'redirect', 'root', 'password', 'crypt', 
                'shell', 'spray', 'evil']

    def url_len(self, url):
        return len(url)

    def html_len(self, html):
        return len(html)

    def url_spec_char(self, url):
        return 1 if any(c in '[@_!#$%^*()<>\|}{~]' for c in url) else 0

    def url_tag(self, url, tag):
        tags = ['<'+tag+'>', '</'+tag+'>', '%3C'+tag+'%3E', '%3C%2F'+tag+'%3E']
        return 1 if any(t in url for t in tags) else 0

    def url_substr(self, url, substr):
        return 1 if substr in url else 0

    def url_params_count(self, url):
        u = urlparse(url)
        query = u.query
        return 0 if query == '' else len(query.split('&'))

    def url_domain_count(self, url):
        # return len(re.search(r'^[^:]+://([^/]+)', url).group(1).split('.'))
        u = urlparse(url)
        return len(u.hostname.split('.'))

    def html_tag_count(self, soup, tag):
        return len(soup.find_all(tag))

    def html_attr_count(self, soup, attr):
        tags = soup.find_all()
        return [t.has_attr(attr) for t in tags].count(True)

    def html_event_count(self, soup, event):
        tags = soup.find_all()
        return [t.has_attr(event) for t in tags].count(True)

    def html_keywords(self, html):
        count = 0
        for k in self.keywords:
            count += html.count(k)
        return count

    def js_file(self, soup):
        scripts = soup.find_all('script')
        for s in scripts:
            try:
                if s['src'].split('.')[-1] == 'js':
                    return 1
            except:
                pass
        return 0

    def pseudo_protocol(self, soup):
        anchors = soup.find_all('a')
        for a in anchors:
            try:
                if a['href'].split(':')[0] == 'javascript':
                    return 1
            except:
                pass
        return 0

    def js_prop_count(self, soup, prop):
        count = 0
        scripts = soup.find_all('script')
        for s in scripts:
            try:
                tokens = esprima.tokenize(str(s.string))
                for t in tokens:
                    idx = tokens.index(t)
                    if t.value == prop:
                        count += 1
            except:
                pass
        return count

    def js_document_obj_count(self, soup):
        count = 0
        scripts = soup.find_all('script')
        for s in scripts:
            try:
                tokens = esprima.tokenize(str(s.string))
                for t in tokens:
                    idx = tokens.index(t)
                    if t.value == 'document':
                        count += 1
            except:
                pass
        return count

    def js_method_count(self, soup, method):
        count = 0
        scripts = soup.find_all('script')
        for s in scripts:
            try:
                tokens = esprima.tokenize(str(s.string))
                for t in tokens:
                    idx = tokens.index(t)
                    if t.value == method:
                        count += 1
            except:
                pass
        return count

    def js_min_len(self, soup):
        min = float('inf')
        scripts = soup.find_all('script')
        for s in scripts:
            length = len(str(s.string))
            if length < min:
                min = length
        return 0 if min == float('inf') else min

    def js_max_len(self, soup):
        max = 0
        scripts = soup.find_all('script')
        for s in scripts:
            length = len(str(s.string))
            if length > max:
                max = length
        return max

    def js_min_function_call(self, soup):
        min = float('inf')
        scripts = soup.find_all('script')
        for s in scripts:
            tree = {}
            try:
                tree = esprima.parseScript(str(s.string))
            except:
                pass
            treestr = str(esprima.toDict(tree))
            count = treestr.count('CallExpression')
            if count < min:
                min = count
        return 0 if min == float('inf') else min

    def js_min_function_def(self, soup):
        min = float('inf')
        scripts = soup.find_all('script')
        for s in scripts:
            tree = {}
            try:
                tree = esprima.parseScript(str(s.string))
            except:
                pass
            treestr = str(esprima.toDict(tree))
            count = treestr.count('FunctionDeclaration')
            if count < min:
                min = count
        return 0 if min == float('inf') else min
