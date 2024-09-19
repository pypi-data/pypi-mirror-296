# !/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2017-07-19 17:22:57.246629"
__version__ = 1.0
# **************************************************


# ////////////////////////////////////////////////////////////////////////////////////////////////////
#                    BEGINING OF THE CODE
# ////////////////////////////////////////////////////////////////////////////////////////////////////
from . import constantes as CST
from . import runners as RUN
from . import statutsManager as StatM
from . import filters
import os
import numpy as np

class TestCase(CST.VerbosityManager):
    """
    This is the test case object
    """

    def __init__(self, cmd:str, cwd:str=None,**kwd):
        super().__init__(**kwd)
        self._abs_cmd_file = cmd
        self._cwd = cwd
        self._cmd_file = None          # propertie fill by initial_process
        self._cmd_fileName = None      # propertie fill by initial_process
        self._cmd_fileNameExt = None   # propertie fill by initial_process
        self._abs_dir = None           # propertie fill by initial_process
        self._rel_dir = None           # propertie fill by initial_process
        self._initial_process()
        self.statm = StatM.StatutManager(abs_dir=self._abs_dir,
                                         rel_dir=self._rel_dir,
                                         baseName=self._cmd_fileName,
                                         verbosity_level=self.verbosity)

        return

    def _initial_process(self):
        if not(os.path.isfile(self._abs_cmd_file)):   #pragma: no cover
            try:
                self._abs_cmd_file = os.path.join(os.getcwd,self._abs_cmd_file)
                if not(os.path.isfile(self._abs_cmd_file)):
                    raise ValueError("{} does not exist.\n Test case can't be build".format(self.cmd))
            except:
                raise ValueError("{} does not exist.\n Test case can't be build".format(self.cmd))

        self._abs_dir = os.path.dirname(self._abs_cmd_file)
        if self._cwd is not None:
            if not os.path.isdir(self._cwd):   #pragma: no cover
                raise ValueError("{} is not a directory".format(self._cwd))
            else:
                try:
                    self._rel_dir = "./"+self._abs_dir.split(self._cwd)[-1][1:]
                    abs_p = os.path.join(str(self._cwd), str(self._rel_dir))
                    if not os.path.isdir(abs_p):   #pragma: no cover
                        print("Warning relative path can be constructed\n current work dir \n {}\n path".foramt(sel._cwd, self._abs_dir))
                        raise RuntimeError
                except:   #pragma: no cover
                    self._rel_dir = None

        self._cmd_file = os.path.basename(self._abs_cmd_file)
        splitFile = os.path.splitext(self._cmd_file)
        self._cmd_fileName = splitFile[0]
        self._cmd_fileNameExt = splitFile[1]
        self._set_runner()
        return

    def _get_test_header(self):
        to_print = ""
        if self.verbosity > 0:
            to_print += "-"*20 + "test case" +"-"*20
            to_print += "\ndir               -> "+ self.directory
        else:
            to_print += self.directory+" "
        if self.verbosity > 1:
            to_print += "\nCommande file     -> "+ self._cmd_file
        return to_print

    def _get_test_end(self):
        to_print = ""
        if self.verbosity > 0:
            to_print = "-"*(40+len("test_case"))
        return to_print

    def __repr__(self):
        to_print = "\n"
        to_print += self._get_test_header()
        if self.verbosity > 1:
            to_print += "\nabs dir           -> "+ self._abs_dir
            to_print += "\nrel dir           -> "+ self._rel_dir
        if self.verbosity == 1:
            to_print += "\n"
        to_print += self.statm.__str__()
        to_print += "\n"
        to_print += self._get_test_end()
        return to_print

    def _set_runner(self):
        self._runner = RUN.BashRunner(cmd_file=self._cmd_file,
                                      abs_dir=self._abs_dir,
                                      verbosity_level=self.verbosity)
        return

    @property
    def abs_dir(self):
        """
        return the abolute path to the directory where the test is.
        """
        return self._abs_dir

    @property
    def directory(self):
        """
        return the directory where the test is.
        it can be the absolute or relative path .
        """
        if self._cwd is None:   #pragma: no cover
            return self._abs_dir
        else:
            if self._rel_dir:
                return self._rel_dir
            else:               #pragma: no cover
                return self._abs_dir
        return

    @property
    def filename(self):
        """
        return the filename of the receipy to run the test
        """
        return self._cmd_fileName + self._cmd_fileNameExt

    def run(self):
        """
        run the test
        """
        self._runner.run()
        self.bilan()
        return

    def print_simplify_statut(self):
        """
        return a simplify printable statut of the test
        """
        if self.verbosity > 0:
            to_print = "test statut        -> "+ str(self.statm.printable_statut)
        else:
             to_print = str(self.statm.printable_statut)
        return to_print

    def flags(self):
        return self.statm.get_flags()

    def flags_msg(self):
        """
        return the flags raised by the test.
        """
        to_print = ""
        if self.statm.statut != 1:
            to_print += self.statm.printable_statut +" "+ self.directory+" "+self.filename
            to_print += " "+self.statm.verbose_flags
            to_print.rstrip()
            print(to_print)
        else:
            pass
        return

    def bilan(self):
        """
        return a bilan for the test
        """
        to_print = " "+str(self.statm.printable_statut)
        to_print += " -- " + self.directory + " " + self._cmd_file + ""
        print(to_print)
        return

# --------------------------------------------------


