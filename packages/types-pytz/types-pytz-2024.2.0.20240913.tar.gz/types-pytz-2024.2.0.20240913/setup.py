from setuptools import setup

name = "types-pytz"
description = "Typing stubs for pytz"
long_description = '''
## Typing stubs for pytz

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pytz`](https://github.com/stub42/pytz) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pytz`.

This version of `types-pytz` aims to provide accurate annotations
for `pytz==2024.2`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pytz. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`d326c9bd424ad60c2b63c2ca1c5c1006c61c3562`](https://github.com/python/typeshed/commit/d326c9bd424ad60c2b63c2ca1c5c1006c61c3562) and was tested
with mypy 1.11.1, pyright 1.1.379, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="2024.2.0.20240913",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pytz.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pytz-stubs'],
      package_data={'pytz-stubs': ['__init__.pyi', 'exceptions.pyi', 'lazy.pyi', 'reference.pyi', 'tzfile.pyi', 'tzinfo.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
