FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# COPY requirements.txt .
# RUN pip install -r requirements.txt
COPY pyproject.toml .
# COPY requirements.txt /app/requirements.txt
# COPY scripts/start.sh scripts/
# COPY src src/
# COPY conf conf/

# RUN chmod +x scripts/start.sh
COPY src src/

RUN pip install -e .

COPY . .
# COPY src /app/src
# COPY conf /app/conf

# RUN cd /app/