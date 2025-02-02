# Dockerfile

```dockerfile
FROM ubuntu:22.04

# 设置环境变量，避免交互式安装时的提示
ENV DEBIAN_FRONTEND=noninteractive

# 更新包列表并安装所需的软件包
RUN apt-get update && apt-get install -y \
    net-tools \
    ssh \
    curl \
    wget \
    git \
    vim \
    unzip \
    zip \
    build-essential \
    make \
    cmake \
    autoconf \
    automake \
    libtool \
    pkg-config \
    libssl-dev \
    openssh-server \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 创建 Python 软链接
RUN ln -s /usr/bin/python3 /usr/bin/python

# 安装 Python 库
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
    jinja2 \
    numpy \
    setuptools \
    pyyaml \
    lxml \
    sympy

# 配置 SSH 服务
RUN mkdir /var/run/sshd && \
    echo 'root:123456' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# 创建 package 文件夹
RUN mkdir -p /root/package

# 安装 json (nlohmann)
COPY json.tar /root/package/json.tar
RUN cd /root/package && \
    tar -xvf json.tar && \
    cd json && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    rm -rf /root/package/json*

# 安装 cyclonedds
COPY cyclonedds.zip /root/package/cyclonedds.zip
RUN cd /root/package && \
    unzip cyclonedds.zip && \
    cd cyclonedds-master && \
    chmod +x build.sh && \
    ./build.sh && \
    rm -rf /root/package/cyclonedds*
    
# 安装grpc
RUN cd /root/package && \
	git clone -b v1.50.0 https://github.com/grpc/grpc.git && \
	cd grpc/  && \
	git submodule update --init && \
	mkdir -p cmake/build  && \
    cd cmake/build  && \
    cmake ../.. -DgRPC_INSTALL=ON  && \
    make -j$(nproc)  && \
    make install   && \
    rm -rf /root/package/grpc*

# 暴露 SSH 端口
EXPOSE 22

# 启动 SSH 服务
CMD ["/usr/sbin/sshd", "-D"]
```



如果由于网络问题，grpc无法正常安装，可以将上面dockerfile中的grpc部分内容修改为下面的方式：（ `grpc.zip` 见文件夹）

```dockerfile
COPY grpc.zip /root/package/grpc.zip
RUN cd /root/package && \
	unzip grpc.zip && \
	cd grpc && \
	mkdir -p cmake/build && \
	cd cmake/build && \
	cmake ../.. -DgRPC_INSTALL=ON && \
	make -j$(nproc) && \
	make install  && \
	rm -rf /root/package/grpc*
```



## Dockerfile使用方法

```shell
docker build -t micro-service:2.0 .
```



```shell
while ! docker build -t micro-service:2.0 .; do
    echo "retry..."
    sleep 2
done
```



## grpc打包流程

```shell
git clone -b v1.50.0 https://github.com/grpc/grpc.git
cd grpc/
git submodule update --init
cd ..
zip -r grpc.zip grpc/
```



# 代码下载

```dockerfile
# 下载git相关文件
RUN mkdir -p /root/micro_service
RUN cd /root/micro_service && \
	git clone -b experimental https://gitee.com/SpidermanW/server_compiling.git && \
	git clone https://github.com/yi-shui-a/ZT-Service-Registry.git
```



# 容器创建

```shell
# 三条命令只有暴露端口和容器名不同
docker run -d -p 2222:22 --name micro-service-test-1 micro-service:1.0
docker run -d -p 2223:22 --name micro-service-test-2 micro-service:1.0
docker run -d -p 2224:22 --name micro-service-test-3 micro-service:1.0

docker run -d -p 2225:22 --name micro-service-test-4 micro-service:2.0
```

