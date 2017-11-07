# encoding: utf-8

from datetime import datetime
from lxml import etree
from StringIO import StringIO

import hashlib
import requests
import time
import random
import string
import threading


class Singleton(object):
    """可配置单例模式"""

    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    impl = cls.configure() if hasattr(cls, "configure") else cls
                    instance = super(Singleton, cls).__new__(impl, *args, **kwargs)
                    if not isinstance(instance, cls):
                        instance.__init__(*args, **kwargs)
                    cls._instance = instance
        return cls._instance


class HongbaoException(Exception):
    def __init__(self, code=None, msg=None):
        self._code = code if code else 0
        self._msg = msg if msg else ''

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code


class WeChatConfig(object):
    APP_ID = ''
    APP_SECRET = ''
    MCH_ID = ''
    WXAPP_ID = ''
    KEY = ''


def generator_now_string():
    # todo if django: timezone.now()
    return datetime.strftime(datetime.now(), '%Y%m%d')

def generator_timestamp():
    return int(time.time())

def generator_md5_msg(msg=None):
    return hashlib.md5(msg).hexdigest()

def generator_sha_msg(msg=None):
    return hashlib.sha1(msg).hexdigest()

def generator_nonce_str(len=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(len))


class WeChatHongbao(Singleton, WeChatConfig):
    SSLCERT_PATH = ''
    SSLKEY_PATH = ''
    uri = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'
    PARAM_DICT = {
        'act_name': 'shlmoon_test',
        'client_ip': '127.0.0.1',
        'mch_billno': '',
        'mch_id': '123456456',
        'nonce_str': '',
        're_openid': '',
        'remark': 'thank you',
        'send_name': 'shlmoon_account',
        'total_amount': 0,
        'total_num': 1,
        'wishing': 'wishing',
        'wxappid': 'shlmoon_appid',
        'sign': ''
    }

    def __init__(self, *args, **kwargs):
        super(WeChatHongbao, self).__init__(*args, **kwargs)

    def post_xml(self, url, data):
        try:
            with requests.Session() as s:
                headers = {'Content-Type': 'application/xml'}
                req = requests.Request('POST', url, data=data, headers=headers)
                prepped = s.prepare_request(req)
                resp = s.send(prepped, verify=True, cert=(self.SSLCERT_PATH, self.SSLKEY_PATH))
                return resp.text
        except (TypeError, ValueError), e:
            # todo: error logger
            raise HongbaoException(code=0, msg=str(e))

    def get_sign(self, paraMap=None):
        def _formatData(paraMap=None):
            return ['%s=%s' % (k, paraMap[k]) for k in sorted(paraMap) if not k == 'sign']
        sign_valus = _formatData(paraMap=paraMap)
        sign_valus = '%s&key=%s' % (sign_valus, self.KEY)
        return generator_md5_msg(msg=sign_valus).upper()

    def set_param(self, **kwargs):
        self.PARAM_DICT['act_name'] = kwargs.get('act_name') or self.PARAM_DICT['act_name']
        self.PARAM_DICT['total_amount'] = kwargs.get('total_amount') or self.PARAM_DICT['total_amount']
        self.PARAM_DICT['re_openid'] = kwargs.get('re_openid')
        self.PARAM_DICT['nonce_str'] = generator_nonce_str(len=15)
        self.PARAM_DICT['wxappid'] = self.APP_ID
        self.PARAM_DICT['mch_billno'] = '{mch}{ns}{st}'.format(
            mch=self.PARAM_DICT['mch_id'],
            ns=generator_now_string(),
            st=generator_timestamp()
        )
        self.PARAM_DICT['sign'] = self.get_sign(paraMap=self.PARAM_DICT)

    def generator_hongbao_xml(self):
        content = etree.Element('xml')
        for parm_xml in self.PARAM_DICT.keys():
            etree.SubElement(content, parm_xml)
            setattr(parm_xml, 'text', self.PARAM_DICT[parm_xml])
        return etree.tostring(content, xml_declaration=True, encoding='utf-8')

    def send_hongbao(self):
        try:
            data = self.generator_hongbao_xml()
            valus = self.post_xml(self.uri, data)
            # todo: info logger. data-valus
            root = etree.parse(StringIO(valus.decode('utf-8')))
            tree = root.getroot()
            ret = tree.xpath(r'result_code')[0].text
            if ret == u'FAIL':
                return False
            return True
        except Exception, e:
            # todo: error logger
            raise HongbaoException(code=0, msg=str(e))
