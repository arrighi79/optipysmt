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
from pysmt.test import TestCase, skipIfNoOptimizerForLogic
from pysmt.test import main

from pysmt.shortcuts import Optimizer, GE, Int, Symbol, INT, LE, GT, REAL, Real
from pysmt.shortcuts import BVType, BVUGE, BVSGE, BVULE, BVSLE, BVUGT, BVSGT, BVULT, BVSLT, BVZero, BVOne, BV
from pysmt.shortcuts import And, Plus, Minus, get_env
from pysmt.logics import QF_LIA, QF_LRA, QF_BV
from pysmt.optimization.goal import MaximizationGoal, MinimizationGoal, \
    MinMaxGoal, MaxMinGoal, MaxSMTGoal

from pysmt.exceptions import PysmtUnboundedOptimizationError

class TestOptimization(TestCase):

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_minimization_basic(self):
        x = Symbol("x", INT)
        min = MinimizationGoal(x)
        formula = GE(x, Int(10))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(formula)
                model, cost = opt.optimize(min)
                self.assertEqual(model[x], Int(10))

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_maximization_basic(self):
        x = Symbol("x", INT)
        max = MaximizationGoal(x)
        formula = LE(x, Int(10))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(formula)
                model, cost = opt.optimize(max)
                self.assertEqual(model[x], Int(10))

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_maxmin_basic_lia(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)

        f11 = GE(x, Int(5))
        f12 = LE(x, Int(8))
        f21 = GE(y, Int(11))
        f22 = LE(y, Int(14))
        f31 = GE(z, Int(15))
        f32 = LE(z, Int(18))

        maxmin = MaxMinGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(maxmin)
                self.assertEqual(model[maxmin.term()], Int(8))

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_minmax_basic_lia(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)

        f11 = GE(x, Int(5))
        f12 = LE(x, Int(8))
        f21 = GE(y, Int(11))
        f22 = LE(y, Int(14))
        f31 = GE(z, Int(15))
        f32 = LE(z, Int(18))

        minmax = MinMaxGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(minmax)
                self.assertEqual(model[minmax.term()], Int(15))

    @skipIfNoOptimizerForLogic(QF_LRA)
    def test_maxmin_basic_lra(self):
        x = Symbol("x", REAL)
        y = Symbol("y", REAL)
        z = Symbol("z", REAL)

        f11 = GE(x, Real(5.0))
        f12 = LE(x, Real(8.0))
        f21 = GE(y, Real(11.0))
        f22 = LE(y, Real(14.0))
        f31 = GE(z, Real(15.0))
        f32 = LE(z, Real(18.0))

        maxmin = MaxMinGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_LRA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(maxmin)
                self.assertEqual(model[maxmin.term()], Real(8.0))

    @skipIfNoOptimizerForLogic(QF_LRA)
    def test_minmax_basic_lra(self):
        x = Symbol("x", REAL)
        y = Symbol("y", REAL)
        z = Symbol("z", REAL)

        f11 = GE(x, Real(5.0))
        f12 = LE(x, Real(8.0))
        f21 = GE(y, Real(11.0))
        f22 = LE(y, Real(14.0))
        f31 = GE(z, Real(15.0))
        f32 = LE(z, Real(18.0))

        minmax = MinMaxGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_LRA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(minmax)
                self.assertEqual(model[minmax.term()], Real(15.0))

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_pareto(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        obj1 = MinimizationGoal(Plus(x, y))
        obj2 = MinimizationGoal(Minus(x, y))
        formula = And(GE(x, Int(0)), GE(y, Int(0)), LE(x, Int(10)), LE(y, Int(10)))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(formula)
                models, costs = zip(*opt.pareto_optimize([obj1, obj2]))
                self.assertEqual(len(models), 11)
                self.assertTrue(all(m[x].constant_value() == 0 for m in models))
                self.assertTrue(all(x[0].constant_value() == -x[1].constant_value() for x in costs))

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_pareto_unsat(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        obj1 = MinimizationGoal(Plus(x, y))
        obj2 = MinimizationGoal(Minus(x, y))
        formula = And(GE(x, Int(0)), GE(y, Int(1)), LE(x, Int(10)), LE(y, Int(10)), LE(y, Int(0)))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(formula)
                for x in opt.pareto_optimize([obj1, obj2]):
                    self.assertTrue(False)

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_boxed(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)
        f1 = And(LE(Int(0), x), LE(Int(0), y), LE(Int(0), z))
        f2 = And(LE(x, Int(10)), LE(y, Int(10)), LE(z, Int(10)))
        obj1 = MinimizationGoal(Minus(x, y))
        obj2 = MinimizationGoal(Minus(y, x))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f1)
                opt.add_assertion(f2)
                models = opt.boxed_optimize([obj1, obj2])
                self.assertEqual(len(models), 2)
                self.assertEqual(models[obj1][0].get_py_value(x), 0)
                self.assertEqual(models[obj1][0].get_py_value(y), 10)
                self.assertEqual(models[obj2][0].get_py_value(x), 10)
                self.assertEqual(models[obj2][0].get_py_value(y), 0)

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_boxed_unsat(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)
        f1 = And(LE(Int(0), x), LE(Int(0), y), LE(Int(1), z))
        f2 = And(LE(x, Int(10)), LE(y, Int(10)), LE(z, Int(10)), LE(z, Int(0)))
        obj1 = MinimizationGoal(Minus(x, y))
        obj2 = MinimizationGoal(Minus(y, x))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f1)
                opt.add_assertion(f2)
                models = opt.boxed_optimize([obj1, obj2])
                self.assertTrue(models is None)

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_lex(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)
        t = Symbol("t", INT)
        u = Symbol("u", INT)
        f1 = And(LE(Int(0), x), LE(Int(0), y), LE(Int(0), z), LE(Int(0), u), LE(Int(0), t))
        f2 = And(LE(x, Int(5)), LE(y, Int(5)), LE(z, Int(5)), LE(u, Int(5)), LE(t, Int(5)))
        obj1 = MaximizationGoal(x)
        obj2 = MinimizationGoal(y)
        obj3 = MaximizationGoal(Plus(x, y, z))
        obj4 = MinimizationGoal(t)
        obj5 = MinimizationGoal(u)
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f1)
                opt.add_assertion(f2)
                model, values = opt.lexicographic_optimize([obj1, obj2, obj3, obj4, obj5])
                self.assertEqual(values[0], Int(5))
                self.assertEqual(values[1], Int(0))
                self.assertEqual(values[2], Int(10))

    def test_lex_unsat(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)
        t = Symbol("t", INT)
        u = Symbol("u", INT)
        f1 = And(LE(Int(0), x), LE(Int(0), y), LE(Int(0), z), LE(Int(0), u), LE(Int(0), t), LE(t, Int(-1)))
        f2 = And(LE(x, Int(5)), LE(y, Int(5)), LE(z, Int(5)), LE(u, Int(5)), LE(t, Int(5)))
        obj1 = MaximizationGoal(x)
        obj2 = MinimizationGoal(y)
        obj3 = MaximizationGoal(Plus(x, y, z))
        obj4 = MinimizationGoal(t)
        obj5 = MinimizationGoal(u)
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f1)
                opt.add_assertion(f2)
                model, values = opt.lexicographic_optimize([obj1, obj2, obj3, obj4, obj5])
                self.assertTrue(model is None)
                self.assertTrue(values is None)

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_unsat(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)
        f1 = And(LE(Int(0), x), LE(Int(0), y), LE(Int(1), z))
        f2 = And(LE(x, Int(10)), LE(y, Int(10)), LE(z, Int(10)), LE(z, Int(0)))
        obj1 = MinimizationGoal(Minus(x, y))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                    opt.add_assertion(f1)
                    opt.add_assertion(f2)
                    rt = opt.optimize(obj1)
                    self.assertTrue(rt is None)

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_unbounded(self):
        x = Symbol("x", INT)
        formula = LE(x, Int(10))
        min = MinimizationGoal(x)
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                if opt.can_diverge_for_unbounded_cases():
                    continue
                opt.add_assertion(formula)
                with self.assertRaises(PysmtUnboundedOptimizationError):
                    opt.optimize(min)

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_can_diverge_for_unbounded_cases(self):
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                if not opt.can_diverge_for_unbounded_cases():
                    self.assertIn(oname, ["optimsat", "z3"])

    @skipIfNoOptimizerForLogic(QF_LRA)
    def test_infinitesimal(self):
        x = Symbol("x", REAL)
        formula = GT(x, Real(10))
        min = MinimizationGoal(x)
        for oname in get_env().factory.all_optimizers(logic=QF_LRA):
            with Optimizer(name=oname) as opt:
                if opt.can_diverge_for_unbounded_cases():
                    continue
                opt.add_assertion(formula)
                with self.assertRaises(PysmtUnboundedOptimizationError):
                    opt.optimize(min)

    @skipIfNoOptimizerForLogic(QF_LIA)
    def test_use_case_001(self):
        x = Symbol("x", INT)
        y = Symbol("y", INT)
        z = Symbol("z", INT)
        t = Symbol("t", INT)
        u = Symbol("u", INT)
        f1 = And(LE(Int(0), x), LE(Int(0), y), LE(Int(0), z), LE(Int(0), u), LE(Int(0), t))
        f2 = And(LE(x, Int(5)), LE(y, Int(5)), LE(z, Int(5)), LE(u, Int(5)), LE(t, Int(5)))
        obj1 = MaximizationGoal(x)
        obj2 = MinimizationGoal(y)
        obj3 = MaximizationGoal(Plus(x, y, z))
        obj4 = MinimizationGoal(t)
        obj5 = MinimizationGoal(u)
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                opt.add_assertion(f1)
                opt.add_assertion(f2)
                model, values = opt.lexicographic_optimize([obj1, obj2, obj3, obj4, obj5])
                self.assertEqual(values[0], Int(5))
                self.assertEqual(values[1], Int(0))
                self.assertEqual(values[2], Int(10))

    def test_minimization_basic_BV(self):
        x = Symbol("x", BVType(32))
        min = MinimizationGoal(x)
        formula = BVSGT(x, BV(10, 32))
        for oname in get_env().factory.all_optimizers(logic=QF_BV):
            with Optimizer(name=oname, logic=QF_BV) as opt:
                opt.add_assertion(formula)
                model, cost = opt.optimize(min)
                self.assertEqual(model[x], BV(11, 32))

    def test_maximization_basic_BV(self):
        x = Symbol("x", BVType(32))
        max = MaximizationGoal(x, signed = True)
        formula = BVSLT(x, BV(10, 32))
        for oname in get_env().factory.all_optimizers(logic=QF_BV):
            with Optimizer(name=oname, logic=QF_BV) as opt:
                opt.add_assertion(formula)
                model, cost = opt.optimize(max)
                self.assertEqual(model[x], BV(9, 32))

    def test_maxmin_basic_BV(self):
        x = Symbol("x", BVType(32))
        y = Symbol("y", BVType(32))
        z = Symbol("z", BVType(32))

        f11 = BVSGE(x, BV(5,32))
        f12 = BVSLE(x, BV(8,32))
        f21 = BVSGE(y, BV(11,32))
        f22 = BVSLE(y, BV(14,32))
        f31 = BVSGE(z, BV(15,32))
        f32 = BVSLE(z, BV(18,32))

        maxmin = MaxMinGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_BV):
            with Optimizer(name=oname, logic=QF_BV) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(maxmin)
                self.assertEqual(model[maxmin.term()], BV(8, 32))

    def test_minmax_basic_BV(self):
        x = Symbol("x", BVType(32))
        y = Symbol("y", BVType(32))
        z = Symbol("z", BVType(32))

        f11 = BVSGE(x, BV(5, 32))
        f12 = BVSLE(x, BV(8, 32))
        f21 = BVSGE(y, BV(11, 32))
        f22 = BVSLE(y, BV(14, 32))
        f31 = BVSGE(z, BV(15, 32))
        f32 = BVSLE(z, BV(18, 32))

        minmax = MinMaxGoal([x, y, z])

        for oname in get_env().factory.all_optimizers(logic=QF_BV):
            with Optimizer(name=oname, logic=QF_BV) as opt:
                opt.add_assertion(f11)
                opt.add_assertion(f12)

                opt.add_assertion(f21)
                opt.add_assertion(f22)

                opt.add_assertion(f31)
                opt.add_assertion(f32)

                model, cost = opt.optimize(minmax)
                self.assertEqual(model[minmax.term()], BV(15, 32))

    def test_maxsmt_basic(self):
        x = Symbol("x", INT)
        maxsmt = MaxSMTGoal()
        maxsmt.add_soft_clause(GE(x, Int(5)), 8)
        maxsmt.add_soft_clause(GE(x, Int(30)), 20)
        maxsmt.add_soft_clause(LE(x, Int(10)), 100)
        maxsmt.add_soft_clause(LE(x, Int(9)), 6)
        formula = GE(x, Int(9))
        for oname in get_env().factory.all_optimizers(logic=QF_LIA):
            with Optimizer(name=oname) as opt:
                if oname == "optimsat":
                    self.assertEqual(True, True)
                else:
                    print(oname)
                    opt.add_assertion(formula)
                    model, cost = opt.optimize(maxsmt)
                    self.assertEqual(model[x], Int(9))

if __name__ == '__main__':
    main()
