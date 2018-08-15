# -*- coding: UTF-8 -*-
import hashlib

try:
    from urllib.parse import quote, urlencode
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:
    from urllib import quote, urlencode
    from urllib2 import Request, urlopen, URLError
import six
import base64
import json
import time

if six.PY3:
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context


class AiPlat(object):
    def __init__(self, app_id, app_key):
        self.url_preffix = 'https://api.ai.qq.com/fcgi-bin/'
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}
        self.url = ''
        self.set_basics_data()

    def set_basics_data(self):
        basics_data = {'app_id': self.app_id, 'app_key': self.app_key,
                       'time_stamp': int(time.time()), 'nonce_str': int(time.time())
                       }
        self.data.update(basics_data)

    def invoke(self, params):
        url_data = urlencode(params)
        if six.PY3:
            url_data = url_data.encode('utf-8')
        req = Request(self.url, url_data)
        try:
            rsp = urlopen(req)
            str_rsp = rsp.read()
            dict_rsp = json.loads(str_rsp)
            return dict_rsp
        except URLError as e:
            dict_error = {}
            if hasattr(e, "code"):
                dict_error['ret'] = -1
                dict_error['httpcode'] = e.code
                dict_error['msg'] = "sdk http post err"
                return dict_error
            if hasattr(e, "reason"):
                dict_error['msg'] = 'sdk http post err'
                dict_error['httpcode'] = -1
                dict_error['ret'] = -1
                return dict_error

    def get_ocr_generalocr(self, image):
        self.url = self.url_preffix + 'ocr/ocr_generalocr'
        image_data = base64.b64encode(image)
        if six.PY3:
            image_data = image_data.decode('utf-8')
        self.data['image'] = image_data
        sign_str = self.gen_sign_string(self.data)
        self.data['sign'] = sign_str
        return self.invoke(self.data)

    def get_nlp_text_trans(self, text, type):
        self.url = self.url_preffix + 'nlp/nlp_texttrans'
        self.data['text'] = text
        self.data['type'] = type
        sign_str = self.gen_sign_string(self.data)
        self.data['sign'] = sign_str
        return self.invoke(self.data)

    def get_aai_wx_asrs(self, chunk, speech_id, end_flag, format_id, rate, bits, seq, chunk_len, cont_res):
        self.url = self.url_preffix + 'aai/aai_wxasrs'
        speech_chunk = base64.b64encode(chunk)
        if six.PY3:
            speech_chunk = speech_chunk.decode('utf-8')
        plus_data = {
            'speech_chunk': speech_chunk,
            'speech_id': speech_id,
            'end': end_flag,
            'format': format_id,
            'rate': rate,
            'bits': bits,
            'seq': seq,
            'len': chunk_len,
            'cont_res': cont_res,
        }
        self.data.update(plus_data)
        sign_str = self.gen_sign_string(self.data)
        self.data['sign'] = sign_str
        return self.invoke(self.data)

    @staticmethod
    def gen_sign_string(parser):
        uri_str = ''
        for key in sorted(parser.keys()):
            if key == 'app_key':
                continue
            uri_str += "%s=%s&" % (key, quote(str(parser[key]), safe=''))
        sign_str = uri_str + 'app_key=' + parser['app_key']

        if six.PY3:
            sign_str = sign_str.encode('utf-8')
        hash_md5 = hashlib.md5(sign_str)
        return hash_md5.hexdigest().upper()
