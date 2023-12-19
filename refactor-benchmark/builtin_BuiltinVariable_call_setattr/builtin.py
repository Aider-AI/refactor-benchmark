import contextlib
import functools
import inspect
import itertools
import logging
import math
import operator
import types
from collections import defaultdict, OrderedDict
from typing import Dict, List

import torch
from torch import sym_float, sym_int

from .. import config, polyfill, variables
from ..exc import (
    AttributeMutationError,
    unimplemented,
    Unsupported,
    UserError,
    UserErrorType,
)
from ..guards import GuardBuilder, install_guard
from ..replay_record import DummyModule
from ..source import AttrSource, GetItemSource, is_constant_source, TypeSource
from ..utils import (
    build_checkpoint_variable,
    check_constant_args,
    check_numpy_ndarray_args,
    check_unspec_python_args,
    extract_fake_example_value,
    get_fake_value,
    guard_if_dyn,
    is_utils_checkpoint,
    istype,
    numpy_operator_wrapper,
    proxy_args_kwargs,
    tensortype_to_dtype,
)
from .base import MutableLocal, typestr, VariableTracker
from .constant import ConstantVariable
from .ctx_manager import EventVariable, StreamVariable
from .dicts import ConstDictVariable, DefaultDictVariable, SetVariable
from .lists import (
    BaseListVariable,
    ListIteratorVariable,
    ListVariable,
    SizeVariable,
    TupleIteratorVariable,
    TupleVariable,
)
from .tensor import FakeItemVariable, SymNodeVariable, UnspecializedPythonVariable
from .user_defined import UserDefinedVariable

log = logging.getLogger(__name__)


IN_PLACE_DESUGARING_MAP = {
    operator.iadd: operator.add,
    operator.isub: operator.sub,
    operator.imul: operator.mul,
    operator.ifloordiv: operator.floordiv,
    operator.itruediv: operator.truediv,
    operator.imod: operator.mod,
    operator.imatmul: operator.imatmul,
    operator.ilshift: operator.lshift,
    operator.irshift: operator.rshift,
    operator.ipow: operator.pow,
    operator.iand: operator.and_,
    operator.ior: operator.or_,
    operator.ixor: operator.xor,
}


def _polyfill_call_impl(name):
    """Create a BuiltinVariable.call_{name} method that inlines through polyfill.{name}"""

    def call_fn(self, tx, *args, **kwargs):
        return tx.inline_user_function_return(
            variables.UserFunctionVariable(fn), args, kwargs
        )

    fn = getattr(polyfill, name)
    call_fn.__name__ = f"call_{name}"
    return call_fn


