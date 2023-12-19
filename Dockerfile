FROM python:3.10.12

RUN pip install --upgrade pip

WORKDIR /usr/src/app

RUN pip install numpy pandas matplotlib

COPY app/*.py .

ENTRYPOINT [ "python", "main.py"]