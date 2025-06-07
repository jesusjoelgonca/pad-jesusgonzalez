FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN mkdir -p actividades/actividad1/static/csv actividades/actividad1/static/db

RUN pip install --upgrade pip \
    && pip install -e . \
    && rm -rf /root/.cache/pip

ENV PYTHONPATH=/app/actividades/actividad1/src

ENTRYPOINT ["python", "-m"]

CMD ["actividades.actividad1.src.main"]