class BuiltinVariable(VariableTracker):
    @staticmethod
    @functools.lru_cache(None)
    def _constant_fold_functions():
        fns = {
            abs,
            all,
            any,
            bool,
            callable,
            chr,
            divmod,
            float,
            int,
            len,
            max,
            min,
            ord,
            pow,
            repr,
            round,
            str,
            str.format,
            sum,
            type,
            operator.pos,
            operator.neg,
            operator.not_,
            operator.invert,
            operator.pow,
            operator.mul,
            operator.matmul,
            operator.floordiv,
            operator.truediv,
            operator.mod,
            operator.add,
            operator.sub,
            operator.getitem,
            operator.lshift,
            operator.rshift,
            operator.and_,
            operator.or_,
            operator.xor,
            operator.ipow,
            operator.imul,
            operator.imatmul,
            operator.ifloordiv,
            operator.itruediv,
            operator.imod,
            operator.iadd,
            operator.isub,
            operator.ilshift,
            operator.irshift,
            operator.iand,
            operator.ixor,
            operator.ior,
            operator.index,
        }
        fns.update(x for x in math.__dict__.values() if isinstance(x, type(math.sqrt)))
        return fns

    def can_constant_fold_through(self):
        return self.fn in self._constant_fold_functions()

    @staticmethod
    @functools.lru_cache(None)
    def _fx_graph_functions():
        fns = {
            operator.pos,
            operator.neg,
            operator.not_,
            operator.invert,
            operator.pow,
            operator.mul,
            operator.matmul,
            operator.floordiv,
            operator.truediv,
            operator.mod,
            operator.add,
            operator.lt,
            operator.gt,
            operator.ge,
            operator.le,
            operator.ne,
            operator.eq,
            operator.sub,
            operator.getitem,
            operator.lshift,
            operator.rshift,
            operator.and_,
            operator.or_,
            operator.xor,
            operator.ipow,
            operator.imul,
            operator.imatmul,
            operator.ifloordiv,
            operator.itruediv,
            operator.imod,
            operator.iadd,
            operator.isub,
            operator.ilshift,
            operator.irshift,
            operator.iand,
            operator.ixor,
            operator.ior,
        }
        return fns

    @staticmethod
    @functools.lru_cache(None)
    def _binops():
        # function -> ([forward name, reverse name, in-place name], in-place op)
        fns = {
            operator.add: (["__add__", "__radd__", "__iadd__"], operator.iadd),
            operator.sub: (["__sub__", "__rsub__", "__isub__"], operator.isub),
            operator.mul: (["__mul__", "__rmul__", "__imul__"], operator.imul),
            operator.truediv: (
                ["__truediv__", "__rtruediv__", "__itruediv__"],
                operator.itruediv,
            ),
            operator.floordiv: (
                ["__floordiv__", "__rfloordiv__", "__ifloordiv__"],
                operator.ifloordiv,
            ),
            operator.mod: (["__mod__", "__rmod__", "__imod__"], operator.imod),
            pow: (["__pow__", "__rpow__", "__ipow__"], operator.ipow),
            operator.pow: (["__pow__", "__rpow__", "__ipow__"], operator.ipow),
            operator.lshift: (
                ["__lshift__", "__rlshift__", "__ilshift__"],
                operator.ilshift,
            ),
            operator.rshift: (
                ["__rshift__", "__rrshift__", "__irshift__"],
                operator.irshift,
            ),
            # NB: The follow binary operators are not supported for now, since the
            # corresponding magic methods aren't defined on SymInt / SymFloat:
            # operator.matmul
            # divmod
            # operator.and_
            # operator.or_
            # operator.xor
        }
        return fns

    @staticmethod
    @functools.lru_cache(None)
    def _binop_handlers():
        # Multiple dispatch mechanism defining custom binop behavior for certain type
        # combinations. Handlers are attempted in order, and will be used if the type checks
        # match. They are expected to have the signature:
        # fn(tx, arg0: VariableTracker, arg1: VariableTracker, options) -> VariableTracker

        # Override table contains: op_fn -> [list of handlers]
        op_handlers = {}
        for (
            op,
            (magic_method_names, in_place_op),
        ) in BuiltinVariable._binops().items():
            op_handlers[op] = []
            op_handlers[in_place_op] = []

            forward_name, reverse_name, inplace_name = magic_method_names

            # User-defined args (highest precedence)
            def user_defined_handler(
                tx,
                a,
                b,
                options,
                forward_name=forward_name,
                reverse_name=reverse_name,
            ):
                # Manually handle reversing logic if needed (e.g. call __radd__)

                # TODO: If we expand this to handle tensor args, we need to manually
                # handle cases like this:
                #
                # class A(int):
                #     def __radd__(self, other):
                #         print("woof")
                # torch.randn(3) + A(3)
                #
                # In this example, A.__radd__() is not called -> nothing is printed, because
                # Tensor.__add__ only does a subtype test against int, ignoring the subclass.
                # To be fully correct, we should not call A.__radd__() here, and there may be
                # other cases to reason about and add exceptions for.
                if isinstance(a, UserDefinedVariable):
                    return a.call_method(tx, forward_name, [b], {})
                else:
                    return b.call_method(tx, reverse_name, [a], {})

            op_handlers[op].append(
                ((UserDefinedVariable, VariableTracker), user_defined_handler)
            )
            op_handlers[op].append(
                ((VariableTracker, UserDefinedVariable), user_defined_handler)
            )

            def user_defined_inplace_handler(
                tx, a, b, options, forward_name=inplace_name
            ):
                return a.call_method(tx, forward_name, [b], {})

            op_handlers[in_place_op].append(
                ((UserDefinedVariable, VariableTracker), user_defined_inplace_handler)
            )
            op_handlers[in_place_op].append(
                ((VariableTracker, UserDefinedVariable), user_defined_inplace_handler)
            )

            # Dynamic shape args
            def dynamic_handler(tx, a, b, options, fn=op):
                from .builder import wrap_fx_proxy

                return wrap_fx_proxy(
                    tx,
                    tx.output.create_proxy(
                        "call_function", fn, *proxy_args_kwargs([a, b], {})
                    ),
                    **options,
                )

            op_handlers[op].append(
                ((SymNodeVariable, VariableTracker), dynamic_handler)
            )
            op_handlers[op].append(
                ((VariableTracker, SymNodeVariable), dynamic_handler)
            )

            # NB: Prefer out-of-place op when calling in-place op to generate valid graph
            op_handlers[in_place_op].append(
                ((SymNodeVariable, VariableTracker), dynamic_handler)
            )
            op_handlers[in_place_op].append(
                ((VariableTracker, SymNodeVariable), dynamic_handler)
            )

        # Special cases - lower precedence but still prefer these over constant folding

        # List-like addition (e.g. [1, 2] + [3, 4])
        def tuple_add_handler(tx, a, b, options):
            return TupleVariable(a.items + list(b.unpack_var_sequence(tx)), **options)

        def size_add_handler(tx, a, b, options):
            return SizeVariable(a.items + list(b.unpack_var_sequence(tx)), **options)

        list_like_addition_handlers = [
            # NB: Prefer the tuple-specific logic over base logic because of
            # some SizeVariable weirdness. Specifically, the tuple-specific logic
            # drops the subclass type (e.g. SizeVariable) and returns TupleVariables.
            (
                (SizeVariable, SizeVariable),
                size_add_handler,
            ),
            (
                (TupleVariable, TupleVariable),
                tuple_add_handler,
            ),
            (
                (TupleVariable, ConstantVariable),
                tuple_add_handler,
            ),
            (
                (ConstantVariable, TupleVariable),
                lambda tx, a, b, options: TupleVariable(
                    list(a.unpack_var_sequence(tx)) + b.items, **options
                ),
            ),
            (
                (BaseListVariable, BaseListVariable),
                lambda tx, a, b, options: type(a)(a.items + b.items, **options),
            ),
        ]
        op_handlers[operator.add].extend(list_like_addition_handlers)

        def list_iadd_handler(tx, a, b, _):
            if not a.mutable_local or not b.has_unpack_var_sequence(tx):
                # Handler doesn't apply
                return None

            seq = b.unpack_var_sequence(tx)
            tx.output.side_effects.mutation(a)
            a.items.extend(seq)
            return a

        list_like_iadd_handlers = [
            (
                (ListVariable, VariableTracker),
                list_iadd_handler,
            ),
            (
                (TupleVariable, TupleVariable),
                tuple_add_handler,
            ),
            (
                (TupleVariable, ConstantVariable),
                tuple_add_handler,
            ),
        ]
        op_handlers[operator.iadd].extend(list_like_iadd_handlers)

        # List-like expansion (e.g. [1, 2, 3] * 3)
        def expand_list_like(tx, lst, const, options):
            return lst.__class__(
                items=lst.items * const.as_python_constant(),
                mutable_local=MutableLocal(),
                **options,
            )

        list_like_expansion_handlers = [
            ((ListVariable, ConstantVariable), expand_list_like),
            ((TupleVariable, ConstantVariable), expand_list_like),
            (
                (ConstantVariable, ListVariable),
                lambda tx, a, b, options: expand_list_like(tx, b, a, options),
            ),
            (
                (ConstantVariable, TupleVariable),
                lambda tx, a, b, options: expand_list_like(tx, b, a, options),
            ),
        ]
        op_handlers[operator.mul].extend(list_like_expansion_handlers)

        return op_handlers

    @staticmethod
    def _find_binop_handler(op, a, b):
        handlers = BuiltinVariable._binop_handlers()
        if op not in handlers:
            return None

        # Return first handler that matches the type checks
        for (type1, type2), handler in handlers[op]:
            if isinstance(a, type1) and isinstance(b, type2):
                return handler

        return None

    def can_insert_in_graph(self):
        return self.fn in self._fx_graph_functions()

    def __init__(self, fn, **kwargs):
        super().__init__(**kwargs)
        self.fn = fn

    def __str__(self):
        if self.fn is None:
            name = "None"
        else:
            name = self.fn.__name__

        return f"{self.__class__.__name__}({name})"

    def python_type(self):
        return type(self.fn)

    def as_python_constant(self):
        return self.fn

    def as_proxy(self):
        DTYPE = {
            bool: torch.bool,
            int: torch.int64,
            float: torch.float64,
        }
        if self.fn in DTYPE:
            return DTYPE[self.fn]
        return super().as_proxy()

    def reconstruct(self, codegen):
        name = self.fn.__name__
        assert self.fn.__module__ == "builtins"
        assert name not in codegen.tx.f_globals, "shadowed global"
        return [codegen.create_load_global(name, False, add=True)]

    def constant_args(self, *args, **kwargs):
        return check_constant_args(args, kwargs)

    def tensor_args(self, *args, **kwargs):
        return any(
            isinstance(i, variables.TensorVariable)
            for i in itertools.chain(args, kwargs.values())
        ) and not any(
            isinstance(i, variables.GetAttrVariable)
            for i in itertools.chain(args, kwargs.values())
        )

    def unspec_python_args(self, *args, **kwargs):
        return check_unspec_python_args(args, kwargs)

    @staticmethod
    def unwrap_unspec_args_kwargs(args, kwargs):
        return [x.as_python_constant() for x in args], {
            k: v.as_python_constant() for k, v in kwargs.items()
        }

    def call_function(
        self, tx, args: "List[VariableTracker]", kwargs: "Dict[str, VariableTracker]"
    ) -> "VariableTracker":
        from . import UserFunctionVariable
        from .builder import wrap_fx_proxy, wrap_fx_proxy_cls

        args = [v.realize() for v in args]
        kwargs = {k: v.realize() for k, v in kwargs.items()}
        constant_args = check_constant_args(args, kwargs)
        tensor_args = self.tensor_args(*args, **kwargs)
        unspec_python_args = self.unspec_python_args(*args, **kwargs)
        has_constant_handler = self.can_constant_fold_through() and (
            constant_args or unspec_python_args
        )
        assert isinstance(args, (list, tuple))
        assert isinstance(kwargs, dict)

        # args[0] is list and args[1] is unspec
        if self.fn is operator.getitem and not isinstance(
            args[0], variables.TensorVariable
        ):
            tensor_args = False

        if (
            self.can_insert_in_graph()
            and tensor_args
            and not (
                self.fn is operator.getitem
                and isinstance(args[0], ConstDictVariable)
                and isinstance(args[1], variables.TensorVariable)
            )
        ):
            try:
                fn = self.fn

                if self.fn in IN_PLACE_DESUGARING_MAP and isinstance(
                    args[0], variables.ConstantVariable
                ):
                    # In-place operators like += usually mustate tensor
                    # values, but in the edge case of immutable values they
                    # re-bind the variable.
                    #
                    # The easiest way to keep the graph consistent in this
                    # scenario is to de-sugar eagerly.
                    fn, args = IN_PLACE_DESUGARING_MAP[self.fn], [args[0], args[1]]

                if self.fn is operator.getitem and isinstance(args[1], SymNodeVariable):
                    # Standard indexing will force specialization due to
                    # __index__.  Rewrite as a regular torch op which will
                    # trace fine
                    fn, args = torch.select, [
                        args[0],
                        variables.ConstantVariable.create(0),
                        args[1],
                    ]

                # Interaction between ndarray and tensors:
                #   We prefer the tensor op whenever there are tensors involved
                if check_numpy_ndarray_args(args, kwargs) and not any(
                    type(arg) == variables.TensorVariable for arg in args
                ):
                    proxy = tx.output.create_proxy(
                        "call_function",
                        numpy_operator_wrapper(self.fn),
                        *proxy_args_kwargs(args, kwargs),
                    )

                    return wrap_fx_proxy_cls(variables.NumpyNdarrayVariable, tx, proxy)

                proxy = tx.output.create_proxy(
                    "call_function",
                    fn,
                    *proxy_args_kwargs(args, kwargs),
                )
                if any(isinstance(arg, FakeItemVariable) for arg in args):
                    return wrap_fx_proxy_cls(
                        FakeItemVariable,
                        tx,
                        proxy,
                    )
                elif self.unspec_python_args(*args, **kwargs):
                    _args, _kwargs = self.unwrap_unspec_args_kwargs(args, kwargs)
                    raw_value = self.fn(*_args, **_kwargs)

                    need_unwrap = any(
                        x.need_unwrap
                        for x in itertools.chain(args, kwargs.values())
                        if isinstance(x, variables.UnspecializedPythonVariable)
                    )

                    return wrap_fx_proxy_cls(
                        UnspecializedPythonVariable,
                        tx,
                        proxy,
                        raw_value=raw_value,
                        need_unwrap=need_unwrap,
                    )
                elif all(isinstance(x, SymNodeVariable) for x in args):
                    return SymNodeVariable.create(tx, proxy, None)
                else:
                    # Work around for vision_maskrcnn due to precision difference
                    # specialize the dividend when float divide by tensor
                    if self.fn is operator.truediv and isinstance(
                        args[0], variables.UnspecializedPythonVariable
                    ):
                        args[0] = args[0].convert_to_constant(tx)
                    return wrap_fx_proxy(tx, proxy)

            except NotImplementedError:
                unimplemented(f"partial tensor op: {self} {args} {kwargs}")

        # Handle cases like int(torch.seed())
        # Also handle sym_float to sym_int cases
        if self.fn in (int, float) and isinstance(
            args[0], (SymNodeVariable, variables.TensorVariable)
        ):
            if isinstance(args[0], variables.TensorVariable):
                item = args[0].call_method(tx, "item", [], {})
            else:
                item = args[0]
            fn_ = sym_int if self.fn is int else sym_float
            out = wrap_fx_proxy(
                tx=tx,
                proxy=tx.output.create_proxy(
                    "call_function",
                    fn_,
                    (item.as_proxy(),),
                    {},
                ),
            )
            return out

        # Handle `str` on a user defined function
        if self.fn == str and args and isinstance(args[0], (UserFunctionVariable)):
            return variables.ConstantVariable.create(value=str(args[0].fn))

        # Handle binary ops (e.g. __add__ / __radd__, __iadd__, etc.)
        # NB: Tensor args are handled above and not here
        if len(kwargs) == 0 and len(args) == 2:
            # Try to find a handler for the arg types; otherwise, fall through to constant handler
            binop_handler = BuiltinVariable._find_binop_handler(
                self.fn, args[0], args[1]
            )
            if binop_handler:
                res = binop_handler(tx, args[0], args[1], {})
                if res is not None:
                    return res

        handler = getattr(self, f"call_{self.fn.__name__}", None)
        if handler:
            try:
                inspect.signature(handler).bind(tx, *args, **kwargs)
            except TypeError as exc:
                if not has_constant_handler:
                    log.warning(
                        "incorrect arg count %s %s and no constant handler",
                        handler,
                        exc,
                    )
                handler = None

        if handler:
            try:
                result = handler(tx, *args, **kwargs)
                if result is not None:
                    return result
            except Unsupported as exc:
                if not has_constant_handler:
                    raise
                # Actually, we will handle this just fine
                exc.remove_from_stats()

        if has_constant_handler:
            # constant fold
            return variables.ConstantVariable.create(
                self.as_python_constant()(
                    *[x.as_python_constant() for x in args],
                    **{k: v.as_python_constant() for k, v in kwargs.items()},
                ),
            )

        if self.fn is round:
            if len(args) > 0 and isinstance(args[0], SymNodeVariable):
                raise UserError(
                    UserErrorType.STANDARD_LIBRARY,
                    "Calling round() on symbolic value is not supported. "
                    "You can use floor() to implement this functionality",
                    case_name="dynamic_shape_round",
                )
        return super().call_function(tx, args, kwargs)

    def call_method(
        self,
        tx,
        name,
        args: "List[VariableTracker]",
        kwargs: "Dict[str, VariableTracker]",
    ) -> "VariableTracker":
        if self.fn == dict and name == "fromkeys":
            return BuiltinVariable.call_custom_dict_fromkeys(tx, dict, *args, **kwargs)
        return super().call_method(tx, name, args, kwargs)

    def _call_min_max(self, tx, *args):
        if len(args) == 1 and args[0].has_unpack_var_sequence(tx):
            # expand iterable
            items = args[0].unpack_var_sequence(tx)
            return self._call_min_max_seq(tx, items)
        elif len(args) == 2:
            return self._call_min_max_binary(tx, args[0], args[1])
        elif len(args) > 2:
            return self._call_min_max_seq(tx, args)

    def _call_min_max_seq(self, tx, items):
        assert len(items) > 0
        if len(items) == 1:
            return items[0]

        return functools.reduce(functools.partial(self._call_min_max_binary, tx), items)

    def _call_min_max_binary(self, tx, a, b):
        if self.tensor_args(a, b):
            if not isinstance(a, variables.TensorVariable):
                a, b = b, a
            assert isinstance(a, variables.TensorVariable)

            # result of an item call is a scalar convert to a tensor
            if isinstance(a, FakeItemVariable):
                a = variables.TorchVariable(torch.tensor).call_function(tx, [a], {})

            # Dynamic input does not get resolved, rather, gets stored as call_function
            if isinstance(a, SymNodeVariable) or isinstance(b, SymNodeVariable):
                from .builder import wrap_fx_proxy_cls

                return wrap_fx_proxy_cls(
                    type(a),
                    tx=tx,
                    proxy=tx.output.create_proxy(
                        "call_function",
                        self.fn,
                        *proxy_args_kwargs([a, b], {}),
                    ),
                )

            # convert min/max to torch ops
            if b.is_python_constant():
                if isinstance(a, variables.NumpyNdarrayVariable):
                    import numpy as np

                    fn = variables.NumpyVariable(np.clip)
                else:
                    fn = variables.TorchVariable(torch.clamp)
                kwargs = {"min": b} if (self.fn is max) else {"max": b}
                result = fn.call_function(tx, [a], kwargs)
            else:
                if isinstance(a, variables.NumpyNdarrayVariable):
                    import numpy as np

                    fn = {max: np.maximum, min: np.minimum}[self.fn]
                    fn = variables.NumpyVariable(fn)
                else:
                    fn = {max: torch.maximum, min: torch.minimum}[self.fn]
                    fn = variables.TorchVariable(fn)
                result = fn.call_function(tx, [a, b], {})

            # return unspec if both a, b are unspec or const
            if all(
                isinstance(
                    i,
                    (
                        variables.UnspecializedPythonVariable,
                        variables.ConstantVariable,
                    ),
                )
                for i in [a, b]
            ):
                if any(isinstance(val, FakeItemVariable) for val in [a, b]):
                    return variables.FakeItemVariable.from_tensor_variable(result)

                if b.is_python_constant():
                    raw_b = b.as_python_constant()
                else:
                    raw_b = b.raw_value
                if self.fn is max:
                    raw_res = max(a.raw_value, raw_b)
                else:
                    raw_res = min(a.raw_value, raw_b)

                need_unwrap = any(
                    x.need_unwrap
                    for x in [a, b]
                    if isinstance(x, variables.UnspecializedPythonVariable)
                )
                return variables.UnspecializedPythonVariable.from_tensor_variable(
                    result, raw_res, need_unwrap
                )
            # otherwise return tensor
            else:
                return result
        elif isinstance(a, SymNodeVariable) or isinstance(b, SymNodeVariable):
            proxy = tx.output.create_proxy(
                "call_function", self.fn, *proxy_args_kwargs([a, b], {})
            )
            return SymNodeVariable.create(tx, proxy, None)

    call_min = _call_min_max
    call_max = _call_min_max

    def call_abs(self, tx, arg: "VariableTracker"):
        # Call arg.__abs__()
        abs_method = BuiltinVariable(getattr).call_function(
            tx, [arg, ConstantVariable.create("__abs__")], {}
        )
        return abs_method.call_function(tx, [], {})

    def call_range(self, tx, *args):
        if self.unspec_python_args(*args) or self.constant_args(*args):
            return variables.RangeVariable(args)
        elif self._dynamic_args(*args):
            args = [
                variables.ConstantVariable.create(guard_if_dyn(arg)) for arg in args
            ]
            return variables.RangeVariable(args)
        # None no-ops this handler and lets the driving function proceed
        return None

    def _dynamic_args(self, *args, **kwargs):
        return any(isinstance(x, SymNodeVariable) for x in args) or any(
            isinstance(x, SymNodeVariable) for x in kwargs.values()
        )

    def call_slice(self, tx, *args):
        return variables.SliceVariable(args)

    def _dyn_proxy(self, tx, *args, **kwargs):
        from .builder import wrap_fx_proxy

        return wrap_fx_proxy(
            tx,
            tx.output.create_proxy(
                "call_function", self.fn, *proxy_args_kwargs(args, kwargs)
            ),
        )

    def _call_iter_tuple_list(self, tx, obj=None, *args, **kwargs):
        if self._dynamic_args(*args, **kwargs):
            return self._dyn_proxy(tx, *args, **kwargs)

        if isinstance(obj, variables.IteratorVariable):
            # For non-list iterators, we will guard on vars that
            # determine the control flow
            return obj

        # TODO This should probably be treated as a dict, or dicts should also be treated here
        if self.fn == set:
            cls = SetVariable
        else:
            cls = variables.BaseListVariable.cls_for(self.fn)
        if obj is None:
            if cls is SetVariable:
                return cls(
                    [],
                    mutable_local=MutableLocal(),
                )
            else:
                return cls(
                    [],
                    mutable_local=MutableLocal(),
                )
        elif obj.has_unpack_var_sequence(tx):
            if obj.source and not is_constant_source(obj.source):
                if isinstance(obj, TupleIteratorVariable):
                    install_guard(
                        obj.source.make_guard(GuardBuilder.TUPLE_ITERATOR_LEN)
                    )
                else:
                    install_guard(obj.source.make_guard(GuardBuilder.LIST_LENGTH))
            if cls is SetVariable:
                return cls(
                    list(obj.unpack_var_sequence(tx)),
                    mutable_local=MutableLocal(),
                )

            return cls(
                list(obj.unpack_var_sequence(tx)),
                mutable_local=MutableLocal(),
            )

    call_iter = _call_iter_tuple_list
    call_tuple = _call_iter_tuple_list
    call_list = _call_iter_tuple_list
    call_set = _call_iter_tuple_list

    def call_callable(self, tx, arg):
        from .functions import BaseUserFunctionVariable

        if isinstance(
            arg, (variables.UserDefinedClassVariable, BaseUserFunctionVariable)
        ):
            return variables.ConstantVariable.create(True)

    def call_cast(self, _, *args, **kwargs):
        if len(args) == 2:
            return args[1]

        unimplemented(f"unsupported args to builtin cast(): {args} {kwargs}")

    def call_dict(self, tx, *args, **kwargs):
        return BuiltinVariable.call_custom_dict(tx, dict, *args, **kwargs)

    @staticmethod
    def call_custom_dict(tx, user_cls, *args, **kwargs):
        if not kwargs:
            if not args:
                args = ({},)
            assert len(args) == 1
            arg = args[0]
            if isinstance(arg, dict):
                return ConstDictVariable(arg, user_cls, mutable_local=MutableLocal())
            elif isinstance(arg, variables.ConstDictVariable):
                return arg.clone(user_cls=user_cls, mutable_local=MutableLocal())
            elif isinstance(
                arg,
                (
                    ListVariable,
                    TupleVariable,
                    ListIteratorVariable,
                ),
            ):
                items = user_cls()
                for x in arg.unpack_var_sequence(tx):
                    k, v = x.unpack_var_sequence(tx)
                    k = ConstDictVariable.get_key(k)
                    items.update({k: v})
                return ConstDictVariable(items, user_cls, mutable_local=MutableLocal())
        elif not args and kwargs:
            return variables.ConstDictVariable(
                dict(kwargs), user_cls=user_cls, mutable_local=MutableLocal()
            )
        unimplemented(f"{user_cls.__name__}(): {args} {kwargs}")

    @staticmethod
    def call_custom_dict_fromkeys(tx, user_cls, *args, **kwargs):
        assert user_cls in {dict, OrderedDict, defaultdict}
        if kwargs:
            # Only `OrderedDict.fromkeys` accepts `value` passed by keyword
            assert user_cls is OrderedDict
            assert len(args) == 1 and len(kwargs) == 1 and "value" in kwargs
            args = (*args, kwargs.pop("value"))
        if len(args) == 0:
            raise UserError(TypeError, "fromkeys expected at least 1 argument, got 0")
        if len(args) == 1:
            args = (*args, ConstantVariable.create(None))
        assert len(args) == 2
        arg, value = args
        DictVariableType = (
            ConstDictVariable if user_cls is not defaultdict else DefaultDictVariable
        )

        if isinstance(arg, dict):
            return DictVariableType(
                dict.fromkeys(arg, value), user_cls, mutable_local=MutableLocal()
            )
        elif isinstance(
            arg,
            (
                ConstDictVariable,
                ListVariable,
                TupleVariable,
                ListIteratorVariable,
            ),
        ):
            keys = [DictVariableType.get_key(x) for x in arg.unpack_var_sequence(tx)]
            return DictVariableType(
                dict.fromkeys(keys, value), user_cls, mutable_local=MutableLocal()
            )
        unimplemented(f"{user_cls.__name__}.fromkeys(): {args} {kwargs}")

    def call_zip(self, tx, *args, **kwargs):
        if kwargs:
            assert len(kwargs) == 1 and "strict" in kwargs
        if all(x.has_unpack_var_sequence(tx) for x in args):
            unpacked = [arg.unpack_var_sequence(tx) for arg in args]
            if kwargs.pop("strict", False) and len(unpacked) > 0:
                if not all(len(u) == len(unpacked[0]) for u in unpacked):
                    raise UserError(
                        ValueError,
                        "zip() has one argument of len differing from others",
                    )
            items = [variables.TupleVariable(list(item)) for item in zip(*unpacked)]
            return variables.TupleVariable(items)

    def call_enumerate(self, tx, *args):
        if len(args) == 1:
            start = 0
        else:
            assert len(args) == 2
            assert isinstance(args[1], variables.ConstantVariable)
            start = args[1].as_python_constant()
        if args[0].has_unpack_var_sequence(tx):
            items = [
                variables.TupleVariable(
                    [variables.ConstantVariable.create(idx), var],
                )
                for idx, var in enumerate(args[0].unpack_var_sequence(tx), start)
            ]
            return variables.TupleVariable(items)

    def call_len(self, tx, *args, **kwargs):
        return args[0].call_method(tx, "__len__", args[1:], kwargs)

    def call_getitem(self, tx, *args, **kwargs):
        return args[0].call_method(tx, "__getitem__", args[1:], kwargs)

    def call_isinstance(self, tx, arg, isinstance_type):
        arg_type = arg.python_type()

        isinstance_type = isinstance_type.as_python_constant()

        if isinstance(arg, variables.TensorVariable) and arg.dtype is not None:

            def _tensor_isinstance(tensor_var, tensor_type):
                def check_type(ty):
                    if ty not in tensortype_to_dtype:
                        return issubclass(arg.python_type(), ty)

                    dtypes = tensortype_to_dtype[ty]
                    return arg.dtype in dtypes

                if type(tensor_type) is tuple:
                    return any(check_type(ty) for ty in tensor_type)
                else:
                    return check_type(tensor_type)

            return variables.ConstantVariable.create(
                _tensor_isinstance(arg, isinstance_type)
            )
        # UserDefinedObject with C extensions can have torch.Tensor attributes,
        # so break graph.
        if isinstance(arg, variables.UserDefinedObjectVariable) and isinstance(
            arg.value, types.MemberDescriptorType
        ):
            unimplemented(
                f"isinstance called on UserDefinedClass {arg} {isinstance_type}"
            )
        # handle __instancecheck__ defined in user class
        if (
            isinstance(arg, variables.UserDefinedObjectVariable)
            and "__instancecheck__" in isinstance_type.__class__.__dict__
        ):
            return variables.ConstantVariable.create(
                isinstance_type.__class__.__instancecheck__(isinstance_type, arg.value)
            )

        try:
            val = issubclass(arg_type, isinstance_type)
        except TypeError:
            val = arg_type is isinstance_type
        return variables.ConstantVariable.create(val)

    def call_issubclass(self, tx, left_ty, right_ty):
        """Checks if first arg is subclass of right arg"""
        left_ty = left_ty.as_python_constant()
        right_ty = right_ty.as_python_constant()

        return variables.ConstantVariable(issubclass(left_ty, right_ty))

    def call_super(self, tx, a, b):
        return variables.SuperVariable(a, b)

    def call_next(self, tx, arg):
        if isinstance(
            arg, (variables.ListIteratorVariable, variables.IteratorVariable)
        ):
            val, next_iter = arg.next_variables(tx)
            return val
        elif isinstance(arg, variables.BaseListVariable):
            return arg.items[0]

    def call_hasattr(self, tx, obj, attr):
        if attr.is_python_constant():
            name = attr.as_python_constant()
            return obj.call_hasattr(tx, name)

    def call_map(self, tx, fn, seq):
        if seq.has_unpack_var_sequence(tx):
            items = [fn.call_function(tx, [x], {}) for x in seq.unpack_var_sequence(tx)]
            return variables.TupleVariable(items)

    def call_sum(self, tx, seq, **kwargs):
        # Special case for sum on tuple of floats and ints
        if (
            isinstance(seq, (variables.ListVariable, variables.TupleVariable))
            and all(
                isinstance(x, variables.ConstantVariable)
                and isinstance(x.value, (int, float))
                for x in seq.items
            )
            and not kwargs
        ):
            new_list = [x.value for x in seq.items]
            return variables.ConstantVariable.create(sum(new_list))
        if seq.has_unpack_var_sequence(tx):
            start = kwargs.pop(
                "start", variables.ConstantVariable.create(0)
            ).as_python_constant()
            assert not kwargs
            items = seq.unpack_var_sequence(tx)[start:]
            return BuiltinVariable(functools.reduce).call_function(
                tx,
                [
                    BuiltinVariable(operator.add),
                    variables.TupleVariable(items),
                    variables.ConstantVariable.create(0),
                ],
                {},
            )

    def call_reduce(self, tx, function, iterable, initializer=None):
        if iterable.has_unpack_var_sequence(tx):
            items = iterable.unpack_var_sequence(tx)
            if initializer is None:
                value, items = items[0], items[1:]
            else:
                value = initializer
            for element in items:
                value = function.call_function(tx, [value, element], {})
            return value

    def call_getattr(
        self, tx, obj: VariableTracker, name_var: VariableTracker, default=None
    ):
        from .. import trace_rules
        from . import (
            ConstantVariable,
            GetAttrVariable,
            PythonModuleVariable,
            TorchInGraphFunctionVariable,
            TorchVariable,
            UserFunctionVariable,
        )
        from .builder import SourcelessBuilder, VariableBuilder

        name = name_var.as_python_constant()

        if not name_var.is_python_constant():
            unimplemented("non-const getattr() name")

        if tx.output.side_effects.is_attribute_mutation(obj) and name != "grad":
            try:
                # re-read a pending side effect?
                return tx.output.side_effects.load_attr(obj, name)
            except KeyError:
                pass

        if default is not None:
            hasattr_var = self.call_hasattr(tx, obj, name_var)
            assert hasattr_var.as_python_constant() in (True, False)
            if not hasattr_var.as_python_constant():
                return default

        options = {}
        if obj.source:
            source = AttrSource(obj.source, name)
            options["source"] = source
        else:
            source = None

        if name == "__bases__":
            try:
                value = obj.as_python_constant()
                if isinstance(value, type):
                    bases = value.__bases__
                    if source is not None:
                        tuple_args = [
                            VariableBuilder(tx, GetItemSource(source, i))(b)
                            for i, b in enumerate(bases)
                        ]
                    else:
                        tuple_args = [SourcelessBuilder()(tx, b) for b in bases]

                    return variables.TupleVariable(tuple_args, **options)
            except NotImplementedError:
                pass

        if isinstance(obj, variables.NNModuleVariable):
            return obj.var_getattr(tx, name)
        elif isinstance(obj, variables.TensorVariable) and name == "grad":
            if source:
                # We are going to be raising this tensor as grapharg. So, ensure
                # that we have real grad value instead of fake tensor value.
                # Walk through the inputs of the subgraph and find if we already
                # have the original tensor stored in the graphargs.
                for grapharg in tx.output.graphargs:
                    if grapharg.source == source.base:
                        old_grad = grapharg.example.grad
                        new_grad = obj.as_proxy().node.meta["example_value"].grad

                        def _grad_changed(old, new):
                            if old is None or new is None:
                                return new is not old
                            try:
                                if old.shape != new.shape:
                                    return True
                                if old.stride() != new.stride():
                                    return True
                                return False
                            except TypeError as te:
                                # There is a rare edge case in which
                                # we seem to get symbol mismatches
                                # for jagged tensor comparison.
                                # See PYTORCH_TEST_WITH_DYNAMO=1 python test/test_nestedtensor.py
                                #   -k test_dropout_backward_layout_torch_jagged_cpu
                                unimplemented(str(te))

                        if _grad_changed(old_grad, new_grad):
                            if new_grad is not None:
                                grad_shape_specialized = [
                                    int(x) for x in new_grad.shape
                                ]
                                # We lazily update the grad on the example to its real state as tracked by fake tensor.
                                # This allocation is fine - it is just a hint. It will not make it to runtime, but it coerces
                                # the underlying value to always be correct.
                                grapharg.example.grad = torch.zeros(
                                    grad_shape_specialized, device=new_grad.device
                                )
                            else:
                                grapharg.example.grad = None
                        return VariableBuilder(tx, source)(grapharg.example.grad)

                return obj.dynamic_getattr(tx, name)
            else:
                example_value = obj.as_proxy().node.meta["example_value"]
                if example_value.grad is not None:
                    unimplemented("getattr on non-None grad - NYI")
                return ConstantVariable(None)
        elif isinstance(
            obj,
            (
                variables.TensorVariable,
                variables.NamedTupleVariable,
                variables.ConstantVariable,
                variables.UserDefinedClassVariable,
                variables.UserDefinedObjectVariable,
            ),
        ):
            try:
                return obj.var_getattr(tx, name)
            except NotImplementedError:
                return GetAttrVariable(obj, name, **options)
        elif isinstance(obj, TorchInGraphFunctionVariable):
            member = getattr(obj.value, name)
            if trace_rules.lookup(member) is not None:
                return trace_rules.lookup(member)(member, **options)
        elif isinstance(obj, TorchVariable):
            member = getattr(obj.value, name)
            if is_utils_checkpoint(member):
                options["source"] = source
                return build_checkpoint_variable(**options)
            elif trace_rules.lookup(member) is not None:
                return trace_rules.lookup(member)(member, **options)
            elif source is not None:
                return VariableBuilder(tx, source)(member)
            else:
                return SourcelessBuilder()(tx, member)
        elif isinstance(obj, (PythonModuleVariable, DummyModule)):
            member = obj.value.__dict__[name]

            if config.replay_record_enabled:
                tx.exec_recorder.record_module_access(obj.value, name, member)

            return VariableBuilder(tx, source)(member)
        elif istype(obj, UserFunctionVariable) and name in ("__name__", "__module__"):
            return ConstantVariable.create(getattr(obj.fn, name))
        else:
            try:
                return obj.var_getattr(tx, name)
            except NotImplementedError:
                return GetAttrVariable(obj, name, **options)

    def call_setattr(
        self, tx, obj: VariableTracker, name_var: VariableTracker, val: VariableTracker
    ):
        from .distributed import PlacementVariable

        if isinstance(
            obj,
            (
                variables.DataClassVariable,
                variables.CustomizedDictVariable,
                PlacementVariable,
            ),
        ):
            return obj.call_method(tx, "__setattr__", [name_var, val], {})
        elif (
            tx.output.side_effects.is_attribute_mutation(obj)
            and name_var.is_python_constant()
        ):
            name = name_var.as_python_constant()
            if isinstance(obj, variables.TensorVariable):
                from .builder import wrap_fx_proxy

                if name == "requires_grad":
                    # TODO(voz): Make it work properly
                    unimplemented(
                        "mutating requires_grad can introduce a new leaf from non-leaf or vice versa in "
                        "the middle of the graph, which aot_autograd does not currently know how to handle. "
                    )
                if name == "data":
                    # Remove the old reference in tracked fakes - if we don't do this
                    # new .data value size and shape differences will cause
                    # tracked fakes to produce incorrect guards. This is sound because the TensorVariable
                    # coming out of set_() below will be a new one, and get
                    # installed in tracked fakes.
                    to_remove = []
                    for tf in tx.output.tracked_fakes:
                        if tf.source == obj.source:
                            to_remove.append(tf)
                    for tf in to_remove:
                        tx.output.tracked_fakes.remove(tf)

                    # Step 1 - disable grads
                    with dynamo_disable_grad(tx), torch.no_grad():
                        # Step 2 - call `set_`
                        out = wrap_fx_proxy(
                            tx,
                            tx.output.create_proxy(
                                "call_function",
                                torch.Tensor.set_,
                                *proxy_args_kwargs([obj, val], {}),
                            ),
                        )

                    # Step 3 - drop the version counter - this is a step required to get
                    # .data setting to play correctly with the autograd engine.
                    # Esentially, dynamo is trying to faithful preserve the (absurd)
                    # behavior of .data= from eager mode
                    def _lower_version_count_by_1(x):
                        version = x._version
                        if version > 0:
                            version = version - 1
                        torch._C._autograd._unsafe_set_version_counter(x, version)
                        return x

                    tx.output.create_proxy(
                        "call_function",
                        _lower_version_count_by_1,
                        (out.as_proxy(),),
                        {},
                    )
                    _lower_version_count_by_1(obj.as_proxy().node.meta["example_value"])
                    # This handles options prop, guards and ends with a clone
                    # Step 4 - replace all reference to the current object with the new one
                    return out

            tx.output.side_effects.store_attr(obj, name, val)
            return val
        elif isinstance(obj, variables.UserDefinedObjectVariable):
            unimplemented(
                f"setattr(UserDefinedObjectVariable) {type(obj.value).__setattr__}"
            )
        elif isinstance(obj, variables.NNModuleVariable):
            if not tx.output.is_root_tracer():
                raise AttributeMutationError(
                    "Can't inplace modify module params/buffers inside HigherOrderOp"
                )
            if name_var.is_python_constant() and isinstance(
                val, variables.TensorVariable
            ):
                assigning_fake_val = get_fake_value(val.as_proxy().node, tx)

                try:
                    getattr_var = obj.var_getattr(tx, name_var.as_python_constant())
                except AttributeError:
                    getattr_var = None

                if isinstance(getattr_var, variables.TensorVariable):
                    # get_fake_val will get the same fake tensor
                    existing_fake_attr = get_fake_value(getattr_var.as_proxy().node, tx)

                    # same tensor identiy, setattr is a no-op
                    mod_setattr = inspect.getattr_static(obj.module_type, "__setattr__")
                    if (
                        existing_fake_attr is assigning_fake_val
                        and mod_setattr is torch.nn.Module.__setattr__
                    ):
                        return getattr_var

            obj.convert_to_unspecialized(tx)
        # FIXME (tmanlaibaatar) this is utter hack to unblock HuggingFace export
        # Export generally doesn't want to allow mutations on objects directly,
        # but we don't have good way to do this rn. For now, we make it an undefined
        # behaviour and just set attributes directly on the PretrainedConfig object
        # for now.
        elif isinstance(obj, variables.dicts.HFPretrainedConfigVariable) and tx.export:
            if name_var.is_python_constant() and isinstance(
                val, variables.ConstantVariable
            ):
                setattr(
                    obj.obj, name_var.as_python_constant(), val.as_python_constant()
                )
                return ConstantVariable(None)

    def call_delattr(self, tx, obj: VariableTracker, name_var: VariableTracker):
        return self.call_setattr(tx, obj, name_var, variables.DeletedVariable())

    def call_type(self, tx, obj: VariableTracker):
        from .builder import SourcelessBuilder, VariableBuilder

        try:
            py_type = obj.python_type()
        except NotImplementedError as error:
            raise UserError(
                UserErrorType.INVALID_INPUT,
                str(error),
                case_name="unknown_python_type",
            ) from None

        if obj.source is None:
            return SourcelessBuilder()(tx, py_type)
        else:
            return VariableBuilder(tx, TypeSource(obj.source))(py_type)

    def call_reversed(self, tx, obj: VariableTracker):
        if obj.has_unpack_var_sequence(tx):
            items = list(reversed(obj.unpack_var_sequence(tx)))
            return variables.TupleVariable(items)

    def call_sorted(self, tx, obj: VariableTracker, **kwargs):
        if (
            obj.has_unpack_var_sequence(tx)
            and not isinstance(obj, variables.TensorVariable)
            and all(x.is_python_constant() for x in obj.unpack_var_sequence(tx))
        ):
            function = kwargs.pop("key", None)
            reverse = kwargs.pop(
                "reverse", ConstantVariable.create(False)
            ).as_python_constant()
            assert len(kwargs) == 0
            if function:
                items = sorted(
                    obj.unpack_var_sequence(tx),
                    key=lambda x: function.call_function(
                        tx, [x], {}
                    ).as_python_constant(),
                    reverse=reverse,
                )
            else:
                items = sorted(
                    obj.unpack_var_sequence(tx),
                    key=lambda x: x.as_python_constant(),
                    reverse=reverse,
                )
            return variables.ListVariable(items)

    def call_chain(self, tx, *args):
        if all(obj.has_unpack_var_sequence(tx) for obj in args):
            items = []
            for obj in args:
                items.extend(obj.unpack_var_sequence(tx))
            return variables.TupleVariable(items)

    def call_islice(self, tx, iterable, *args):
        if iterable.has_unpack_var_sequence(tx) and all(
            x.is_python_constant() for x in args
        ):
            const_args = [x.as_python_constant() for x in args]
            items = iterable.unpack_var_sequence(tx)
            items = list(itertools.islice(items, *const_args))
            return variables.TupleVariable(items)

    # neg is a constant fold function, so we only get here if constant fold is not valid
    def call_neg(self, tx, a):
        if isinstance(a, SymNodeVariable):
            return SymNodeVariable.create(
                tx,
                (operator.neg)(a.as_proxy()),
                sym_num=None,
            )
        # None no-ops this handler and lets the driving function proceed
        return None

    def call_format(self, tx, _format_string, *args, **kwargs):
        format_string = _format_string.as_python_constant()
        return variables.StringFormatVariable.create(format_string, args, kwargs)

    def call_id(self, tx, *args):
        if len(args) > 0 and isinstance(args[0], variables.NNModuleVariable):
            nn_mod_variable = args[0]
            mod = tx.output.get_submodule(nn_mod_variable.module_key)
            return variables.ConstantVariable.create(id(mod))
        else:
            unimplemented(f"call_id with args {args}")

    def call_deepcopy(self, tx, x):
        unimplemented(f"copy.deepcopy {repr(x)}")

    def _comparison(self, tx, left, right):
        """
        Used to implement comparison operators for different types.
        For example, list1 < list2 is implemented differently from tensor1 < tensor2
        """
        from . import (
            BaseListVariable,
            ConstantVariable,
            NNModuleVariable,
            TensorVariable,
            UserDefinedObjectVariable,
            UserFunctionVariable,
        )
        from .lists import SizeVariable
        from .tensor import (
            supported_const_comparison_ops,
            supported_tensor_comparison_ops,
        )

        op = self.fn

        def _unimplemented():
            unimplemented(f"comparison {typestr(left)} {op} {typestr(right)}")

        if (
            all(
                isinstance(x, (NNModuleVariable, ConstantVariable))
                for x in [left, right]
            )
            and op in supported_const_comparison_ops.values()
        ):
            left = (
                tx.output.get_submodule(left.module_key)
                if isinstance(left, NNModuleVariable)
                else left.as_python_constant()
            )
            right = (
                tx.output.get_submodule(right.module_key)
                if isinstance(right, NNModuleVariable)
                else right.as_python_constant()
            )
            return ConstantVariable.create(op(left, right))

        if isinstance(left, UserFunctionVariable):
            if op not in supported_const_comparison_ops.values():
                _unimplemented()
            if not isinstance(right, UserFunctionVariable):
                _unimplemented()
            return ConstantVariable.create(op(left.fn, right.fn))

        # Note, we have a rare BaseListVariable subtype mismatch with valid comparison
        # x = torch.randn([3, 3])
        # x.size() == (3, 3) # True
        # (3, 3) == x.size() # True
        if isinstance(left, (SizeVariable, TupleVariable)) and isinstance(
            right, (TupleVariable, SizeVariable)
        ):
            return BaseListVariable.list_compare(tx, op, left, right)

        if isinstance(left, BaseListVariable):
            if not type(left) == type(right):  # Mismatch in BaseListVariable subclasses
                _unimplemented()
            return BaseListVariable.list_compare(tx, op, left, right)

        if isinstance(left, SetVariable):
            if not type(left) == type(right):  # Mismatch in BaseListVariable subclasses
                _unimplemented()
            return ConstantVariable.create(
                op(left._underlying_items, right._underlying_items)
            )

        if isinstance(left, TensorVariable) or isinstance(right, TensorVariable):
            from .builder import wrap_fx_proxy_cls

            if op is operator.is_ and isinstance(right, TensorVariable):
                return ConstantVariable.create(
                    id(extract_fake_example_value(left.as_proxy().node))
                    == id(extract_fake_example_value(right.as_proxy().node))
                )

            if op not in supported_tensor_comparison_ops.values():
                _unimplemented()
            if (
                isinstance(left, TensorVariable)
                and isinstance(right, TensorVariable)
                and (left.size and right.size) is not None
                and left.size != right.size
            ):
                try:
                    torch.broadcast_shapes(left.size, right.size)
                except RuntimeError:
                    # not broadcastable, can't be compared
                    _unimplemented()
            tensor_cls = left if isinstance(left, TensorVariable) else right
            return wrap_fx_proxy_cls(
                type(tensor_cls),  # handle Ndarrays and Tensors
                tx,
                proxy,
            )

        if isinstance(left, SymNodeVariable) or isinstance(right, SymNodeVariable):
            if op not in supported_tensor_comparison_ops.values():
                _unimplemented()

            proxy = tx.output.create_proxy(
                "call_function", op, (left.as_proxy(), right.as_proxy()), {}
            )
            return SymNodeVariable.create(
                tx,
                proxy,
                sym_num=None,
            )

        if isinstance(left, UserDefinedObjectVariable) and isinstance(
            right, UserDefinedObjectVariable
        ):
            return ConstantVariable.create(op(left.value, right.value))

        if (
            (isinstance(left, StreamVariable) and isinstance(right, StreamVariable))
            or (isinstance(left, EventVariable) and isinstance(right, EventVariable))
        ) and op is operator.eq:
            return ConstantVariable(op(left.value, right.value))

        if op.__name__ == "is_":
            # If the two objects are of different type, we can safely return False
            if type(left) is not type(right):
                return ConstantVariable.create(False)

        if isinstance(left, BuiltinVariable) and isinstance(right, BuiltinVariable):
            return ConstantVariable.create(op(left.fn, right.fn))

        _unimplemented()

    def call_and_(self, tx, a, b):
        # Rely on constant_handler
        if isinstance(a, ConstantVariable) and isinstance(b, ConstantVariable):
            return None
        if isinstance(a, (SymNodeVariable, ConstantVariable)) and isinstance(
            b, (SymNodeVariable, ConstantVariable)
        ):
            return SymNodeVariable.create(
                tx,
                tx.output.create_proxy(
                    "call_function", operator.and_, *proxy_args_kwargs([a, b], {})
                ),
                sym_num=None,
            )
        # None no-ops this handler and lets the driving function proceed
        return None

    def call_or_(self, tx, a, b):
        # Rely on constant_handler
        if isinstance(a, ConstantVariable) and isinstance(b, ConstantVariable):
            return None
        if isinstance(a, (SymNodeVariable, ConstantVariable)) and isinstance(
            b, (SymNodeVariable, ConstantVariable)
        ):
            return SymNodeVariable.create(
                tx,
                tx.output.create_proxy(
                    "call_function", operator.or_, *proxy_args_kwargs([a, b], {})
                ),
                sym_num=None,
            )
        # None no-ops this handler and lets the driving function proceed
        return None

    def call_not_(self, tx, a):
        if isinstance(a, SymNodeVariable):
            return SymNodeVariable.create(
                tx,
                tx.output.create_proxy(
                    "call_function", operator.not_, *proxy_args_kwargs([a], {})
                ),
                sym_num=None,
            )

        if isinstance(a, ListVariable):
            return ConstantVariable.create(len(a.items) == 0)

        return None

    call_eq = _comparison
    call_gt = _comparison
    call_lt = _comparison
    call_ge = _comparison
    call_le = _comparison
    call_ne = _comparison
    call_is_ = _comparison
    call_is_not = _comparison

    call_all = _polyfill_call_impl("all")
    call_any = _polyfill_call_impl("any")


@contextlib.contextmanager
def dynamo_disable_grad(tx):
    from . import GradModeVariable

    org_value = torch.is_grad_enabled()
    gmv = GradModeVariable.create(tx, False)
    try:
        gmv.enter(tx)
        yield
    finally:
        gmv.exit(tx)
