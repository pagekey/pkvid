# PKVid

This is a Python package intended to help with automation of video editing.

See the docs site at [docs.pkvid.pagekey.io](https://docs.pkvid.pagekey.io/).

## Getting Started

1. Ensure blender is installed on your system and on your PATH as `blender`. If you can run `blender --version` in a terminal, you're good to go.

2. Install `pkvid`. You must have at least Python 3.9 for this.

```bash
pip install pkvid
```

3. Generate a new project:

```bash
pkvid new
```

4. You should now see `pkvid.yaml` in the current directory. Run:

```bash
pkvid render
```

5. Check the `build/` folder for your rendered project. You may also open the Blender project file to explore/debug.


## Building Blender with Sound in Docker (Advanced)

1. Build the Docker image. It will take a while. Final image will be huge, ~10-15 GB.

```bash
docker-compose build
```

## Developer Instructions

1. Install poetry.

```bash
pip install poetry
```

2. Install dependencies.

```bash
poetry install --with dev --with filters
```

3. Run the test suite:

```bash
poetry run pytest
```

4. Run integration test:

```bash
cd test/integration
poetry run pkvid render
```

## Old GUides

Do not follow these guides. I need to find a better place to put them, or just delete them.

These are old guides - leaving them here in case they're useful at some point.

### OLD Installation Guide 

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

### OLD Development Install

Same process, but for the last step, run this instead:

```bash
$BLENDER_PYTHON -m pip install -e .
```

### OLD Example Run Command

```bash
blender -b -P pkvid/__main__.py test/sample_config.json 
```


## Refernces

Building Blender from scratch:

- [Blender Community YouTube video](https://www.youtube.com/watch?v=WBAnd-r_x64)
- [Building on Ubuntu](https://wiki.blender.org/wiki/Building_Blender/Linux/Ubuntu)
- [Building bpy module](https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule)
