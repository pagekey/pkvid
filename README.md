# PKVid

This is a Python package intended to help with automation of video editing.

## Installation Guide

This package is not meant to be installed in a regular Python environment. Instead, you must install it from the Python that is embedded in Blender.

1. Find the path to Blender's embedded Python.

```bash
cd $(dirname $(which blender))
ls
```

In my case, I was able to find it at the following path: `/opt/blender/blender-3.1.2-linux-x64/3.1/python/bin/python3.10`

Let's save this path for use in later steps.

```bash
# replace with the path you found:
export BLENDER_PYTHON=/opt/blender/blender-3.1.2-linux-x64/3.1/python/bin/python3.10
```

2. Ensure that pip is installed.

```bash
$BLENDER_PYTHON -m ensurepip
$BLENDER_PYTHON -m pip install --upgrade pip
```

3. Install pkvid from pypi.

```bash
$BLENDER_PYTHON -m pip install pkvid
```

## Development Install

Same process, but for the last step, run this instead:

```bash
$BLENDER_PYTHON -m pip install -e .
```

## Example Run Command

```bash
blender -b -P pkvid/__main__.py test/sample_config.json 
```
