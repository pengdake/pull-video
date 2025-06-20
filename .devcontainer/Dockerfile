FROM docker.m.daocloud.io/python:3.10.12

RUN mv /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.bak && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list


RUN apt-get update && \
    apt-get install -y ffmpeg vim && \
    apt install -y chromium chromium-driver fonts-wqy-zenhei fonts-wqy-microhei


RUN pip install -U yt-dlp && \
    pip install ffmpeg-python pycryptodomex scrapy PySocks selenium-wire blinker==1.6.2 undetected-chromedriver -i https://pypi.tuna.tsinghua.edu.cn/simple
    
WORKDIR /app