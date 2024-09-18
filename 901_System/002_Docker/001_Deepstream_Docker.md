
- [1. 安装Docker Desktop for Windows](#1-安装docker-desktop-for-windows)
- [2. 安装WSL 2](#2-安装wsl-2)
- [3. 安装NVIDIA Container Toolkit](#3-安装nvidia-container-toolkit)
- [4. 拉取并运行Nvidia Deepstream容器](#4-拉取并运行nvidia-deepstream容器)


# 1. 安装Docker Desktop for Windows

1. 从[Docker官网](https://www.docker.com/products/docker-desktop)下载Docker Desktop。
2. 运行安装程序并按照提示完成安装。
3. 在安装过程中确保启用了Windows的WSL 2（Windows Subsystem for Linux）。

# 2. 安装WSL 2

1. 打开PowerShell或命令提示符，运行以下命令来启用WSL和虚拟机平台：

    ```powershell
    wsl --install
    ```

2. 重新启动计算机以完成安装。
3. 安装Ubuntu或其他你喜欢的Linux发行版。可以从Microsoft Store中选择并安装，例如Ubuntu

    ```powershell
    wsl --install -d Ubuntu-22.04
    ```

# 3. 安装NVIDIA Container Toolkit

1. 确保你的Windows机器上安装了NVIDIA GPU驱动。
2. 打开WSL 2的Linux终端，配置生产环境库：

    ```sh
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    ```

3. 可选：配置库以使用实验包：

    ```sh
    sudo sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
    ```

4. 更新库中的包列表：

    ```sh
    sudo apt-get update
    ```

5. 安装NVIDIA Container Toolkit包：

    ```sh
    sudo apt-get install -y nvidia-container-toolkit
    ```


# 4. 拉取并运行Nvidia Deepstream容器

1. 打开WSL 2的Linux终端，拉取Nvidia Deepstream Docker镜像：

    ```sh
    docker pull nvcr.io/nvidia/deepstream:7.0-samples-multiarch
    ```

如果需要其他版本的，可以在下述网页中找到相关信息：

https://catalog.ngc.nvidia.com/orgs/nvidia/containers/deepstream-l4t

2. 下面是运行Deepstream Docker容器：

    ```sh
    docker run --gpus all -it --rm --net=host --privileged \
     -v /tmp/.X11-unix:/tmp/.X11-unix \
     -e DISPLAY=$DISPLAY \
     -w /opt/nvidia/deepstream/deepstream \
     nvcr.io/nvidia/deepstream:7.0-samples-multiarch
    ```
    
**Docker命令选项说明**

- `-it`: 以交互模式运行
- `--gpus all`: 使GPU可在容器中访问
- `--rm`: 退出时删除容器
- `--privileged`: 赋予容器对主机资源的访问权限
- `-v`: 指定挂载目录
- `-e DISPLAY=$DISPLAY`: 将显示变量传递给容器
