from typing import Tuple

import numpy as np
from numba import njit
from numba.types import bool_


@njit(inline='always')
def nbround(num: float, digit: int) -> float:
    return np.around(num, digit)


@njit(inline="always")
def nbvstack(tup: Tuple[np.ndarray, ...]) -> np.ndarray:
    return np.vstack(tup)


@njit(inline="always")
def nbisin(a: np.ndarray, b: np.ndarray) -> np.ndarray[bool]:
    
    assert a.ndim == 1 and b.ndim == 1, "2D arrays not supported."

    b_set = set(b)
    out_len = a.size
    out = np.empty(out_len, dtype=bool_)
    for i in range(out_len):
        out[i] = a[i] in b_set

    return out


@njit(inline="always")
def nbroll(a: np.ndarray, shift: int, axis: int) -> np.ndarray:
    assert axis >= 0, "Axis must be positive."

    if shift == 0:
        return a

    if a.ndim == 1:
        if shift > 0:
            return np.concat((a[-shift:], a[:-shift]))
        else:
            return np.concat((a[shift:], a[:shift]))

    # Numba throws index error without this
    assert a.ndim > 1

    shift = shift % a.shape[axis]

    out = np.empty_like(a)
    axis_len = a.shape[axis]

    for i in range(axis_len):
        new_index = (i + shift) % axis_len
        if axis == 0:
            out[new_index, :] = a[i, :]
        else:
            out[:, new_index] = a[:, i]

    return out