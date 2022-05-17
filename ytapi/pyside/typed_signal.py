"""
This class exists to add type checking to Qt Signals and Slots,
to prevent inadvertently connecting signals to slots with a different signature.
This class should be preferred wherever we control both the signal and the slot.
Raw QT classes still need using for signals emerging from inbuilt QT objects.

Usage: 
To define a slot, decorate a method like so:
@TypedSlot
def foo(self: Any, a: int, b: bool) -> None:
    print(a if b else -a)

To define a signal, decorate a method stub like so:

@TypedSignal
def trigger(self: Any, a: int, b: bool) -> None:
    ...

To directly connect a signal to a matching slot, call
trigger.connect(foo)
MyPy will complain if the signatures of the methods 
do not match exactly.

To trigger the signal, call emit like so:
signal.emit(4, False)
_____________________________________
Known limitations:
In methods, the first argument must be "self: Any"
The call to emit is not type checked.
Direct calls to the slot are not type checked.
"""
import inspect
import re
from typing import (
    TYPE_CHECKING,
    Callable,
    Generic,
    List,
    overload,
    Protocol,
    TypeVar,
    Union,
)

from PySide6 import QtCore

FuncT = TypeVar("FuncT", bound=Callable)


if TYPE_CHECKING:

    # To support methods with up to N parameters, define N type vars.
    # For more parameters, just keep counting.
    TSelf = TypeVar("TSelf")
    T1 = TypeVar("T1", contravariant=True)
    T2 = TypeVar("T2", contravariant=True)
    T3 = TypeVar("T3", contravariant=True)
    T4 = TypeVar("T4", contravariant=True)
    T5 = TypeVar("T5", contravariant=True)
    T6 = TypeVar("T6", contravariant=True)
    T7 = TypeVar("T7", contravariant=True)
    T8 = TypeVar("T8", contravariant=True)
    T9 = TypeVar("T9", contravariant=True)
    TA = TypeVar("TA", contravariant=True)
    TB = TypeVar("TB", contravariant=True)
    TC = TypeVar("TC", contravariant=True)
    TD = TypeVar("TD", contravariant=True)
    TE = TypeVar("TE", contravariant=True)
    TF = TypeVar("TF", contravariant=True)

    R = TypeVar("R")

    class TypedSignalObj(Generic[FuncT]):
        def connect(
            self,
            slot: "TypedTriggerable[FuncT]",
            type: QtCore.Qt.ConnectionType = QtCore.Qt.ConnectionType.AutoConnection,
        ) -> None:
            ...

        def disconnect(self, slot: "TypedTriggerable[FuncT]") -> None:
            ...

        emit: FuncT

    @overload
    def TypedSignal(f: Callable[[TSelf], R]) -> TypedSignalObj[Callable[[], R]]:
        ...

    @overload
    def TypedSignal(f: Callable[[TSelf, T1], R]) -> TypedSignalObj[Callable[[T1], R]]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2], R]
    ) -> TypedSignalObj[Callable[[T1, T2], R]]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3], R]]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3, T4], R]]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3, T4, T5], R]]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3, T4, T5, T6], R],]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3, T4, T5, T6, T7], R],]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8], R],]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9], R],]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA], R],]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB], R],]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC], R]
    ) -> TypedSignalObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC], R],]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD], R]
    ) -> TypedSignalObj[
        Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD], R],
    ]:
        ...

    @overload
    def TypedSignal(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD, TE], R]
    ) -> TypedSignalObj[
        Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD, TE], R],
    ]:
        ...

    @overload
    def TypedSignal(
        f: Callable[
            [TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD, TE, TF], R
        ]
    ) -> TypedSignalObj[
        Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD, TE, TF], R],
    ]:
        ...

    def TypedSignal(f: Callable[..., R]) -> TypedSignalObj[Callable]:
        ...

    class TypedSlotObj(Generic[FuncT]):
        ...
        # To allow calling slots as functions, add
        # __call__: FuncT
        # But our current policy is that we avoid that.

    @overload
    def TypedSlot(f: Callable[[TSelf], R]) -> TypedSlotObj[Callable[[], R]]:
        ...

    @overload
    def TypedSlot(f: Callable[[TSelf, T1], R]) -> TypedSlotObj[Callable[[T1], R]]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2], R]
    ) -> TypedSlotObj[Callable[[T1, T2], R]]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3], R]]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3, T4], R]]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3, T4, T5], R]]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3, T4, T5, T6], R],]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3, T4, T5, T6, T7], R],]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8], R],]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9], R],]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA], R],]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB], R],]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC], R]
    ) -> TypedSlotObj[Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC], R],]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD], R]
    ) -> TypedSlotObj[
        Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD], R],
    ]:
        ...

    @overload
    def TypedSlot(
        f: Callable[[TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD, TE], R]
    ) -> TypedSlotObj[
        Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD, TE], R],
    ]:
        ...

    @overload
    def TypedSlot(
        f: Callable[
            [TSelf, T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD, TE, TF], R
        ]
    ) -> TypedSlotObj[
        Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, TA, TB, TC, TD, TE, TF], R],
    ]:
        ...

    def TypedSlot(f: Callable[..., R]) -> TypedSlotObj[Callable]:
        ...

    # Slight hack because signals (of the same signature) can be chained
    TypedTriggerable = Union[TypedSignalObj[FuncT], TypedSlotObj[FuncT]]

    class NoParamFunction(Protocol):
        # This represents something that matches a function `def foo() -> None`
        # And is incompatible with everything else, including things that take arguments.
        def __call__(self) -> None:
            ...

    SelfOnlySignalType = TypedSignalObj[NoParamFunction]
    SelfOnlySlotType = TypedTriggerable[NoParamFunction]

    # Workaround for QT bug
    BaseClassTypedSlot = TypedSlot

    class TypedConnectablePair(Generic[FuncT]):

        signal: TypedSignalObj[FuncT]
        slot: TypedTriggerable[FuncT]

        def __init__(
            self, signal: TypedSignalObj[FuncT], slot: TypedTriggerable[FuncT]
        ) -> None:
            ...


