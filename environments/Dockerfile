FROM ubuntu:20.04

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DEBIAN_FRONTEND=nointeractive

RUN apt-get update --fix-missing && \
    apt-get install -y \
    libocct-foundation-dev \
    libocct-modeling-algorithms-dev \
    libocct-modeling-data-dev \
    libocct-ocaf-dev \
    libocct-visualization-dev \
    libocct-data-exchange-dev \
    python3-all-dev \
    libboost-all-dev \
    wget \
    unzip \
    cmake \
    gcc \
    g++ \
    swig

ENV PYTHON_SITEPACKAGES /usr/local/lib/python3.8/dist-packages

ENV IFCOPENSHELL_URL https://s3.amazonaws.com/ifcopenshell-builds/ifcopenshell-python-38-master-8625aab-linux64.zip
RUN wget $IFCOPENSHELL_URL && \
    unzip ifcopenshell-python-* -d $PYTHON_SITEPACKAGES && rm -rf ifcopenshell-python*

ENV PYTHONOCC_URL https://github.com/tpaviot/pythonocc-core/archive/7.4.0.zip
RUN wget -q -O pythonocc-core.zip $PYTHONOCC_URL && \
    unzip pythonocc-core.zip && \
    rm -vf pythonocc-core.zip && \
    cd pythonocc-core-7.4.0 && mkdir build && cd build && \
    cmake -DOCE_INCLUDE_PATH=/usr/include/ -DOCE_LIB_PATH=/usr/lib/x86_64-linux-gnu/ .. && \
    make -j6 && make install


RUN echo $(python3 -c "import ifcopenshell.geom;print(ifcopenshell.geom.has_occ)")
