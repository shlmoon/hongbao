#!/usr/bin/env python
# encoding: utf-8

import requests

from lxml import etree
from StringIO import StringIO

from urllib import quote
import hashlib

from config import (
    mch_id,
    wxappid,
    key,
    act_name,
    remark,
    send_name,
    wishing,
)

from utils import (
    get_now_str,
    create_timestamp,
    create_sign_nonce_str,
)

from weixinExceptions import userException

import logging
logging.basicConfig(level=logging.ERROR)

class hongbao(object):
    """docstring for hongbao"""
    def __init__(self):
        super(hongbao, self).__init__()
        self.SSLCERT_PATH = '/home/shlmoon/env/hongbao/ca/apiclient_cert.pem'
        self.SSLKEY_PATH = '/home/shlmoon/env/hongbao/ca/apiclient_key.pem'

    def set_hongbao_parm(self, total_amount, open_id):
        self.total_amount = u'%s' % total_amount
        self.open_id = open_id
        self.nonce_str = create_sign_nonce_str()

    def post_hongbao(self, url, data):
        try:
            with requests.Session() as s:
                headers = {'Content-Type': 'application/xml'}
                req = requests.Request('POST', url, data=data, headers=headers)
                prepped = s.prepare_request(req)
                resp = s.send(prepped, verify=True, cert=(self.SSLCERT_PATH, self.SSLKEY_PATH))

            return resp.text
        except Exception:
            raise userException

    def formatBizQueryParaMap(self, paraMap, flags):
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if flags else paraMap[k]
            buff.append("{0}={1}".format(k, v))
        return "&".join(buff)

    def get_sign_data(self):
        data = {
        'mch_id': mch_id,
        'mch_billno': self.get_mch_billno(),
        'nonce_str': self.nonce_str,
        'client_ip': '127.0.0.1',
        'act_name': act_name,
        're_openid': self.open_id,
        'remark': remark,
        'send_name': send_name,
        'total_amount': self.total_amount,
        'total_num': 1,
        'wishing': wishing,
        'wxappid': wxappid,
        }
        sign_valus = self.formatBizQueryParaMap(data, False)
        sign_valus = "{0}&key={1}".format(sign_valus, key)
        sign_valus = hashlib.md5(sign_valus).hexdigest()
        return sign_valus.upper()

    def get_mch_billno(self):
        return '%s%s%s' % (mch_id, get_now_str(), create_timestamp())

    def get_hongbao_data(self):
        content = etree.Element('xml')
        act_name_xml = etree.SubElement(content, 'act_name')
        act_name_xml.text = act_name
        client_ip_xml = etree.SubElement(content, 'client_ip')
        client_ip_xml.text = u'127.0.0.1'
        mch_billno_xml = etree.SubElement(content, 'mch_billno')
        mch_billno_xml.text = self.get_mch_billno()
        mch_id_xml = etree.SubElement(content, 'mch_id')
        mch_id_xml.text = mch_id
        nonce_str_xml = etree.SubElement(content, 'nonce_str')
        nonce_str_xml.text = self.nonce_str
        re_openid_xml = etree.SubElement(content, 're_openid')
        re_openid_xml.text = self.open_id
        remark_xml = etree.SubElement(content, 'remark')
        remark_xml.text = remark
        send_name_xml = etree.SubElement(content, 'send_name')
        send_name_xml.text = send_name
        total_amount_xml = etree.SubElement(content, 'total_amount')
        total_amount_xml.text = self.total_amount
        total_num_xml = etree.SubElement(content, 'total_num')
        total_num_xml.text = u'1'
        wishing_xml = etree.SubElement(content, 'wishing')
        wishing_xml.text = wishing
        wxappid_xml = etree.SubElement(content, 'wxappid')
        wxappid_xml.text = wxappid
        sign_xml = etree.SubElement(content, 'sign')
        sign_xml.text = self.get_sign_data()
        return etree.tostring(content, xml_declaration=True, encoding='utf-8')


    #xml解析
    def get_hongbao_resp(self):
        try:
            url = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'
            data = self.get_hongbao_data()
            valus = self.post_hongbao(url, data)
            print valus
            root = etree.parse(StringIO(valus.decode('utf-8')))
            tree = root.getroot()
            ret = tree.xpath(r'result_code')[0].text
            if ret == u'FAIL':
                return False
            return True
        except userException, e:
            logging.error('get_hongbao_error: {}'.format(e))
            return False

