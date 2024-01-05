# PKVid

This is a Python package intended to help with automation of video editing.

## Getting Started

1. Build the Docker image. It will take a while. Final image will be huge, ~10-15 GB.

```bash
docker build -t pkvid .
```

2. Run pkvid.

```bash
docker run --rm pkvid
```

## Usage without Docker (Not Recommended)

These are old guides - leaving them here in case they're useful at some point.

### Installation Guide 

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

### Development Install

Same process, but for the last step, run this instead:

```bash
$BLENDER_PYTHON -m pip install -e .
```

### Example Run Command

```bash
blender -b -P pkvid/__main__.py test/sample_config.json 
```


## Refernces

Building Blender from scratch:

- [Blender Community YouTube video](https://www.youtube.com/watch?v=WBAnd-r_x64)
- [Building on Ubuntu](https://wiki.blender.org/wiki/Building_Blender/Linux/Ubuntu)
- [Building bpy module](https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule)
