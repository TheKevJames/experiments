FROM python:3.7.2-windowsservercore

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && \
    apt-get install -qy apt-transport-https && \
    wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB && \
    apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB && \
    rm GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB && \
    echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list && \
    apt-get update && \
    apt-get install -qy intel-mkl-2019.4-070

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libcurl3-dev \
        libfreetype6-dev \
        libhdf5-serial-dev \
        libzmq3-dev \
        openjdk-8-jdk \
        openjdk-8-jre-headless \
        pkg-config \
        python3-dev \
        rsync \
        software-properties-common \
        swig \
        unzip \
        zip \
        zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip --no-cache-dir install --upgrade pip setuptools && \
    pip --no-cache-dir install \
        h5py \
        keras_applications \
        keras_preprocessing \
        matplotlib \
        mock \
        numpy \
        pandas \
        Pillow \
        scipy \
        sklearn

# See https://github.com/tensorflow/tensorflow/blob/v1.13.1/tensorflow/tools/docker/Dockerfile.devel#L59-L77
RUN echo "startup --batch" >>/etc/bazel.bazelrc
RUN echo "build --spawn_strategy=standalone --genrule_strategy=standalone" >>/etc/bazel.bazelrc
ENV BAZEL_VERSION 0.20.0
RUN mkdir /bazel && \
    cd /bazel && \
    curl -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36" -fSsL -O https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh && \
    curl -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36" -fSsL -o /bazel/LICENSE.txt https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE && \
    chmod +x bazel-*.sh && \
    ./bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh && \
    rm -f /bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh

RUN git clone --branch r1.13 --single-branch --depth 1 https://github.com/tensorflow/tensorflow.git /tensorflow

ENV PYTHON_BIN_PATH /usr/local/bin/python
ENV USE_DEFAULT_PYTHON_LIB_PATH 1

ENV TF_NEED_AWS 0
ENV TF_NEED_GCP 0
ENV TF_NEED_HDFS 0
ENV TF_NEED_KAFKA 0
ENV TF_SET_ANDROID_WORKSPACE 0
ENV TF_DOWNLOAD_CLANG 0

ENV TF_NEED_GDR 0
ENV TF_NEED_JEMALLOC 1
ENV TF_NEED_NGRAPH 0
ENV TF_NEED_VERBS 0
ENV TF_ENABLE_XLA 0

ENV TF_NEED_OPENCL_SYCL 0
ENV TF_NEED_COMPUTECPP 1
ENV TF_NEED_CUDA 0

ENV TF_NEED_MPI 0

ENV CC_OPT_FLAGS "-march=native -mavx2 -mfma -O3"

WORKDIR /tensorflow
RUN ./configure && \
    bazel build --config=opt --config=mkl //tensorflow/tools/pip_package:build_pip_package && \
    ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /pkg
