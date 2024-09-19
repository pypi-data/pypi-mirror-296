# !/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2017-07-19 17:22:57.246629"
__version__ = 1.0
# **************************************************
import os
import sys
from nonRegressionTestTools import genericTestBase as GTB

def test_flags():
    NR_TEST_PATTERN = ".slurm"
    RES = {'./01-CHECK-STATUS/00-TEST-ALWAY-OK/runme.slurm': [0],
           './01-CHECK-STATUS/01-TEST-WITHOUT-RES/runme.slurm': [-1],
           './01-CHECK-STATUS/02-TEST-WITHOUT-REF/runme.slurm': [-2],
           './01-CHECK-STATUS/03-TEST_NO_READABLE_REF/runme.slurm': [-3],
           './01-CHECK-STATUS/04-TEST_NO_READABLE_RES/runme.slurm': [-4],
           './01-CHECK-STATUS/05-TEST-DOWNGRADED-RES-BROKEN/runme.slurm': [-5],
           './01-CHECK-STATUS/06-TEST-FIXED-REF-BROKEN/runme.slurm': [-6],
           './01-CHECK-STATUS/07-TEST-OK-BUT-NOT-NOMINAL/runme.slurm': [-7],
           './01-CHECK-STATUS/08-TEST-UNDEFINED/runme.slurm': [-8],
           './01-CHECK-STATUS/09-TEST-UNDER-CONSTRUCTION/runme.slurm': [-2, 999, -8],
           './01-CHECK-STATUS/10-TEST-WITHOUT-REF-AND-RES/runme.slurm': [-2, -1],
           './01-CHECK-STATUS/11-TEST-NO_READABLE_REF-AND-RES/runme.slurm': [-3, -4],
           './02-CHECK-RUN/01-RUN-OK/runme.slurm': [0],
           './02-CHECK-RUN/02-RUN-KO/runme.slurm': [-5],
           './02-CHECK-RUN/03-RUN-FAILED/runme.slurm': [-1],
           './02-CHECK-RUN/04-RUN-UNDER-CONSTRUCTION/runme.slurm': [-2, 999, -8]
           }
    # --------------------------------------------------
    # verbosity_level=0
    # --------------------------------------------------
    test_cases = None
    test_cases = GTB.test_cases(path=os.path.dirname(__file__),
                                ext=NR_TEST_PATTERN,
                                verbosity_level=0)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        assert(RES[k] == val)
    # --------------------------------------------------



    # --------------------------------------------------
    # test regex filter
    # --------------------------------------------------
    RES = {'./02-CHECK-RUN/01-RUN-OK/runme.slurm': [0],
           './02-CHECK-RUN/02-RUN-KO/runme.slurm': [-5],
           './02-CHECK-RUN/03-RUN-FAILED/runme.slurm': [-1],
           './02-CHECK-RUN/04-RUN-UNDER-CONSTRUCTION/runme.slurm': [-2, 999, -8]}
    test_cases = GTB.test_cases(path=os.path.dirname(__file__),
                                regex="02-CHECK-RUN",
                                ext=NR_TEST_PATTERN,
                                verbosity_level=4)
    test_cases.run()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        assert(RES[k] == val)
    # --------------------------------------------------


    # --------------------------------------------------
    # recusrive option
    # --------------------------------------------------
    test_cases = GTB.test_cases(path=os.path.dirname(__file__),
                                recursive = False,
                                ext=NR_TEST_PATTERN,
                                verbosity_level=4)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert({} == flags)
    # --------------------------------------------------

    # --------------------------------------------------
    # test filter_name
    # --------------------------------------------------
    RES = {'./01-CHECK-STATUS/00-TEST-ALWAY-OK/runme.slurm': [0],
           './02-CHECK-RUN/01-RUN-OK/runme.slurm': [0]}
    test_cases = GTB.test_cases(path=os.path.dirname(__file__),
                                filter_name="ok",
                                ext=NR_TEST_PATTERN,
                                verbosity_level=4)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        assert(RES[k] == val)
    # --------------------------------------------------

    # --------------------------------------------------
    # verbosity_level=1
    # --------------------------------------------------
    test_cases = GTB.test_cases(path=os.path.dirname(__file__),
                                filter_name="ok",
                                ext=NR_TEST_PATTERN,
                                verbosity_level=1)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        assert(RES[k] == val)
    # --------------------------------------------------

    # --------------------------------------------------
    # verbosity_level=2
    # --------------------------------------------------
    test_cases = GTB.test_cases(path=os.path.dirname(__file__),
                                filter_name="ok",
                                ext=NR_TEST_PATTERN,
                                verbosity_level=2)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        assert(RES[k] == val)
    # --------------------------------------------------

    # --------------------------------------------------
    # verbosity_level=3
    # --------------------------------------------------
    test_cases = GTB.test_cases(path=os.path.dirname(__file__),
                                filter_name="ok",
                                ext=NR_TEST_PATTERN,
                                verbosity_level=3)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        assert(RES[k] == val)
    # --------------------------------------------------

    # --------------------------------------------------
    # verbosity_level=4
    # --------------------------------------------------
    test_cases = GTB.test_cases(path=os.path.dirname(__file__),
                                filter_name="ok",
                                ext=NR_TEST_PATTERN,
                                verbosity_level=4)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        assert(RES[k] == val)
    # --------------------------------------------------
