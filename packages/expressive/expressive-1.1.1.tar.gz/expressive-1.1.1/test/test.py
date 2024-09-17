#!/usr/bin/env python3

""" Copyright 2024 Russell Fordyce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
import time

import numpy

# FIXME ugly hack
import sys
sys.path.append("src")
import expressive


class TestExpressiveHighlights(unittest.TestCase):

    def test_basic(self):
        data = {
            "a": numpy.array(range(100), dtype="int32"),
            "b": numpy.array([1 for _ in range(100)], dtype="int32"),
        }

        result_expected = numpy.array(range(100)) + 1

        E = expressive.Expressive("a + b")
        E.build(data)
        result = E(data)

        self.assertTrue(numpy.array_equal(result_expected, result))

    def test_speedy(self):
        """ basic use should be fast """
        data = {
            "a": numpy.array(range(10000), dtype="int64"),
            "b": numpy.array(range(10000), dtype="int64"),
        }
        E = expressive.Expressive("a*b")
        E.build(data)
        time_start = time.time()
        result = E(data)
        self.assertTrue(time.time() - time_start < 1)

    def test_offset_parse(self):
        data = {
            "a": numpy.array(range(100), dtype="int64"),
        }
        E = expressive.Expressive("a[i] + a[i+1]")
        E.build(data)

        # give it a spin
        data = {
            "a": numpy.array(range(1000), dtype="int64"),
        }
        result = E(data)

        # TODO manage the last value, which is some cast NaN for now
        self.assertTrue(numpy.array_equal(
            numpy.array(range(1, 2000, 2), dtype="int64")[:-1],
            result[:-1],
        ))


class TestGuess_dtype(unittest.TestCase):

    def test_simple(self):
        data = {
            "a": numpy.array([1,2,3], dtype="uint8"),
        }
        E = expressive.Expressive("2*a")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "uint32")

        # exclusively float32
        data = {
            "a": numpy.array([1,2,3], dtype="float32"),
            "b": numpy.array([1,2,3], dtype="float32"),
        }
        E = expressive.Expressive("a * b")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float32")

        # choose wider when present
        data = {
            "a": numpy.array([1,2,3], dtype="float32"),
            "b": numpy.array([1,2,3], dtype="float64"),
        }
        E = expressive.Expressive("a * b")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float64")

    def test_empty_inputs(self):
        E = expressive.Expressive("2*a")
        with self.assertRaisesRegex(ValueError, r"no data"):
            expressive.dtype_result_guess(E._expr_sympy, data={})

    def test_floating_point_operators(self):
        # most floating point math results in float64
        data = {
            "a": numpy.array([1,2,3], dtype="int32"),
        }
        E = expressive.Expressive("log(a)")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float64")

    def test_float_promote(self):
        # presence of a wider value causes promotion to float64
        data = {
            "a": numpy.array([1,2,3], dtype="int64"),
            "b": numpy.array([1,2,3], dtype="float32"),
        }
        E = expressive.Expressive("a * b")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float64")

        # most values are promoted to float64 regardless of width
        data = {
            "a": numpy.array([1,2,3], dtype="int32"),
        }
        E = expressive.Expressive("log(a)")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float64")

        # while small values are promoted to float32
        data = {
            "a": numpy.array([1,2,3], dtype="int8"),
            "b": numpy.array([1,2,3], dtype="int8"),
        }
        E = expressive.Expressive("log(a) + b")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float32")

    def test_bad(self):
        # boolean is currently unsupported
        data = {
            "a": numpy.array([1,2,3], dtype="bool"),
            "b": numpy.array([1,2,3], dtype="bool"),
        }
        E = expressive.Expressive("a * b")
        with self.assertRaisesRegex(TypeError, r"unsupported.*bool"):
            expressive.dtype_result_guess(E._expr_sympy, data=data)

        # mixed integer signs
        data = {
            "a": numpy.array([1,2,3], dtype="int32"),
            "b": numpy.array([1,2,3], dtype="uint32"),
        }
        E = expressive.Expressive("a * b")
        with self.assertRaisesRegex(TypeError, r"mixed int and uint"):
            expressive.dtype_result_guess(E._expr_sympy, data=data)


class Testdata_cleanup(unittest.TestCase):

    def test_simple(self):
        with self.assertRaisesRegex(ValueError, r"no data"):
            expressive.data_cleanup({})

        data = ["a"]
        with self.assertRaisesRegex(TypeError, r"dict of NumPy arrays, .*list"):
            expressive.data_cleanup(data)

        data = {"a": [1]}
        with self.assertRaisesRegex(TypeError, r"dict of NumPy arrays, .*list"):
            expressive.data_cleanup(data)

        data = {"a": numpy.array([1,2,3], dtype="bool")}
        with self.assertRaisesRegex(TypeError, r"unsupported dtype .*bool"):
            expressive.data_cleanup(data)

    def test_uneven_arrays(self):
        # see TestSingleValues for non-vector data
        data = {
            "a": numpy.array(range(100), dtype="int64"),
            "b": numpy.array(range(99), dtype="int64"),
        }
        with self.assertRaisesRegex(ValueError, r"uneven data lengths .*99"):
            expressive.data_cleanup(data)


class TestSingleValues(unittest.TestCase):

    def test_simple(self):
        data = {
            "a": numpy.array(range(100), dtype="int64"),
            "b": 5,
        }

        result_expected = numpy.array(range(100)) + 5
        E = expressive.Expressive("a + b")
        E.build(data)
        result = E(data)
        self.assertTrue(numpy.array_equal(result_expected, result))

    def test_indexed(self):
        data = {
            "a": numpy.array(range(100), dtype="int64"),
            "b": 5,
        }

        result_expected = numpy.array(range(100)) + 5
        E = expressive.Expressive("a[i] + b")
        E.build(data)
        result = E(data)
        self.assertTrue(numpy.array_equal(result_expected, result))


class Test_input_cleanup(unittest.TestCase):

    def test_simple(self):
        # whitespace removal
        expr_string = expressive.string_expr_cleanup("a * b")
        self.assertEqual(expr_string, "a*b")

    def test_bad(self):
        # junk inputs
        with self.assertRaisesRegex(ValueError, "string"):
            expressive.string_expr_cleanup(None)
        with self.assertRaisesRegex(ValueError, "string"):
            expressive.string_expr_cleanup(3)

        # empty string
        with self.assertRaisesRegex(ValueError, "no content"):
            expressive.string_expr_cleanup("")
        with self.assertRaisesRegex(ValueError, "no content"):
            expressive.string_expr_cleanup(" ")

        # SymPy expr doesn't need these cleanups (already parsed)
        E = expressive.Expressive("a*b")
        expr = E._expr_sympy
        with self.assertRaisesRegex(ValueError, "string"):
            expressive.string_expr_cleanup(expr)

        # literal equals `=` not yet supported [ISSUE 14]
        with self.assertRaisesRegex(ValueError, "="):
            expressive.string_expr_cleanup("a = b")

    def test_adjacent_to_mul(self):
        expr_string = expressive.string_expr_cleanup("2x")
        self.assertEqual(expr_string, "2*x")

        # multiple cleanups
        expr_string = expressive.string_expr_cleanup("1 + 2x - 7y")
        self.assertEqual(expr_string, "1+2*x-7*y")

        # handle function or symbol
        expr_string = expressive.string_expr_cleanup("3cos(2x + pi)")
        self.assertEqual(expr_string, "3*cos(2*x+pi)")

        # function with number in name
        expr_string = expressive.string_expr_cleanup("2x + 3 - log2(n)")
        self.assertEqual(expr_string, "2*x+3-log2(n)")

        # symbol with a number in the name
        expr_string = expressive.string_expr_cleanup("t0 + t2")
        self.assertEqual(expr_string, "t0+t2")

        # FIXME detect and raise or warn for this confusing parse
        expr_string = expressive.string_expr_cleanup("log2(2value3)")
        self.assertEqual(expr_string, "log2(2*value3)")

    def test_pow_xor(self):
        expr_string = expressive.string_expr_cleanup("2^x")
        self.assertEqual(expr_string, "2**x")

    def test_fraction(self):
        expr_string = "1/2x"

        # fails without cleanup
        with self.assertRaises(SyntaxError):
            expressive.string_expr_to_sympy(expr_string)

        # division (actually Mul internally)
        expr_string = expressive.string_expr_cleanup(expr_string)
        self.assertEqual(expr_string, "1/2*x")

        # parsed result should be consistent across inputs
        self.assertEqual(
            expressive.string_expr_to_sympy(expr_string),
            expressive.string_expr_to_sympy("""Mul(Rational(1, 2), Symbol("x"))"""),
            expressive.string_expr_to_sympy("x/2"),
        )


class TestRelativeOffsets(unittest.TestCase):

    def test_paired(self):
        data = {
            "a": numpy.array(range(100), dtype="int64"),
            "b": numpy.array(range(100), dtype="int64"),
            "c": numpy.array(range(100), dtype="int64"),
        }
        E = expressive.Expressive("a[i+1] + b[i-1] + c[i]")
        E.build(data)

        # give it a spin
        data = {
            "a": numpy.array(range(10000), dtype="int64"),
            "b": numpy.array(range(10000), dtype="int64"),
            "c": numpy.array(range(10000), dtype="int64"),
        }
        result = E(data)

        # cherry-pick test cases
        self.assertEqual(result[   1],    0 +    2 +    1)
        self.assertEqual(result[5000], 4999 + 5000 + 5001)
        self.assertEqual(result[9000], 8999 + 9000 + 9001)

        # TODO consider whole array check

    def test_bad(self):
        # multiple indexers
        with self.assertRaisesRegex(ValueError, r"only a single Idx is supported, but got:"):
            E = expressive.Expressive("a[i] + b[n]")

    # FUTURE new test combining non-vector values in relative offset loop [ISSUE 5]


if __name__ == "__main__":
     r = unittest.main(exit=False)
     if not r.result.wasSuccessful():
        sys.exit("some tests failed")  # pragma nocover
