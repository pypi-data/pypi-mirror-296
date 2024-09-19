#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-04-26 14:00:51.591452"
__version__ = 1.0
# **************************************************
class VerbosityManager():
    def __init__(self, verbosity_level:int=3):
        self._verbosity = verbosity_level
        return

    @property
    def verbosity(self):
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value:int):
        self._verbosity = value


class Flags():
    OK = 0
    NO_RES = -1
    NO_REF = -2
    NO_READABLE_REF = -3
    NO_READABLE_RES = -4
    DOWNGRADED = -5
    FIXED = -6
    OK_WARNING = -7
    UNDEFINED = -8
    IGNORE = -999
    CONSTRUCTION = 999

    @classmethod
    def get_flags_dict(cls):
        to_ret = {}
        for att in list(cls.__dict__.keys()):
            if att.isupper():
                to_ret[att] = cls.__getattribute__(cls, att)
        return to_ret

    @classmethod
    def get_flag_name(cls, flag_num:int):
        flags = cls.get_flags_dict()
        keys = list(flags.keys())
        val = list(flags.values())
        inv_dict = dict(zip(val, keys))
        to_ret = inv_dict[flag_num]
        return to_ret

    @classmethod
    def msg(cls, statu):
        assert(statu in list(cls.get_flags_dict().values()))
        if statu is Flags.OK:
            return "Reference and result statuts match"
        if statu is Flags.NO_REF:
            return "Reference statut is missing"
        if statu is Flags.NO_RES:
            return "Result statut is missing"
        if statu is Flags.NO_READABLE_REF:
            return "Reference statut format is not as expected (int)"
        if statu is Flags.NO_READABLE_RES:
            return "Reference result format is not as expected (int)"
        if statu is Flags.DOWNGRADED:
            return "\033[38;5;202m↓\033[0m Last job produce an unexpected results :-("
        if statu is Flags.FIXED:
            return "\033[38;5;040m↑\033[0m Reference state should be updated ;-)."
        if statu is Flags.OK_WARNING:
            return "Status are the same but its value is not nominal"
        if statu is Flags.UNDEFINED:
            return "Reference statut and results status differs and none of them are nominal"
        if statu is Flags.IGNORE:
            return "Ignore test"
        if statu is Flags.CONSTRUCTION:
            return "Test in construction"
        return ""  #pragma: no cover

    def __init__(self, *args, **kwd):
        self.res_val = 0
        self.ref_val = 0
        self.stderr = ""
        self.msg = ""


class StatuConfig:
    STORAGE_DIR = ".test_results"
    EXT_REF = ".state"
    EXT_RES = ".res"


class ColorConfig:
    FLAG = "\033[38;5;03m"
    END = "\033[0m"
    KO = "\033[38;5;202m"
    OK = "\033[38;5;040m"
    SUMMARY = "\033[38;5;04m"
    BUILD = "\033[38;5;04m"
