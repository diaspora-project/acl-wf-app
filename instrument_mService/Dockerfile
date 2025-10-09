 # Use the official Ubuntu 22.04 base image
FROM ubuntu:22.04
LABEL authors="Anees Al-Najjar"

# Set environment variables for Python version
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=US

# 1. Install Linux dependencies
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends\
    software-properties-common \
    git-core build-essential \
    wget \
    sudo \
    vim \
    apt-utils \
    net-tools \
    iptables \
    iputils-ping \
    iproute2 \
    ufw \
    tar \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    pkg-config \
    man-db \
    python-is-python3 && \
    rm -rf /var/lib/apt/lists/*

#####################################################################################################################
# 2. Download, extract, configure, and install Python from source
ENV PYTHON_VERSION=3.10.11
ENV PYTHON_URL=https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz
WORKDIR /usr/src

# Download and extract
RUN wget $PYTHON_URL -O python.tgz && \
    tar -xzf python.tgz && \
    rm python.tgz

WORKDIR /usr/src/Python-$PYTHON_VERSION
# Configure with optimizations and install to /usr/local
# 'altinstall' is used to avoid replacing the system's pre-installed python3 executable.
RUN ./configure --enable-optimizations --with-ensurepip=install --prefix=/usr/local && \
    make -j$(nproc) && \
    make install


#####################################################################################################################
# 3. Set the custom-built Python as the default using update-alternatives
# The executable path is /usr/local/bin/python3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.10 1 && \
    update-alternatives --install /usr/bin/python python /usr/local/bin/python3.10 1

## Set PATH to include the installation directory (though update-alternatives handles the main 'python' link)
ENV PATH="/usr/local/bin:$PATH"

##############################################################################################
# 4.  Create user '$USER' with no password and home directory
ENV USER=acl
RUN useradd -m -s /bin/bash $USER
# Set no password for '$USER'
RUN passwd -d $USER
# Add user to sudo group
RUN usermod -aG sudo $USER
# Configure passwordless sudo for '$USER'
RUN echo '$USER ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/$USER \
&& chmod 0440 /etc/sudoers.d/$USER
# Switch to the new user
USER $USER
# Set working directory
WORKDIR /home/$USER
#####################################################################################################
# 5. copy docker image files from the source and install python requirements.

COPY . .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

#CMD ["python3", "instrument_control.py", "ipServerAddress=192.168.100.10", "connectionPort=5001"]
#########################################################################################

# Comments
# 1- to build the docker image: cd acl-mini-app/instrument_mService && docker build -f Dockerfile -t acl-electrochemistry:latest .
# 2- to run the container with dockerfile CMD: docker run -it acl-electrochemistry:latest
# 3- to execute acl-electrochemistry service: python3 instrument_control.py ipServerAddress=<acl-electrochemistry container ip> connectionPort=5001
