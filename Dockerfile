FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY requirements.dev.txt .
RUN pip install -r requirements.dev.txt
COPY project project
COPY create_tables.py .
RUN python create_tables.py
COPY load_fixtures.py .
COPY fixtures.json .
RUN python load_fixtures.py
COPY run.py .


CMD flask run -h 0.0.0.0 -p 25000