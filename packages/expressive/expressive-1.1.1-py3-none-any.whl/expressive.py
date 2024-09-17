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

import re
import textwrap

import numba
import sympy
from sympy.utilities.lambdify import MODULES as lambdify_modules

import numpy


DTYPES_SUPPORTED = {
    # numpy.dtype("bool"):     1,
    numpy.dtype("uint8"):    8,
    numpy.dtype("uint16"):  16,
    numpy.dtype("uint32"):  32,
    numpy.dtype("uint64"):  64,
    numpy.dtype("int8"):     8,
    numpy.dtype("int16"):   16,
    numpy.dtype("int32"):   32,
    numpy.dtype("int64"):   64,
    numpy.dtype("float32"): 32,
    numpy.dtype("float64"): 64,
    # numpy.dtype("complex64"): 64,
    # numpy.dtype("complex128"): 128,
}


def data_cleanup(data):
    # dict of numpy arrays
    # FUTURE optional pandas support
    if not data:
        raise ValueError("no data provided")
    if not isinstance(data, dict):
        raise TypeError(f"data must be a dict of NumPy arrays, but got {type(data)}")

    result = {}
    vector_length = {}
    for name, ref in data.items():
        # coerce single python values to 0-dim numpy values
        # FIXME makes even small values too wide (int64,float64)
        if isinstance(ref, (int, float)):
            ref = numpy.array(ref)
        if not isinstance(ref, numpy.ndarray):
            raise TypeError(f"data must be a dict of NumPy arrays, but has member ({name}:{type(ref)})")
        if ref.dtype not in DTYPES_SUPPORTED:
            raise TypeError(f"unsupported dtype ({name}:{ref.dtype})")
        # 0-dim values have shape==() and `len(array) # TypeError: len() of unsized object`
        vector_length[name] = len(ref) if ref.shape else 0
        result[name] = ref  # pack reference into collection

    # FUTURE support uneven input arrays when indexed [ISSUE 10]
    set_vector_lengths = set(vector_length.values())
    if len(set_vector_lengths - {0}) != 1:
        raise ValueError(f"uneven data lengths (must be all equal or 0 (non-vector)): {set_vector_lengths}")

    return result


def string_expr_cleanup(expr_string):
    """ a few rounds of basic cleanup to ease usage """
    # FUTURE reconsider if these can use the transformation subsystem
    if not isinstance(expr_string, str):
        raise ValueError("expr must be a string")

    # FUTURE handle equality [ISSUE 14]
    #   expr_string = expr_string.replace("==", "=")
    #   `A = B` can be `A - B`
    #   handle indexing
    if "=" in expr_string:
        raise ValueError("no support for = yet")

    # discard all whitespace to ease string processing
    expr_string = re.sub(r"\s+", r"", expr_string)  # expr_string.replace(" ", "")

    # user probably meant Pow() not bitwise XOR
    # FIXME add to warning subsystem `if "^" in expr_string:` and allow configuring
    expr_string = expr_string.replace("^", "**")

    # SymPy expects symbols to be separated from Numbers for multiplication
    #   ie. "5x+7" -> "5*x+7"
    # however, care needs to be taken to avoid splitting symbols and functions
    # which contain a number, like `t3`, `log2()`, etc.
    # currently considers only matches where a number appears directly after
    #   start of string | basic operators +-*/ | open parenthesis
    # and then a string starts (symbol)
    # likely this could be better tokenized by Python AST or SymPy itself
    expr_string = re.sub(r"(^|[\+\-\*\/]|\()(\d+)(\w)", r"\1\2*\3", expr_string)

    # make sure there's something left
    if not expr_string:
        raise ValueError("no content after cleanup")

    return expr_string


