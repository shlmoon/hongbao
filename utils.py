#!/usr/bin/env python
# encoding: utf-8

from pytz import timezone
from datetime import datetime, date, timedelta
import time
import random
import string
import hashlib
from Crypto.Cipher import AES

import json

from weixinExceptions import userException

class subMessages(object):
    def __init__(self, open_id):
        if not open_id:
            raise userException
        if len(open_id) <  16:
            raise userException
        keys = open_id[:16]
        mode = AES.MODE_CBC
        iv = '1234567812345678'
        self.obj_message = AES.new(keys, mode, iv)

    def get_encrypt_message(self, data):
        return json.dumps(self.obj_message.encrypt(data))

    def get_decrypt_message(self, data):
        return json.loads(self.obj_message.decrypt(data))

def get_datetime_now():
    return datetime.now().replace(tzinfo=timezone('Asia/Shanghai'))

def get_access_token_expire(expire_in):
    now = get_datetime_now()
    return now + timedelta(seconds=expire_in)

def get_today():
    return date.today()

def get_tomorrow():
    return date.today() + timedelta(days=1)

def date_to_datetime(nows):
    ret_date_time = datetime.strptime(str(nows), '%Y-%m-%d')
    return ret_date_time.replace(tzinfo=timezone('Asia/Shanghai'))

def create_nonce_str():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

def create_sign_nonce_str():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))


def create_timestamp():
    return int(time.time())

def get_signature(msg):
    return hashlib.sha1(msg).hexdigest()

def get_len_data_str():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(24))

def trans_django_datetime(nows):
    return nows.replace(tzinfo=timezone('Asia/Shanghai'))

def get_now_str():
    return datetime.strftime(get_datetime_now(), '%Y%m%d')

def get_check_userInfo_datetime(altimedelta):
    # return trans_django_datetime(get_datetime_now()) - timedelta(seconds=altimedelta)
    return trans_django_datetime(get_datetime_now()) - timedelta(seconds=altimedelta)

def get_md_data(msg):
    md = hashlib.md5()
    md.update(msg)
    return md.hexdigest()

def sub_json(msg):
    return json.loads(msg)
