FROM docker.m.daocloud.io/python:3.10.12

# 设置镜像源
RUN mv /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.bak && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg vim \
        chromium chromium-driver \
        fonts-wqy-zenhei fonts-wqy-microhei \
        unzip wget curl xvfb && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录并复制代码
WORKDIR /pull-video
COPY . /pull-video

# 安装 Python 依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 下载 uBlock 插件
RUN mkdir -p /pull-video/extensions && \
    wget https://github.com/gorhill/uBlock/releases/download/1.64.0/uBlock0_1.64.0.chromium.zip && \
    unzip uBlock0_1.64.0.chromium.zip -d /pull-video/extensions && \
    rm uBlock0_1.64.0.chromium.zip

# 安装 Playwright 及浏览器依赖
RUN pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    playwright install --with-deps
