FROM python:3.7.3-stretch

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && \
    apt-get install -qy apt-transport-https && \
    wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB && \
    apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB && \
    rm GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB && \
    echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list && \
    apt-get update && \
    apt-get install -qy intel-mkl-2019.4-070

ENV OMP_NUM_THREADS 1

COPY tensorflow /src/tensorflow
COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt

COPY MANIFEST.in /src
COPY g2p /src/g2p
COPY setup.py /src
RUN pip install /src

COPY . /src

CMD ["bash"]
