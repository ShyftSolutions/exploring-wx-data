FROM jupyter/datascience-notebook:latest as base

COPY requirements.txt ./

RUN conda install -c conda-forge iris iris-grib && \
    pip install --no-cache-dir -r requirements.txt

FROM base as api

WORKDIR /app

COPY --chown=jovyan:jovyan fastapi/app/ /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]