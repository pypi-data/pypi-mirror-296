from collections.abc import Sequence
from typing import Union
from numbers import Number, Integral

try:
    from types import EllipsisType

    SingleDataIndexType = Union[Integral, slice, Sequence, EllipsisType]
except ImportError:
    SingleDataIndexType = Union[Integral, slice, Sequence]
from numpy.typing import ArrayLike

DataType = Union[bytes, Number, ArrayLike]
DataIndexType = Union[SingleDataIndexType, tuple[SingleDataIndexType]]
