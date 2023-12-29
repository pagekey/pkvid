# PKVid

This is a Python package intended to help with automation of video editing.

## Building bpy with audio support

The `bpy` package available on PyPI doesn't include audio support (unfortunately).

To fix this, I created a Docker image to build Blender from source.

The image is based on [these docs](https://wiki.blender.org/wiki/Building_Blender/Linux/Ubuntu) and [these too](https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule).

To build Blender using the image, run these commands:

```bash
docker build -t tmp .
# TODO command to copy the bpy whl out of the image
```
