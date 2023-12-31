# This was a failed attempt at building Blender from source
# Leaving it here just in case it's needed later

FROM ubuntu:jammy-20231211.1 as builder

RUN apt update && apt install -y \
        build-essential \
        cmake \
        git \
        libboost-all-dev \
        libegl-dev \
        libdbus-1-dev \
        libembree-dev \
        libepoxy-dev \
        libfreetype6-dev \
        libjpeg-dev \
        libopenimageio-dev \
        libpng-dev \
        libpugixml-dev \
        libvulkan-dev \
        libwayland-dev \
        libx11-dev \
        libxxf86vm-dev \
        libxcursor-dev \
        libxi-dev \
        libxinerama-dev \
        libxrandr-dev \
        libxkbcommon-dev \
        libtbb-dev \
        libzstd-dev \
        linux-libc-dev \
        python3-dev \
        python3-numpy \
        subversion \
        wayland-protocols \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/blender-git

RUN git clone -b v3.6.7 --depth 1 https://projects.blender.org/blender/blender.git

# Add the libs recommended by blender compilation guide
WORKDIR /root/blender-git/lib
ENV LC_ALL=en_US.UTF-8
RUN svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_x86_64_glibc_228
RUN svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/tests

WORKDIR /root/blender-git/blender
RUN make update
# RUN git submodule update --init --recursive

# install a fake pass-thru sudo command
RUN echo '#!/bin/bash' > /usr/local/bin/sudo
RUN echo "exec \"\$@\"" >> /usr/local/bin/sudo
RUN chmod +x /usr/local/bin/sudo

# install packages
RUN ./build_files/build_environment/install_linux_packages.py && rm -rf /var/lib/apt/lists/*

WORKDIR /root/blender-git/cmake

RUN cmake ../blender -DWITH_PYTHON_INSTALL=OFF -DWITH_AUDASPACE=ON -DWITH_PYTHON_MODULE=ON -DWITH_MOD_OCEANSIM=OFF

RUN make -j16
