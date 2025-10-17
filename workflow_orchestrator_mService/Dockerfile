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
ENV USER=wf-orchestrator
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

RUN sudo chmod -R u+w /home/$USER/
#####################################################################################################
# 5. copy docker image files from the source and install python requirements.

COPY . .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
## add python3.10 path to $PATH
ENV PATH="/home/$USER/.local/bin:$PATH"

#######################################################################################################
# 6. install and configure Jupyter Notebook
# Install Jupyter Notebook as a root
USER root
RUN pip3 install --no-cache-dir jupyter notebook ipykernel

# Create a notebook configuration file
# This sets the server to listen on all interfaces (0.0.0.0)
RUN jupyter notebook --generate-config -y
RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.allow_origin = '*'" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py
# Make port 8888 available to the world outside this container
EXPOSE 8888
ENV PYTHONPATH=".local/lib/python3.10/site-packages/:$PYTHONPATH"

# Run Jupyter Notebook when the container launches
CMD ["jupyter", "notebook", "workflow_orchestration.ipynb", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

#########################################################################################
# Comments
# 1- to build the docker image: cd acl-mini-app/workflow_orchestrator_mService && docker build -f Dockerfile -t workfloworchestration:latest .
# 2- to run the container with dockerfile CMD: docker run -it workfloworchestration:latest bash
# 3- to execute worflow orchestrator
#    3-1. no Jupyter notebook:
#       - docker run -it workfloworchestration:latest bash
#       - python3 workflow_orchstration.py ipServerAddress=<acl-electrochemistry container ip> connectionPort=5001 gendpoint=endpoint03.yaml
#    3-2. with Jupyter notebook:
#       - docker run -p 8888:8888 workfloworchestration:latest # then find and open workflow_orchestration.ipynb
# 4- make sure you have the ip address of container running the instrument control module.
# 5- make sure you update endpoint03 file with globus token.
# Note: the workfloworchestration container at this point is just a forwarding service that takes the measurement from the acl-electrochemistry service and forward it with analytic code to the iv_inference_ep service