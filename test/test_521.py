# builder:wstki
# 开发时间17:42,2024/2/2
# name:test_521
import requests
import re
from js2py import evaljs

def get_521_content():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    req = requests.get('https://www.seebug.org/vuldb/ssvid-92666', headers=headers)
    cookies = '; '.join(['='.join(item) for item in req.cookies.items()])
    txt_521 = ''.join(re.findall('<script>(.*?)</script>', req.text))
    return txt_521, cookies

def fixed_fun(function):
    func_return = function.replace('eval', 'return')
    evaled_func = evaljs(func_return)
    mode_func = evaled_func.f().replace('while(window._phantom||window.__phantomas){};', '') \
        .replace('document.cookie=', 'return').replace(';if((function(){try{return !!window.addEventListener;}', '') \
        .replace("catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',l,false);}", '') \
        .replace("else{document.attachEvent('onreadystatechange',l);}", '') \
        .replace(r"setTimeout('location.href=location.href.replace(/[\?|&]captcha-challenge/,\'\')',1500);", '')
    cookies = evaljs(mode_func).l()
    __jsl_clearance = cookies.split(';')[0]
    return __jsl_clearance

def cookie_dict(js, id):
    dict_ = {}
    js = js.split('=')
    id = id.split('=')
    dict_[js[0]] = js[1]
    dict_[id[0]] = id[1]
    return dict_

if __name__ == '__main__':
    func = get_521_content()
    content = func[0]
    cookie_id = func[1]
    cookie_js = fixed_fun(func[0])
    dicted_cookie = cookie_dict(cookie_js, cookie_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
        'Cookie': cookie_id + ';' + cookie_js
    }
    req = requests.get('https://www.seebug.org/vuldb/ssvid-92666', headers=headers)
    print(req.status_code)
    print(len(req.text))
