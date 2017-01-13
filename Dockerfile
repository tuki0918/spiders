FROM python:3.6-onbuild

# http://docs.opencv.org/3.2.0/d7/d9f/tutorial_linux_install.html
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
RUN apt-get install -y unzip

# numpy install
RUN python -m pip install numpy

# check cmake option
RUN cv_ver='3.2.0' build_dir="/tmp/opencv-build" cv_name="opencv-${cv_ver}" cv_con_name="opencv_contrib-${cv_ver}" \
    && mkdir -p ${build_dir} \
    && cd ${build_dir} \
    && wget https://github.com/Itseez/opencv/archive/${cv_ver}.zip -O ${cv_name}.zip \
    && wget https://github.com/Itseez/opencv_contrib/archive/${cv_ver}.zip -O ${cv_con_name}.zip \
    && unzip ${cv_name}.zip \
    && unzip ${cv_con_name}.zip \
    && mkdir -p ${cv_name}/cmake_build \
    && cd ${cv_name}/cmake_build \
    && cmake \
        -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=$(python -c "import sys; print(sys.prefix)") \
        -D INSTALL_C_EXAMPLES=OFF \
        -D BUILD_opencv_python3=ON \
        -D PYTHON_EXECUTABLE=$(which python) \
        -D PYTHON3_EXECUTABLE=$(which python3) \
        -D PYTHON3_PACKAGES_PATH=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
        -D OPENCV_EXTRA_MODULES_PATH=${build_dir}/${cv_con_name}/modules .. \
    && make -j4 \
    && make install \
    && rm -rf /tmp/opencv-build
