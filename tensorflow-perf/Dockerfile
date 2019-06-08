FROM python:3.7.3-stretch

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt

COPY MANIFEST.in /src
COPY g2p /src
COPY setup.py /src
RUN pip install /src

COPY . /src

CMD ["bash"]