def string_expr_to_sympy(expr_string):
    """ parse string to a SymPy expression
        this is largely a wrapper around sympy.parse_expr()
        however, it also enables indexing Symbols via IndexBase[Idx]
    """
    local_dict = {}  # used for relative_offset and maybe more

    # detect and manage relative offsets
    # FUTURE handle advanced relative indexing logic [ISSUE 11]
    offset_values = {}
    offset_range = [0, 0]  # spread amongst offsets as [min,max]
    for chunk in re.findall(r"(\w+)\[(.+?)\]", expr_string):
        base, indexing_block = chunk
        indexer = str(sympy.parse_expr(indexing_block).free_symbols.pop())
        try:  # extract the offset amount ie. x[i-1] is -1
            offset = sympy.parse_expr(indexing_block).atoms(sympy.Number).pop()
        except KeyError:
            offset = 0  # no offset like x[i]
        if offset < 0:
            offset_range[0] = min(offset_range[0], offset)
        elif offset > 0:
            offset_range[1] = max(offset_range[1], offset)
        offset_values[base] = sympy.IndexedBase(base)
        offset_values[indexer] = sympy.Idx(indexer)
    local_dict.update(offset_values)

    # FUTURE consider transformation system instead of direct regex hackery
    expr_sympy = sympy.parse_expr(expr_string, local_dict=local_dict)

    # assert there is only a single Idx
    # FUTURE multiple Idx can generate deeper loops
    indexers = expr_sympy.atoms(sympy.Idx)  # set of Symbols
    if len(indexers) > 1:
        raise ValueError(f"only a single Idx is supported, but got: {indexers}")

    # make dicts of {name: symbol} for caller
    symbols  = {s.name: s for s in expr_sympy.atoms(sympy.Symbol)}
    symbols  = {n: symbols[n] for n in sorted(symbols)}  # make symbol ordering consistent
    indexers = {s.name: offset_range for s in indexers}  # NOTE only one value
    # FIXME atoms(Symbol) demotes IndexBase and Idx to Symbol in result [ISSUE 9]
    for name_idx in indexers.keys():  # expressly remove Idx names
        del symbols[name_idx]

    return expr_sympy, symbols, indexers