class test_cases(CST.VerbosityManager):
    """
    This is the object test base which contain all test_case object and some usefull fonctions to act on them
    """

    def __init__(self, path:str=os.getcwd(),
                 recursive:bool=True,
                 filter_name:str="",
                 regex:str="",
                 ext=".slurm", **kwd):
        super().__init__(**kwd)
        self.path = path
        self.recursive = recursive
        self.filter_name = filter_name
        self.regex=regex
        self.testCases = []
        self.ext = ext
        self._find_test_cases()
        self._filters = []
        self._set_filters()
        self._apply_filters()
        self._sort()
        self.all_test_OK = False
        return

    def _find_test_cases(self):
        """
        return findf *.ext, path, results
        where ext is .slurm by default
        """
        for root, subFolder, files in os.walk(self.path):
            for ifile in files:
                splitfile = os.path.splitext(ifile)
                if splitfile[1] == self.ext:
                    exe = os.path.join(root, ifile)
                    self.testCases.append(TestCase(cmd=exe,
                                                   cwd=self.path,
                                                   verbosity_level=self.verbosity))
            if not self.recursive:
                break
        return

    def _sort(self):
        dirs = [test.abs_dir for test in self.testCases]
        idx = list(zip(dirs, range(len(dirs))))
        # sort by directory name
        cas = {}
        for k in idx:
            if k[0] in cas:
                cas[k[0]].append(k[1])
            else:
                cas[k[0]] = [k[1]]
        dirs = np.unique(dirs)
        dirs.sort()
        # sort by filname in directory
        new_order = []
        for idir in dirs:
            names = [self.testCases[i].filename for i in cas[idir]]
            idx2 = dict(zip(names, range(len(names))))
            names.sort()
            new_idx = []
            for name in names:
                new_idx.append(idx2[name])
            new_order += list(np.array(cas[idir])[new_idx])
        self.testCases = [self.testCases[i] for i in new_order]
        return


    def _set_filters(self):
        allow_filters = filters.iTestFilter.implemented_filters
        if self.filter_name in allow_filters.keys():
            if self.filter_name == "regex":
                pass   #pragma: no cover
            else:
                ifilter = allow_filters[self.filter_name](initial_list=self.testCases)
                self._filters.append(ifilter)
        else:
            if self.filter_name == "":
                pass
            else:   #pragma: no cover
                raise NotImplementedError("\n Filter \"{}\" is not allowed\n Candidates are {}".format(self.filter_name, ", ".join(list(allow_filters.keys()))))
        if self.regex != "":
                ifilter = allow_filters["regex"](initial_list=self.testCases,regex=self.regex)
                self._filters.append(ifilter)

        return

    def _apply_filters(self):
        for ifilter in self._filters:
            self.testCases = ifilter.apply()
            self.testCases = ifilter.lst
        if self.verbosity > 1:
            print("filter applied")
            print("run only\n", self.testCases)
        return

    def print_tests_to_fix(self, *args,  **kwd):
        """
        print all tests to fix.
        """
        color = CST.ColorConfig.FLAG
        cend = CST.ColorConfig.END
        print("\n"+color+"-"*15+"TESTS WITH NO NOMINAL FLAG"+"-"*20+cend)
        statuts = []
        for icase in self.testCases:
            icase.flags_msg()
        print(color+"-"*50+cend)
        return

    def print_stats(self, *args,  **kwd):
        """
        print stats messages
        """
        statuts = []
        for icase in self.testCases:
            statuts.append(icase.statm.statut)

        ct_tests = len(self.testCases)
        statuts = np.array(statuts, dtype=np.int32).reshape(-1)
        ct_ok = np.argwhere(statuts == 1).shape[0]
        ct_build = np.argwhere(statuts == 3).shape[0]
        to_print = ""
        if ct_tests > 0:
            ratio = ct_ok/ct_tests*100
            ct_failed = ct_tests-ct_ok-ct_build
            to_print = "\n"+CST.ColorConfig.SUMMARY+"-"*50+CST.ColorConfig.END
            to_print += "\nSummary : |"+CST.ColorConfig.OK+"{:2.1f}% OK ({}/{})".format(ratio, ct_ok,ct_tests)+CST.ColorConfig.END+" |"
            to_print += CST.ColorConfig.KO+"{:2.1f}% KO ({}/{})".format(ct_failed/ct_tests*100,ct_failed,ct_tests,)+CST.ColorConfig.END+"| "
            to_print += CST.ColorConfig.BUILD+"{:2.1f}% IN CONSTRUCTION ({}/{})".format(ct_build/ct_tests*100,ct_build,ct_tests,)+CST.ColorConfig.END+"| "
            to_print += "\n"+CST.ColorConfig.SUMMARY+"-"*50+CST.ColorConfig.END
            if ct_tests == ct_ok:
                self.all_test_OK = True
        else:
            to_print = "0 test run"
            self.all_test_OK = True
        print(to_print)
        return

    def print_bilan(self,quiet:bool=False, *args,  **kwd):
        """
        print bilan messages
        """
        print()
        print("-"*50)
        print(" "*25+"Bilan (verbosity: {})".format(self.verbosity)+" "*25)
        print("-"*50)
        if self.verbosity > 0:
            print(self.testCases)
        else:
            for icase in self.testCases:
                icase.bilan()
        self.print_stats()
        if not(quiet):
            if not self.all_test_OK:
                self.print_tests_to_fix()
        print("-"*50)
        return

    def run(self, *args, **kwd):
        """
        run all the selected tests
        options:
        -b to run only the broken tests
        -c to run only the broken tests
        """
        for icase in self.testCases:
            iProc = icase.run()
        # self.print_bilan( *args, **kwd)
        return

    def flags(self, *args, **kwd):
        """
        run all the selected tests
        options:
        -b to run only the broken tests
        -c to run only the broken tests
        """
        all_flags = {}
        for icase in self.testCases:
            flags = icase.flags()
            all_flags[os.path.join(icase.directory, icase.filename)] = flags
        # self.print_bilan( *args, **kwd)
        return all_flags

# --------------------------------------------------
