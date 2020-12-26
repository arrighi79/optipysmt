#
# This file is part of pySMT.
#
#   Copyright 2014 Andrea Micheli and Marco Gario
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from pysmt.test import TestCase
from pysmt.test import main
from six.moves import cStringIO
from  pysmt.cmd.shell import PysmtShell

class TestSmtLibSolver(TestCase):

    def test_base(self):
        txt = """(declare-fun x () Real)
        (assert (> x 0))
        (check-sat)"""
        f_in = cStringIO(txt)
        f_out = cStringIO()
        args = ""
        pysmtshell = PysmtShell(args)
        pysmtshell.smtlib_solver(f_in, f_out)
        self.assertEqual(f_out.getvalue(), "sat\n")

    def test_omt_minimize(self):
        txt = """(declare-fun x () Real)
(declare-fun y () Real)
(declare-fun z () Real)
(assert (and
        (<= x 10)
        (<= 0 x)
        (<= y 10)
        (<= 4 y)
))
(minimize x)
(check-sat)
(get-objectives)"""
        f_in = cStringIO(txt)
        f_out = cStringIO()
        args = ['-o', 'auto']
        pysmtshell = PysmtShell(args)
        pysmtshell.smtlib_solver(f_in, f_out)
        self.assertEqual(f_out.getvalue(), """sat
(objectives
  (x 0.0)
)
""")

    def test_omt_minmax(self):
        txt = """(declare-fun x () Real)
(declare-fun y () Real)
(declare-fun z () Real)
(assert (and
        (<= x 10)
        (<= 0 x)
        (<= y 11)
        (<= 4 y)
))
(maxmin (x y))
(check-sat)
(get-objectives)"""
        f_in = cStringIO(txt)
        f_out = cStringIO()
        args = ['-o', 'auto']
        pysmtshell = PysmtShell(args)
        pysmtshell.smtlib_solver(f_in, f_out)
        self.assertEqual(f_out.getvalue(), """sat
(objectives
  (((x <= y) ? x : y) 10.0)
)
""")


    def test_omt_box(self):
        txt = """(set-option :opt.priority box)
(declare-fun x () Int)
(declare-fun y () Int)
(declare-fun z () Int)
(assert (and
        (<= x 10)
        (<= 0 x)
        (<= y 10)
        (<= 0 y)
        (<= z 10)
        (<= 0 z)
))
(minimize (- x y))
(minimize (- y x))
(check-sat)
(get-objectives)"""
        f_in = cStringIO(txt)
        f_out = cStringIO()
        args = ['-o', 'auto']
        pysmtshell = PysmtShell(args)
        pysmtshell.smtlib_solver(f_in, f_out)
        self.assertEqual(f_out.getvalue(), """sat
(objectives
  ((x - y) -10)
  ((y - x) -10)
)
""")

    def test_omt_box_unsat(self):
        txt = """(set-option :opt.priority box)
(declare-fun x () Int)
(declare-fun y () Int)
(declare-fun z () Int)
(assert (and
        (<= x 10)
        (<= 11 x)
        (<= y 10)
        (<= 0 y)
        (<= z 10)
        (<= 0 z)
))
(minimize (- x y))
(minimize (- y x))
(check-sat)
(get-objectives)"""
        f_in = cStringIO(txt)
        f_out = cStringIO()
        args = ['-o', 'auto']
        pysmtshell = PysmtShell(args)
        pysmtshell.smtlib_solver(f_in, f_out)
        self.assertEqual(f_out.getvalue(), """unsat
(objectives
)
""")


    def test_omt_lex(self):
        txt = """(set-option :opt.priority lex)
(declare-fun x () Int)
(declare-fun y () Int)
(declare-fun z () Int)
(assert (and
        (<= x 10)
        (<= 0 x)
        (<= y 10)
        (<= 0 y)
        (<= z 10)
        (<= 0 z)
))
(minimize (- x y))
(minimize (- y x))
(check-sat)
(get-objectives)"""
        f_in = cStringIO(txt)
        f_out = cStringIO()
        args = ['-o', 'auto']
        pysmtshell = PysmtShell(args)
        pysmtshell.smtlib_solver(f_in, f_out)
        self.assertEqual(f_out.getvalue(), """sat
(objectives
  ((x - y) -10)
  ((y - x) 10)
)
""")

    def test_omt_int_01(self):
        txt = """(set-option :opt.priority lex)
(declare-fun x () Int)
(declare-fun y () Int)
(declare-fun z () Int)
(assert (and
        (<= x 10)
        (<= 0 x)
        (<= y 10)
        (<= 0 y)
        (<= z 10)
        (<= 0 z)
))
(minimize (- x y))
(minimize (- y x))
(check-sat)
(get-objectives)
(set-option :opt.priority box)
(check-sat)
(get-objectives)
(maxmin (x y))
(check-sat)
(get-objectives)"""
        f_in = cStringIO(txt)
        f_out = cStringIO()
        args = ['-o', 'auto']
        pysmtshell = PysmtShell(args)
        pysmtshell.smtlib_solver(f_in, f_out)
        self.assertEqual(f_out.getvalue(), """sat
(objectives
  ((x - y) -10)
  ((y - x) 10)
)
sat
(objectives
  ((x - y) -10)
  ((y - x) -10)
)
sat
(objectives
  ((x - y) -10)
  ((y - x) -10)
  (((x <= y) ? x : y) 0)
)
""")

    def test_omt_real_01(self):
        txt = """(set-option :opt.priority lex)
(declare-fun x () Real)
(declare-fun y () Real)
(declare-fun z () Real)
(assert (and
        (<= x 10.0)
        (<= 0.0 x)
        (<= y 10.0)
        (<= 0.0 y)
        (<= z 10.0)
        (<= 0.0 z)
))
(minimize (- x y))
(minimize (- y x))
(check-sat)
(get-objectives)
(set-option :opt.priority box)
(check-sat)
(get-objectives)
(maxmin (x y))
(check-sat)
(get-objectives)"""
        f_in = cStringIO(txt)
        f_out = cStringIO()
        args = ['-o', 'auto']
        pysmtshell = PysmtShell(args)
        pysmtshell.smtlib_solver(f_in, f_out)
        self.assertEqual(f_out.getvalue(), """sat
(objectives
  ((x - y) -10.0)
  ((y - x) 10.0)
)
sat
(objectives
  ((x - y) -10.0)
  ((y - x) -10.0)
)
sat
(objectives
  ((x - y) -10.0)
  ((y - x) -10.0)
  (((x <= y) ? x : y) 0.0)
)
""")

    def test_omt_lex_unsat(self):
        txt = """(set-option :opt.priority lex)
(declare-fun x () Int)
(declare-fun y () Int)
(declare-fun z () Int)
(assert (and
        (<= x 10)
        (<= 11 x)
        (<= y 10)
        (<= 0 y)
        (<= z 10)
        (<= 0 z)
))
(minimize (- x y))
(minimize (- y x))
(check-sat)
(get-objectives)"""
        f_in = cStringIO(txt)
        f_out = cStringIO()
        args = ['-o', 'auto']
        pysmtshell = PysmtShell(args)
        pysmtshell.smtlib_solver(f_in, f_out)
        self.assertEqual(f_out.getvalue(), """unsat
(objectives
)
""")

if __name__ == '__main__':
    main()
