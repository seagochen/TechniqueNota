- [1. **下载 CUDA 仓库 Pin 文件**](#1-下载-cuda-仓库-pin-文件)
- [2. **下载 CUDA 本地安装程序**](#2-下载-cuda-本地安装程序)
- [3. **安装 CUDA 仓库**](#3-安装-cuda-仓库)
- [4. **复制密钥文件**](#4-复制密钥文件)
- [5. **更新包列表**](#5-更新包列表)
- [6. **安装 CUDA**](#6-安装-cuda)
- [7. **配置环境变量**](#7-配置环境变量)
- [8. **刷新 `.bashrc` 配置**](#8-刷新-bashrc-配置)
- [9. **验证 CUDA 安装**](#9-验证-cuda-安装)
- [10. **重启系统**](#10-重启系统)


### 1. **下载 CUDA 仓库 Pin 文件**
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
```

### 2. **下载 CUDA 本地安装程序**
```bash
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-ubuntu2204-11-8-local_11.8.0-520.61.05-1_amd64.deb
```

### 3. **安装 CUDA 仓库**
```bash
sudo dpkg -i cuda-repo-ubuntu2204-11-8-local_11.8.0-520.61.05-1_amd64.deb
```

### 4. **复制密钥文件**
```bash
sudo cp /var/cuda-repo-ubuntu2204-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
```

### 5. **更新包列表**
```bash
sudo apt-get update
```

### 6. **安装 CUDA**
```bash
sudo apt-get -y install cuda
```

### 7. **配置环境变量**
要使系统正确识别 CUDA 工具，需要将 CUDA 路径添加到环境变量。编辑 `.bashrc` 文件：

```bash
nano ~/.bashrc
```

在文件末尾添加以下两行内容：

```bash
export PATH=/usr/local/cuda-11.8/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

保存并退出编辑器。

### 8. **刷新 `.bashrc` 配置**

```bash
source ~/.bashrc
```

### 9. **验证 CUDA 安装**
执行以下命令以检查 CUDA 是否正确安装：

```bash
nvcc --version
```

你应该看到类似以下输出：

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Sep_21_11:15:35_PDT_2022
Cuda compilation tools, release 11.8, V11.8.89
```

### 10. **重启系统**

为了确保 CUDA 和 NVIDIA 驱动正常加载，重启系统：

```bash
sudo reboot
```

这样，系统就会加载 CUDA 11.8 环境，并且 `.bashrc` 配置也会生效。
