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
        self.hb.set_hongbao_parm(100, 'onEn6siHKrAmcMTmsCiDbtqPTvEk')
        self.assertTrue(self.hb.get_hongbao_resp())

    def test_hongbao_invalid(self):
        self.hb.set_hongbao_parm(1, 'onEn6siHKrAmcMTmsCiDbtq')
        self.assertFalse(self.hb.get_hongbao_resp())