def dtype_result_guess(expr, data):
    """ attempt to automatically determine the resulting dtype given an expr and data

        this is a backup where the user has not provided a result dtype
        possibly it could support warning for likely wrong dtype

        this is not expected to be a general solution as the problem is open-ended
        and likely depends on the real data

        WARNING this logic assumes the highest bit-width is 64
          larger widths will require rewriting some logic!
          intermediately a user should specify the type, assuming
          a (future) numba really has support for it
    """
    # set of dtypes from given data
    dtypes_expr = {c.dtype for c in data.values()}  # set of NumPy types

    # throw out some obviously bad cases
    if not dtypes_expr:
        raise ValueError("no data provided")
    dtypes_unsupported = dtypes_expr - set(DTYPES_SUPPORTED.keys())
    if dtypes_unsupported:
        raise TypeError(f"unsupported dtypes: {dtypes_unsupported}")

    # helper functions for string dtype set membership checks
    #   these are useful because set comparisons are less-flexible
    #   than numpy types equality checks, which will handle strings
    # examples
    #   numpy.dtype("float64") == "float64"      # True
    #   "float64" == numpy.dtype("float64")      # True
    #   {"float64"} == {numpy.dtype("float64")}  # False
    #   {numpy.dtype("float64")} == {"float64"}  # False
    #   "float64" in {numpy.dtype("float64")}    # False

    def set_contains_dtype(dtype_test):
        if isinstance(dtype_test, str):
            return any((dtype_test == dt) for dt in dtypes_expr)
        # elif isinstance(dtype_test, numpy.dtype):
        #     return numpy.dtype(dtype_test) in dtypes_expr
        raise TypeError(f"BUG: unsupported dtype type {type(dtype_test)}: {dtype_test}")

    if set_contains_dtype("float64"):
        return numpy.dtype("float64")
    # promote 32-bit float to 64-bit when greater types are present
    max_bitwidth = max(DTYPES_SUPPORTED[dt] for dt in dtypes_expr)
    if set_contains_dtype("float32"):
        if max_bitwidth > 32:
            return numpy.dtype("float64")
        return numpy.dtype("float32")

    # result is logically floating-point
    # TODO these should be part of a more serious attempt to constrain inputs
    #   in addition to being available for guessing resulting type,
    #   even if the constraints are (initially) warns, not hard errors
    # see https://docs.sympy.org/latest/modules/functions/elementary.html
    if (
        expr.atoms(
            # straightforward floats
            sympy.Float,
            # trancendental constants
            sympy.pi,
            sympy.E,
            # FUTURE general scipy.constants support
            # common floating-point functions
            sympy.log,
            sympy.exp,
            # sympy.sqrt,  # NOTE simplifies to Pow(..., Rational(1,2))
            # sympy.cbrt,  #   can be found with expr.match(cbrt(Wild('a')))
            # trig functions
            sympy.sin, sympy.asin, sympy.sinh, sympy.asinh,
            sympy.cos, sympy.acos, sympy.cosh, sympy.acosh,
            sympy.tan, sympy.atan, sympy.tanh, sympy.atanh,
            sympy.cot, sympy.acot, sympy.coth, sympy.acoth,
            sympy.sec, sympy.asec, sympy.sech, sympy.asech,
            sympy.csc, sympy.acsc, sympy.csch, sympy.acsch,
            sympy.sinc,
            sympy.atan2,
            # LambertW?  # TODO is complex support actually extra work?
        ) or (
            # discover simple division
            # direct Integers are Rational, but fractional atoms are not Integer
            # additionally, simple divisions will simplify to Integer
            #   >>> parse_expr("4").atoms(Rational), parse_expr("4").atoms(Integer)
            #   ({4}, {4})
            #   >>> parse_expr("4/2").atoms(Rational), parse_expr("4/2").atoms(Integer)
            #   ({2}, {2})
            #   >>> e = "4/2*x + 1/3*y"
            #   >>> parse_expr(e).atoms(Rational) - parse_expr(e).atoms(Integer)
            #   {1/3}
            expr.atoms(sympy.Rational) - expr.atoms(sympy.Integer)
        ) or (
            # detect N/x constructs
            #   >>> srepr(parse_expr("2/x"))
            #   "Mul(Integer(2), Pow(Symbol('x'), Integer(-1)))"
            expr.match(sympy.Pow(sympy.Wild("", properties=[lambda a: a.is_Symbol or a.is_Function]), sympy.Integer(-1)))
        )
    ):
        # if any(("float64" == t) for t in dtypes):  # redundant
        #     return "float64"
        # if set_of_1x_dtype("float32"):  # collection is {"float32"}  # redundant
        #     return "float32"
        if max_bitwidth <= 16:  # TODO is this a good assumption?
            return numpy.dtype("float32")
        return numpy.dtype("float64")

    # now pick the largest useful int
    # NOTE constant coefficients should all be Integer (Rational) if reached here

    w_signed   = 0  # NOTE Falsey
    w_unsigned = 0
    for dtype in dtypes_expr:
        if numpy.issubdtype(dtype, numpy.signedinteger):
            w_signed = max(w_signed, DTYPES_SUPPORTED[dtype])
        elif numpy.issubdtype(dtype, numpy.unsignedinteger):
            w_unsigned = max(w_unsigned, DTYPES_SUPPORTED[dtype])
        else:
            raise TypeError(f"BUG: failed to determine if {dtype} is a signed or unsigned int (is it a float?)")
    if w_signed and w_unsigned:
        raise TypeError("won't guess dtype for mixed int and uint, must be provided")
    if w_signed and not w_unsigned:
        return numpy.dtype("int64") if w_signed > 32 else numpy.dtype("int32")  # FUTURE >=
    if not w_signed and w_unsigned:
        return numpy.dtype("uint64") if w_unsigned > 32 else numpy.dtype("uint32")  # FUTURE >=

    raise TypeError(f"BUG: couldn't determine a good dtype for {dtypes_expr}")