else:

    def _lookupType(ann, func_globals):
        if isinstance(ann, type):
            return ann
        if not isinstance(ann, str):
            return object
        if not re.match(r"\w+(\.\w+)*$", ann):
            # Check if it is in the form a.b.c.d
            # If it is not, it's probably a Union or some other generic.
            return object
        # Cython changes str annotations to unicode, so change it back
        if ann == "unicode":
            ann = "str"
        # Perform a restricted evaluation of expressions in the form a.b.c.d
        startName, *names = ann.split(".")
        t = func_globals.get(startName)
        if t is None:
            builtins = func_globals.get("__builtins__", {})
            if not isinstance(builtins, dict):
                builtins = builtins.__dict__
            t = builtins.get(startName)
        for name in names:
            if t is not None:
                t = getattr(t, name)
        return t if t is not None and isinstance(t, type) else object

    def _annotations_for_qt(f: Callable[..., None]) -> List[type]:
        sig = inspect.signature(f)
        sig_param_names = [p for p in sig.parameters]
        should_skip_first = len(sig_param_names) > 0 and sig_param_names[0] == "self"
        names_to_use = sig_param_names[1 if should_skip_first else 0 :]
        sig_annotations = [sig.parameters[p].annotation for p in names_to_use]
        func_globals = f.__globals__
        return [_lookupType(ann, func_globals) for ann in sig_annotations]

    def TypedSignal(f: FuncT):
        return QtCore.Signal(*_annotations_for_qt(f))

    def TypedSlot(f: FuncT):
        return QtCore.Slot(*_annotations_for_qt(f))(f)

    # Base classes must not have qt slot decorator because of qt bug
    def BaseClassTypedSlot(f: FuncT) -> FuncT:
        return f

    TypedTriggerable = Union[TypedSignal, TypedSlot]

    SelfOnlySlotType = TypedTriggerable
    SelfOnlySignalType = TypedSignal

    # These are sometimes used elsewhere but only in a Type Checking context,
    # so we just need them to not be undefined
    TypedSignalObj = None
    TypedSlotObj = None

    class TypedConnectablePair:
        def __init__(self, signal, slot):
            self.signal = signal
            self.slot = slot
