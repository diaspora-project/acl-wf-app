# Use the official Ubuntu 22.04 base image
FROM ubuntu:22.04
LABEL authors="Anees Al-Najjar"
# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
ENV TZ=US
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update --fix-missing && apt-get install -y \
    software-properties-common \
    git-core build-essential \
    apt-utils \
    net-tools \
    iptables \
    iputils-ping \
    iproute2 \
    ufw

# Update package lists and install necessary packages for Python 3.10.11
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.10=3.10.11-1~22.04 \
    python3.10-distutils \
    python3.10-venv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && update-alternatives --set python3 /usr/bin/python3.10

COPY . .
# install python packages
RUN pip install --no-cache-dir -r requirements.txt

# Verify Python installation
RUN python3 --version




#RUN globus-compute-endpoint configure ornl_polaris_ep
#RUN globus-compute-endpoint start ornl_polaris_ep

#CMD ["python3", "instrument_control.py", "ipServerAddress=172.17.0.2", "connectionPort=5001"]




## Use the official Ubuntu 22.04 base image
#FROM ubuntu:22.04
#LABEL authors="Anees Al-Najjar"
## Set environment variables to prevent interactive prompts during package installation
#ENV DEBIAN_FRONTEND=noninteractive
## Update package lists and install necessary packages for Python 3.10
## Python 3.10 is the default Python 3 version in Ubuntu 22.04
#RUN apt-get update && \
#    apt-get install -y python3.10 python3-pip && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*
#
## Set the default Python 3 executable to python3.10
#RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
#COPY . .
#RUN pip install --no-cache-dir -r requirements.txt
#
#ENV TZ=US
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#RUN apt-get update --fix-missing && apt-get install -y \
#    software-properties-common \
#    git-core build-essential \
#    apt-utils \
#    net-tools \
#    iptables \
#    iputils-ping \
#    iproute2 \
#    ufw
#
#RUN globus-compute-endpoint configure ornl_polaris_ep
#RUN globus-compute-endpoint start ornl_polaris_ep
#
##CMD ["python3", "instrument_control.py", "ipServerAddress=172.17.0.2", "connectionPort=5001"]