def signature_generate(symbols, data, dtype_result):
    # FUTURE support for names (mabye an upstream change to numba)
    #   likely further C-stlye like `void(int32 a[], int64 b)`
    # without names, the dtypes are positional, so ordering must be maintained
    # within logic that could reorder the arguments after fixing the signature!
    # however, when the user calls the Expressive instance,
    # data is passed as kwargs `fn(**data)` to the inner function
    mapper = []
    for name in symbols:
        ref = data[name]
        # make a field like `array(int64, 1d, C)`
        dims   = 1 if ref.shape else 0  # FUTURE support additional dimensions
        layout = "C"  # FUTURE allow other layouts (FORTRAN) and get from array
        dtype  = getattr(numba.types, str(ref.dtype))  # FIXME brittle, can `numba.typeof()` be used?
        field  = numba.types.Array(dtype, dims, layout)
        mapper.append(field)

    # create function signature
    dtype = getattr(numba.types, str(dtype_result))
    return numba.types.Array(dtype, 1, "C")(*mapper)


def loop_function_template_builder(expr, symbols, indexers, dtype_result):
    """ template workflow for indexed values
    """
    # build namespace with everything needed to support the new callable
    # simplified version of sympy.utilities.lambdify._import
    _, _, translations, import_cmds = lambdify_modules["numpy"]
    expr_namespace = {"I": 1j}  # alt `copy.deepcopy(lambdify_modules["numpy"][1])`
    for import_line in import_cmds:
        exec(import_line, expr_namespace)
    for sympyname, translation in translations.items():
        expr_namespace[sympyname] = expr_namespace[translation]

    # TODO allow seeding the result array for self-reference
    #   specifically this is for referring to the result, not
    #   relative offsets of a given array

    # FIXME ugly, convert to loop with enumerate and error on >=1 index
    if len(indexers) != 1:
        raise RuntimeError("BUG: indexers must be len 1 for now (see string_expr_to_sympy)")
    indexer, (start, end) = next(iter(indexers.items()))

    # FIXME numpy.nan filler may not always be appropriate
    TEMPLATE = """
    def expressive_wrapper({argsblock}):
        length = len({sizer_name})
        result = numpy.full(length, numpy.nan, dtype={dtype_result})
        for {indexer} in range({start}, length - {end} + 1):
            result[{indexer}] = {expr}
        return result
    """

    argsblock = ", ".join(symbols.keys())

    # TODO is next(iter()) hack better?
    # FUTURE: need to manage this with [ISSUE 10] uneven arrays
    for symbol in expr.atoms(sympy.IndexedBase):
        sizer_name = symbol
        break
    else:
        raise RuntimeError("BUG: using template path without IndexedBase symbol")

    # build and extract
    T = TEMPLATE.format(
        argsblock=argsblock,
        sizer_name=sizer_name,
        dtype_result=dtype_result,
        expr=expr,
        indexer=indexer,
        start=start,
        end=end,
    )
    T = textwrap.dedent(T)

    exec(T, expr_namespace)
    fn = expr_namespace["expressive_wrapper"]

    return fn


class Expressive:

    def __init__(self, expr, *, config=None):
        # FUTURE make cleanup optional (arg or config)
        self._expr_source_string = string_expr_cleanup(expr)
        self._expr_sympy, self._symbols, self._indexers = string_expr_to_sympy(self._expr_source_string)

        "config hoopla"
        self.signatures_mapper = {}

    def build(self, data, *, dtype_result=None):  # arch target?
        data = data_cleanup(data)
        if dtype_result is None:
            dtype_result = dtype_result_guess(self._expr_sympy, data)

        signature = signature_generate(self._symbols, data, dtype_result)

        if self._indexers:
            expr_fn = loop_function_template_builder(self._expr_sympy, self._symbols, self._indexers, dtype_result)
        else:
            expr_fn = sympy.lambdify(self._symbols.values(), self._expr_sympy)

        built_function = numba.jit(
            signature,
            nopython=True,  # now the default
            # fastmath=True,  # FUTURE config setting
            parallel=True,  # FUTURE config setting
        )(expr_fn)

        self.signatures_mapper[signature] = built_function

        return self  # enable dot chaining

    def __call__(self, data, dtype_result=None):
        data = data_cleanup(data)
        if dtype_result is None:
            dtype_result = dtype_result_guess(self._expr_sympy, data)
        signature = signature_generate(self._symbols, data, dtype_result)

        return self.signatures_mapper[signature](**data)
