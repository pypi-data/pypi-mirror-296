from typing import Any, Protocol

import pyarrow as pa


# pa.Scalar is generic but its type constraint is not very useful
# because it cannot be inferred to anything besides Unknown.
# Instead, just define what we need from any "Scalar" structurally
# and avoid nominal typing altogether.
class Scalar(Protocol):
    @property
    def type(self) -> pa.DataType: ...

    def equals(self, other: "Scalar") -> bool: ...

    def as_py(self) -> Any: ...
