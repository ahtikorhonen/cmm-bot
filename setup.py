from setuptools import setup
from Cython.Build import cythonize

import numpy


setup(
    name="cmm-bot",
    ext_modules=cythonize("c_funcs/*.pyx"),
    include_dirs=[numpy.get_include()],
        options={
        "build_ext": {
            "build_lib": "c_funcs/build_lib"
        }
    },
)