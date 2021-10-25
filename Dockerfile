FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

RUN true \
    && apt-get update \
    && apt-get -yq dist-upgrade \
    && apt-get install -yq --no-install-recommends \
    cron \
    curl \
    git \
    sudo \
    vim \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && true

RUN pip --no-cache-dir install \
    opencv-python \
    opencv-contrib-python \
    selenium \
    tqdm \
    webdriver-manager \
    && true

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb

## Set up scripts 

COPY ./ /workspace
WORKDIR /workspace
RUN chmod -R 777 /workspace
