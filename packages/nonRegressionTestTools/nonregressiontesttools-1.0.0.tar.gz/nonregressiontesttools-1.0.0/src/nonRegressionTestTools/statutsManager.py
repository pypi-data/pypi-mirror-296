#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-04-26 14:16:13.359025"
__version__ = 1.0
# **************************************************
from . import constantes as CST
import os


class StatutManager(CST.VerbosityManager):
    """
    manage the statut of a test

    """

    def __init__(self, abs_dir, rel_dir, baseName, **kwd):
        super().__init__(**kwd)
        self._abs_dir = abs_dir
        self._rel_dir = rel_dir
        self._baseName = baseName
        self._ref_statut_file = None
        self._rel_ref_statut_file = None
        self._ref_statut = None
        self._last_run_statut_file = None
        self._rel_last_run_statut_file = None
        self._last_run_statut = None
        self._set_ref_statut_file()
        self._set_last_run_statut_file()
        self._get_ref_statut(True)
        self._get_last_run_statut(True)
        return

    def _set_ref_statut_file(self):
        fn = self._baseName+CST.StatuConfig.EXT_REF
        self._ref_statut_file = os.path.join(self._abs_dir,
                                             CST.StatuConfig.STORAGE_DIR,
                                             fn)
        if self._rel_dir:
            self._rel_ref_statut_file = os.path.join(self._rel_dir,
                                                     CST.StatuConfig.STORAGE_DIR,
                                                     fn)
        return

    def _set_last_run_statut_file(self):
        fn = self._baseName+CST.StatuConfig.EXT_RES
        self._last_run_statut_file = os.path.join(self._abs_dir,
                                                  CST.StatuConfig.STORAGE_DIR,
                                                  fn)
        if self._rel_dir:
            self._rel_last_run_statut_file = os.path.join(self._rel_dir,
                                                          CST.StatuConfig.STORAGE_DIR,
                                                          fn)
        return

    def _update_ref_statut(self):
        if not os.path.isfile(self._ref_statut_file):
               self._ref_statut = CST.Flags.NO_REF
        else:
            try:
                with open(self._ref_statut_file, 'r') as f1:
                    self._ref_statut = int(f1.readline())
            except:
                self._ref_statut = CST.Flags.NO_READABLE_REF
        return

    def _update_last_run_statut(self):
        if not os.path.isfile(self._last_run_statut_file):
            self._last_run_statut = CST.Flags.NO_RES
        else:
            try:
                with open(self._last_run_statut_file, 'r') as f1:
                    self._last_run_statut = int(f1.readline())
            except:
                self._last_run_statut = CST.Flags.NO_READABLE_RES
        return

    def get_flags(self):
        self._update()
        to_return = []
        if (self._last_run_statut == self._ref_statut) and (self._last_run_statut == 0):
            to_return.append(CST.Flags.OK)
        else:
            if self._ref_statut == CST.Flags.NO_REF:
                to_return.append(CST.Flags.NO_REF)
            if self._last_run_statut == CST.Flags.NO_RES:
                to_return.append(CST.Flags.NO_RES)
            if self._ref_statut == CST.Flags.NO_READABLE_REF:
                to_return.append(CST.Flags.NO_READABLE_REF)
            if self._last_run_statut == CST.Flags.NO_READABLE_RES:
                to_return.append(CST.Flags.NO_READABLE_RES)
            if self._last_run_statut == CST.Flags.CONSTRUCTION:
                to_return.append(CST.Flags.CONSTRUCTION)

            if self._ref_statut > 0 or self._last_run_statut > 0:
                CST.Flags.ref_val = self._ref_statut
                CST.Flags.res_val = self._last_run_statut
                if self._ref_statut == 0 and self._last_run_statut > 0:
                    to_return.append(CST.Flags.DOWNGRADED)
                elif self._ref_statut > 0 and self._last_run_statut == 0:
                    to_return.append(CST.Flags.FIXED)
                elif self._ref_statut == self._last_run_statut:
                    to_return.append(CST.Flags.OK_WARNING)
                else:
                    to_return.append(CST.Flags.UNDEFINED)
        return to_return

    @property
    def verbose_flags(self):
        self._update()
        pre = "\t-->  "
        flags = self.get_flags()
        flags_to_print = "\n\t|"
        to_add = " "
        for flag in flags:
            flags_to_print += CST.ColorConfig.FLAG+ CST.Flags.get_flag_name(flag) + CST.ColorConfig.END +"|"
            to_add += "\n\t -> "+str(CST.Flags.msg(flag))
            # to_add += "\n\t-- ref value: "+str(CST.Flags.ref_val)
            # to_add += "\n\t-- res value: "+str(CST.Flags.res_val)
            if (flag is CST.Flags.DOWNGRADED)\
               or (flag is CST.Flags.FIXED)\
               or (flag is CST.Flags.OK_WARNING)\
               or (flag is CST.Flags.UNDEFINED):
                to_add += "\n\t-- ref value: "+str(CST.Flags.ref_val)
                to_add += "\n\t-- res value: "+str(CST.Flags.res_val)
        to_print = flags_to_print + to_add
        return to_print

    @property
    def statut(self):
        """
        retrun true if the currennt statut match the reference statut or false otherwise.
        """
        self._update()
        statut = -1
        if self._last_run_statut == self._ref_statut and (self._last_run_statut == 0):
            statut = 1
        elif self._last_run_statut == self._ref_statut and (self._last_run_statut != 0):
            statut = 2
        elif self._last_run_statut == CST.Flags.CONSTRUCTION:
            statut = 3
        else:
            statut = 0
        return statut

    @property
    def ref_statut(self):
        return self._get_ref_statut(True)

    @property
    def last_run_statut(self):
        return self._get_last_run_statut(True)

    @property
    def printable_statut(self):
        """
        return "OK" if the currennt statuts match the reference statuts or "KO" otherwise.
        """
        if self.statut == 0:
            return CST.ColorConfig.KO +"KO"+CST.ColorConfig.END
        elif self.statut == 1:
            return CST.ColorConfig.OK+"OK"+CST.ColorConfig.END
        elif self.statut == 2:
            return CST.ColorConfig.OK+"OK (WARNING not nominal)"+CST.ColorConfig.END
        elif self.statut == 3:
            return CST.ColorConfig.BUILD+"IN CONSTRUCTION"+CST.ColorConfig.END
        else:
            raise NotImplemented  #pragma: no cover
        return

    @property
    def ref_statut_file(self):
        if self._rel_ref_statut_file:
            return self._rel_ref_statut_file
        else:   # pragma: no cover
            return self._ref_statut_file
        return

    @property
    def last_run_statut_file(self):
        if self._rel_last_run_statut_file:
            return self._rel_last_run_statut_file
        else:   # pragma: no cover
            return self._last_run_statut_file
        return

    def _get_ref_statut(self, update=True):
        if ((self._ref_statut is None) or update):
            self._update_ref_statut()

        if self._ref_statut == CST.Flags.NO_REF:
            return "NO REF STATUT"
        elif self._last_run_statut == CST.Flags.NO_READABLE_REF: # pragma: no cover
            return "NO READABLE STATUT"
        else:
            return str(self._ref_statut)
        return

    def _get_last_run_statut(self, update=True):
        if (self._last_run_statut is None):
            self._update_last_run_statut()
        if (update):
            self._update_last_run_statut()

        if self._last_run_statut == CST.Flags.NO_RES:
            return "NO RES STATUT"
        elif self._last_run_statut == CST.Flags.NO_READABLE_RES:
            return "NO READABLE STATUT"
        else:
            return str(self._last_run_statut)
        raise RuntimeError
        return

    def _update(self):
        self._update_ref_statut()
        self._update_last_run_statut()
        return

    def __repr__(self):
        to_print = ""
        if self.verbosity > 1:
            to_print += "\nref statut file   -> "+ str(self.ref_statut_file)
            to_print += "\ncur statut file   -> "+ str(self.last_run_statut_file)
            to_print += "\nref statut        -> "+ str(self.ref_statut)
            to_print += "\ncur statut        -> "+ str(self.last_run_statut)
            to_print += "\nflags             -> "+ str(self.verbose_flags)
            to_print += "\n"
            to_print += "test statut        > "+ str(self.printable_statut)
        elif self.verbosity == 1:
            to_print += "test statut       -> "+ str(self.printable_statut)
            to_print += "\nflags           -> "+ str(self.verbose_flags)
        else:
            to_print += str(self._baseName)+" -> "+ str(self.printable_statut)
        return to_print
# --------------------------------------------------
