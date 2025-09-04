# Use the official Ubuntu 22.04 base image
FROM ubuntu:22.04
LABEL authors="Anees Al-Najjar"
# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
# Update package lists and install necessary packages for Python 3.10
# Python 3.10 is the default Python 3 version in Ubuntu 22.04
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the default Python 3 executable to python3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

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


CMD ["python3", "workflow_orchstration.py", "ipServerAddress=172.17.0.2", "connectionPort=5001","gendpoint=endpoint01.yaml"]

#python3 workflow_orchstration.py ipServerAddress=172.17.0.2 connectionPort=5001 gendpoint=endpoint01.yaml

# [4ua@wolf1 workflow_orchestrator_mService]$ docker build -f Dockerfile -t workfloworchestration:latest .

# [4ua@wolf1 workflow_orchestrator_mService]$ docker run -it workfloworchestration:latest
