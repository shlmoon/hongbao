# encoding: utf-8

import requests

from lxml import etree
from StringIO import StringIO

import hashlib
from datetime import datetime

import time
import random
import string

class BasicConf(object):
    app_id = ''
    app_secret = ''
    mch_id = ''
    wxappid = ''
    key = ''

class hongbaoException(Exception):
    def __init__(self, code, msg):
        self.code = code if code else 0
        self.msg = msg if msg else ''

    @property
    def get_code(self):
        return self.code

    @get_code.setter
    def set_values(self, code):
        self.code = code

class hongbaoUtils(object):
    def get_now_str(self):
        return datetime.strftime(datetime.now(), '%Y%m%d')

    def get_md5_msg(self, msg):
        return hashlib.md5(msg).hexdigest()

    def get_sha_msg(self, msg):
        return hashlib.sha1(msg).hexdigest()

    def create_sign_nonce_str(self, len):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(len))

    def create_timestamp(self):
        return int(time.time())

class hongbao(BasicConf, hongbaoUtils):
    """docstring for hongbao"""
    # act_name = ''
    # remart = ''
    # send_name = ''
    # wishing = ''
    SSLCERT_PATH = ''
    SSLKEY_PATH = ''
    hongbao_dict = {
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
    def __init__(self):
        super(hongbao, self).__init__()
        self.exce = hongbaoException(0, '')

    def post_hongbao(self, url, data):
        try:
            with requests.Session() as s:
                headers = {'Content-Type': 'application/xml'}
                req = requests.Request('POST', url, data=data, headers=headers)
                prepped = s.prepare_request(req)
                resp = s.send(prepped, verify=True, cert=(self.SSLCERT_PATH, self.SSLKEY_PATH))
            return resp.text
        except Exception:
            # self.exce.set_values(codeEnum)
            raise self.exce

    def set_hongbao_parm(self, total_amount, open_id):
        self.hongbao_dict['total_amount'] = total_amount
        self.hongbao_dict['re_openid'] = open_id
        self.hongbao_dict['nonce_str'] = self.create_sign_nonce_str(15)
        self.hongbao_dict['wxappid'] = self.app_id
        self.hongbao_dict['mch_billno'] = '%s%s%s' % (self.hongbao_dict.get('mch_id'), self.get_now_str(), self.create_timestamp())
        self.hongbao_dict['sign'] = self.get_sign(paraMap=self.hongbao_dict)

    def get_sign(self, paraMap=None):
        def _formatData(paraMap=None):
            try:
                del paraMap['sign']
            except KeyError:
                pass
            return ['%s=%s' % (k, paraMap[k]) for k in sorted(paraMap)]
        sign_valus = _formatData(paraMap=paraMap)
        sign_valus = '%s&key=%s' % (sign_valus, self.key)
        return self.get_md5_msg(sign_valus).upper()

    def get_hongbao_xml(self):
        content = etree.Element('xml')
        for parm_xml in self.hongbao_dict.keys():
            etree.SubElement(content, parm_xml)
            setattr(parm_xml, 'text', self.hongbao_dict.get('parm_xml'))
            # parm_xml.text = hongbao_dict.get(parm_xml, None)
        return etree.tostring(content, xml_declaration=True, encoding='utf-8')

    def send_hongbao(self):
        try:
            url = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'
            data = self.get_hongbao_data()
            valus = self.post_hongbao(url, data)
            root = etree.parse(StringIO(valus.decode('utf-8')))
            tree = root.getroot()
            ret = tree.xpath(r'result_code')[0].text
            if ret == u'FAIL':
                return False
            return True
        except:
            return False
