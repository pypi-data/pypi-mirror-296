# OOFEM Post-Processing Python Package (oofempostpy)

`oofempostpy` is a simple Python package to parse OOFEM simulation logs and export extracted data to a CSV file.

## Generate oofempostpy

```
python setup.py sdist bdist_wheel
```

## Upload to PyPi

```
twine upload dist/*
```

## Installation

You can install the package by running:

```bash
pip install oofempostpy
