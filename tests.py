#!/usr/bin/env python
# encoding: utf-8

import unittest
from hongbao import hongbao

class hongbaoTest(unittest.TestCase):
    def setUp(self):
        self.hb = hongbao()

    def tearDown(self):
        self.hb = hongbao()

    def test_hongbao_valid(self):
        self.assertTrue(
            self.hb.send_hongbao(
                act_name=u'感恩回馈',
                re_openid='onEn6siHKrAmcMTmsCiDbtqPTvEk',
                remark='good luck',
                send_name=u'小乌牛',
                total_amount=100,
                wishing='best wishing'
            )
        )

    def test_hongbao_invalid(self):
        self.hb.set_hongbao_parm(1, 'onEn6siHKrAmcMTmsCiDbtq')
        self.assertFalse(
            self.hb.send_hongbao(
                act_name=u'感恩回馈',
                re_openid='onEn6siHKrAmcMTmsCiDbtqPTvEdd',
                remark='good luck',
                send_name=u'小乌牛',
                total_amount=100,
                wishing='best wishing'
            )
        )
