from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        name="ai.heuristic",
        sources=["ai/heuristic.pyx"],
        include_dirs=[numpy.get_include()],
    )
]

setup(
    name="LOA AI",
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
)
