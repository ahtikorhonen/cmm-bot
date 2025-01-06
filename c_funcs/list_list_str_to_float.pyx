from libc.stdint cimport uint16_t
from libc.stdlib cimport strtod
from cpython.unicode cimport PyUnicode_AsUTF8

import numpy as np
cimport numpy as np


cpdef np.ndarray[np.double_t, ndim=2] parse(list[list[str]] data):
    """
    Parses a list of lists of strings into a NumPy array of floats
    :data (list[list[str]]): Input data, where each inner list contains strings
    :return (np.ndarray): NumPy array of shape (n, m) with dtype float64
    """
    cdef uint16_t                           i, j
    cdef uint16_t                           n = len(data)
    if n == 0:
        return np.empty((0, 0), dtype=np.float64)
    cdef uint16_t                           m = len(data[0])
    cdef np.ndarray[np.double_t, ndim=2]    result = np.empty((n, m), dtype=np.double)
    cdef list[str]                          row
    cdef double                             value
    cdef str                                item
    cdef const char*                        s
    cdef char*                              endptr

    for i in range(n):
        row = data[i]
        if len(row) != m:
            raise ValueError("All inner lists must have the same length.")

        for j in range(m):
            item = row[j]
            s = PyUnicode_AsUTF8(item)
            value = strtod(s, &endptr)
            if endptr == s:
                raise ValueError(f"Invalid float value: '{item}' at position ({i}, {j}).")
                
            result[i, j] = value

    return result