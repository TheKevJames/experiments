FROM python:3.7.3-stretch

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt

COPY . /src
RUN pip install -e /src

CMD ["bash"]
