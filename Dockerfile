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
        python3-pip \
        subversion \
        wayland-protocols \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/blender-git

RUN git clone -b v3.6.7 --depth 1 https://projects.blender.org/blender/blender.git

# Add the libs recommended by blender compilation guide
WORKDIR /root/blender-git/lib
ENV LC_ALL=en_US.UTF-8
RUN svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_x86_64_glibc_228

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

# Fix error for numpy version wrong
# (compiled against API version 0x10 instead of 0xe)
RUN python3 -m pip install numpy --upgrade

# Configure build
RUN cmake ../blender \
    -DWITH_PYTHON_INSTALL=OFF \
    -DWITH_AUDASPACE=ON \
    -DWITH_PYTHON_MODULE=ON \
    -DWITH_MOD_OCEANSIM=OFF \
    -DWITH_MEM_JEMALLOC=OFF

# Build blender from source
RUN make -j16
RUN make install

# Create the whl file
RUN python3 ../blender/build_files/utils/make_bpy_wheel.py bin/

RUN python3 -m pip install ./bin/bpy-*.whl

# Start fresh, discard the (huge) build files
FROM ubuntu:jammy-20231211.1 as runner

RUN apt update && apt install -y \
        ffmpeg \
        libsm6 \
        libxkbcommon-x11-0 \
        libxext6 \
        libxfixes3 \
        libxi6 \
        libxxf86vm \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip


WORKDIR /app/
COPY requirements.txt pyproject.toml poetry.lock test /app/
COPY pkvid /app/pkvid

# Install requirements
RUN python3 -m pip install -r requirements.txt
# Install bpy
COPY --from=builder /root/blender-git/cmake/bin/bpy-*.whl /
RUN python3 -m pip install /bpy-*.whl
# Install pkvid
RUN python3 -m pip install -e .

CMD [ "pkvid" ]
