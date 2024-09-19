# !/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2017-07-19 17:22:57.246629"
__version__ = 1.0
# **************************************************
from nonRegressionTestTools import constantes as CST
import pytest

def test_verbosity():
    verb = CST.VerbosityManager()
    assert("verbosity" in list(verb.__class__.__dict__.keys()))
    assert(type(verb.verbosity) == int)
    assert(verb.verbosity == 3)
    verb.verbosity = 4
    assert(verb.verbosity == 4)


def test_flags():
    FLAGS = {"OK": 0,
             "NO_RES": -1,
             "NO_REF": -2,
             "NO_READABLE_REF": -3,
             "NO_READABLE_RES": -4,
             "DOWNGRADED": -5,
             "FIXED": -6,
             "OK_WARNING": -7,
             "UNDEFINED": -8,
             "IGNORE": -999,
             "CONSTRUCTION": 999,
             }
    flags = CST.Flags()
    for att in list(flags.__class__.__dict__.keys()):
        if att[0].isupper():
            assert(att in list(FLAGS.keys()))
            val = flags.__getattribute__(att)
            assert(val == FLAGS[att])
    flags_dict = flags.get_flags_dict()
    for k, val in flags_dict.items():
        assert(k in list(FLAGS.keys()))
        assert(val == FLAGS[k])
    for val in flags_dict.values():
        flag_name = flags.get_flag_name(val)
        assert(val == FLAGS[flag_name])
        msg = CST.Flags.msg(val)
        assert(msg != "")
