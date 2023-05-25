FROM jupyter/datascience-notebook:latest

COPY requirements.txt ./

# RUN conda install -c conda-forge iris iris-grib && \
USER root
ENV UDUNITS2_XML_PATH=/usr/share/xml/udunits/udunits2.xml
RUN apt-get update \
    && apt-get -y install --no-install-recommends python3-dev python3-pip python3-tk libudunits2-dev libproj-dev proj-bin libgeos-dev libcunit1-dev python3-eccodes
RUN pip install --no-cache-dir -r requirements.txt
