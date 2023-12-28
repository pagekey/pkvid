# PKVid

This is a Python package intended to help with automation of video editing.

## Building bpy with audio support

The `bpy` package available on PyPI doesn't include audio support (unfortunately).

To fix this, clone Blender and build it yourself.

These instructions are for Ubuntu based on [these docs](https://wiki.blender.org/wiki/Building_Blender/Linux/Ubuntu) and [these too](https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule). There should probably be a Docker image to do this too (but for now, this is the best we've got).

```bash
# packages
sudo apt update
sudo apt install build-essential git subversion cmake libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev libegl-dev
sudo apt install libwayland-dev wayland-protocols libxkbcommon-dev libdbus-1-dev linux-libc-dev
# source cloning
mkdir ~/blender-git/lib -p
cd ~/blender-git
git clone --depth 1 https://projects.blender.org/blender/blender.git
cd ~/blender-git/lib
svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_x86_64_glibc_228
# edit config to create python module w/ audio support
cd ~/blender-git/blender
# perform build
make update
make
```
