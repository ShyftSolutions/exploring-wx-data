FROM jupyter/datascience-notebook:latest

COPY requirements.txt ./

RUN conda install -c conda-forge iris iris-grib && \
    pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org  -r requirements.txt
