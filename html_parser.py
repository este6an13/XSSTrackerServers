from bs4 import BeautifulSoup
import requests
import json
import simplejson
import os
from Parser import Parser

perm = 0o666
path = './pipe'
os.unlink(path)
parser = Parser()
os.mkfifo(path, perm) 
  
while True:
    pr = open(path, 'r')
    r = pr.read()
    url = r.split()[0]
    html = r[len(url)+1:]
    pr.close()
    soup = BeautifulSoup(html, 'html.parser')
   
    data = {
        'url' : url,
        'url_length' : parser.url_len(url),
        'url_spec_char' : parser.url_spec_char(url),
        'url_tag_script' : parser.url_tag(url, 'script'),
        'url_tag_iframe' : parser.url_tag(url, 'iframe'),
        'url_attr_src' : parser.url_substr(url, 'src'),
        'url_ev_onload' : parser.url_substr(url, 'onload'),
        'url_ev_onmouseover' : parser.url_substr(url, 'onmouseover'),
        'url_cookie' : parser.url_substr(url, 'cookie'),
        'url_params_count' : parser.url_params_count(url),
        'url_domains_count' : parser.url_domain_count(url),
        'html_tag_script' : parser.html_tag_count(soup, 'script'),
        'html_tag_iframe' : parser.html_tag_count(soup, 'iframe'),
        'html_tag_meta' : parser.html_tag_count(soup, 'meta'),
        'html_tag_object' : parser.html_tag_count(soup, 'object'),
        'html_tag_embed' : parser.html_tag_count(soup, 'embed'),
        'html_tag_link' : parser.html_tag_count(soup, 'link'),
        'html_tag_svg' : parser.html_tag_count(soup, 'svg'),
        'html_tag_frame' : parser.html_tag_count(soup, 'frame'),
        'html_tag_form' : parser.html_tag_count(soup, 'form'),
        'html_tag_div' : parser.html_tag_count(soup, 'div'),
        'html_tag_style' : parser.html_tag_count(soup, 'style'),
        'html_tag_img' : parser.html_tag_count(soup, 'img'),
        'html_tag_input' : parser.html_tag_count(soup, 'input'),
        'html_tag_textarea' : parser.html_tag_count(soup, 'textarea'),
        'html_attr_action' : parser.html_attr_count(soup, 'action'),
        'html_attr_background' : parser.html_attr_count(soup, 'background'),
        'html_attr_classid' : parser.html_attr_count(soup, 'classid'),
        'html_attr_codebase' : parser.html_attr_count(soup, 'codebase'),
        'html_attr_href' : parser.html_attr_count(soup, 'href'),
        'html_attr_longdesc' : parser.html_attr_count(soup, 'longdesc'),
        'html_attr_profile' : parser.html_attr_count(soup, 'profile'),
        'html_attr_src' : parser.html_attr_count(soup, 'src'),
        'html_attr_usemap' : parser.html_attr_count(soup, 'usemap'),
        'html_attr_http-equiv' : parser.html_attr_count(soup, 'http-equiv'),
        'html_ev_onblur' : parser.html_event_count(soup, 'onblur'),
        'html_ev_onchange' : parser.html_event_count(soup, 'onchange'),
        'html_ev_onclick' : parser.html_event_count(soup, 'onclick'),
        'html_ev_onerror' : parser.html_event_count(soup, 'onerror'),
        'html_ev_onfocus' : parser.html_event_count(soup, 'onfocus'),
        'html_ev_onkeydown' : parser.html_event_count(soup, 'onkeydown'),
        'html_ev_onkeypress' : parser.html_event_count(soup, 'onkeypress'),
        'html_ev_onkeyup' : parser.html_event_count(soup, 'onkeyup'),
        'html_ev_onload' : parser.html_event_count(soup, 'onload'),
        'html_ev_onmousedown' : parser.html_event_count(soup, 'onmousedown'),
        'html_ev_onmouseout' : parser.html_event_count(soup, 'onmouseout'),
        'html_ev_onmouseover' : parser.html_event_count(soup, 'onmouseover'),
        'html_ev_onmouseup' : parser.html_event_count(soup, 'onmouseup'),
        'html_ev_onsubmit' : parser.html_event_count(soup, 'onsubmit'),
        'html_keywords_evil' : parser.html_keywords(html),
        'js_file' : parser.js_file(soup),
        'js_pseudo_protocol' : parser.pseudo_protocol(soup),
        'js_prop_location' : parser.js_prop_count(soup, 'location'),
        'js_dom_document' : parser.js_document_obj_count(soup),
        'js_prop_cookie' : parser.js_prop_count(soup, 'cookie'),
        'js_prop_referrer' : parser.js_prop_count(soup, 'referrer'),
        'js_method_write' : parser.js_method_count(soup, 'write'),
        'js_method_geteltag' : parser.js_method_count(soup, 'getElementsByTagName'),
        'js_method_getelid' : parser.js_method_count(soup, 'getElementById'),
        'js_method_alert' : parser.js_method_count(soup, 'alert'),
        'js_method_eval' : parser.js_method_count(soup, 'eval'),
        'js_method_fromcharcode' : parser.js_method_count(soup, 'fromCharCode'),
        'js_method_confirm' : parser.js_method_count(soup, 'confirm'),
        'js_min_len' : parser.js_min_len(soup),
        'js_min_func_def' : parser.js_min_function_def(soup),
        'js_min_func_call' : parser.js_min_function_call(soup),
        'js_max_len' : parser.js_max_len(soup),
        'html_len' : parser.html_len(html)
        }
    r = requests.post("http://localhost:5000/", json=data)
