FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . ./
ARG DEBIAN_FRONTEND=noninteractive
ARG DEBCONF_NOWARNINGS="yes"

RUN python -m pip install --upgrade pip && \

EXPOSE 8000

CMD ["fastapi", "run", "--host=0.0.0.0", "--port=8000"]