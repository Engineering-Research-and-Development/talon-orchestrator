FROM python:3.10.6


RUN apt-get update && apt-get install -y libffi-dev


COPY ./requirements.txt .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /gunicorn-worker-tmp-dir

# gunicorn
CMD ["gunicorn", "--worker-tmp-dir", "/gunicorn-worker-tmp-dir", "--config", "gunicorn-cfg.py", "run:app"]