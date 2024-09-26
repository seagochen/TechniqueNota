- [0. 准备工作](#0-准备工作)
- [1. **删除非符号链接的文件**](#1-删除非符号链接的文件)
- [2. **创建符号链接**](#2-创建符号链接)
- [3. **重新运行 `ldconfig`**](#3-重新运行-ldconfig)


### 0. 准备工作

下载链接

```bash
wget https://developer.download.nvidia.com/compute/cudnn/redist/cudnn/linux-x86_64/cudnn-linux-x86_64-9.4.0.58_cuda11-archive.tar.xz
```

要解压你下载的 `cudnn-linux-x86_64-9.4.0.58_cuda11-archive.tar.xz` 文件，可以使用 `tar` 命令。你可以按以下步骤进行解压：

1. **进入下载文件的目录**（如果你不在那个目录的话）：
   ```bash
   cd ~/Download
   ```

2. **解压缩 `.tar.xz` 文件**：
   ```bash
   tar -xvf cudnn-linux-x86_64-9.4.0.58_cuda11-archive.tar.xz
   ```

   这个命令会解压文件并显示每个解压的文件名。

3. **查看解压后的文件**：
   执行完解压命令后，可以查看解压出的文件夹和内容：

   ```bash
   ls
   ```

通常，解压后的内容会包括 `include/`、`lib/` 等目录，你可以将这些文件按照 NVIDIA 的 cuDNN 安装说明复制到你的 CUDA 安装目录中，通常是 `/usr/local/cuda/`。

如果你需要将这些文件复制到 CUDA 目录，可以执行以下命令：

4. **复制 `include` 和 `lib` 文件到 CUDA 安装目录**：

   ```bash
   sudo cp cudnn-linux-x86_64-9.4.0.58_cuda11-archive/include/* /usr/local/cuda/include/
   sudo cp cudnn-linux-x86_64-9.4.0.58_cuda11-archive/lib/* /usr/local/cuda/lib64/
   ```

5. **刷新动态链接库缓存**：

   ```bash
   sudo ldconfig
   ```

这样就完成了 cuDNN 的安装。你可以通过检查 `/usr/local/cuda/include` 和 `/usr/local/cuda/lib64` 目录确认文件是否正确复制。

```bash
(base) vipuser@ubuntu22:~/Download$ sudo ldconfig
/sbin/ldconfig.real: /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_ops.so.9 不是符号链接

/sbin/ldconfig.real: /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_heuristic.so.9 不是符号链接

/sbin/ldconfig.real: /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_graph.so.9 不是符号链接

/sbin/ldconfig.real: /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_engines_runtime_compiled.so.9 不是符号链接

/sbin/ldconfig.real: /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_engines_precompiled.so.9 不是符号链接

/sbin/ldconfig.real: /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_cnn.so.9 不是符号链接

/sbin/ldconfig.real: /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_adv.so.9 不是符号链接

/sbin/ldconfig.real: /usr/local/cuda/targets/x86_64-linux/lib/libcudnn.so.9 不是符号链接
```

从错误信息可以看出，`ldconfig` 提示在 `/usr/local/cuda/targets/x86_64-linux/lib/` 目录中的某些 `libcudnn` 库文件不是符号链接。

在 CUDA 和 cuDNN 的安装过程中，通常库文件应该作为符号链接指向实际的库文件，以方便不同版本的管理。你可以手动创建这些符号链接来修复此问题。以下是步骤：

### 1. **删除非符号链接的文件**
首先，需要删除当前这些不是符号链接的库文件：

```bash
sudo rm /usr/local/cuda/targets/x86_64-linux/lib/libcudnn*.so.9
```

### 2. **创建符号链接**
现在，找到库的实际文件，并为它们创建符号链接。假设你安装的 cuDNN 版本是 `9.4.0.58`，可以执行以下命令来创建符号链接：

```bash
sudo ln -sf /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_ops.so.9.4.0 /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_ops.so.9
sudo ln -sf /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_heuristic.so.9.4.0 /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_heuristic.so.9
sudo ln -sf /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_graph.so.9.4.0 /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_graph.so.9
sudo ln -sf /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_engines_runtime_compiled.so.9.4.0 /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_engines_runtime_compiled.so.9
sudo ln -sf /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_engines_precompiled.so.9.4.0 /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_engines_precompiled.so.9
sudo ln -sf /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_cnn.so.9.4.0 /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_cnn.so.9
sudo ln -sf /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_adv.so.9.4.0 /usr/local/cuda/targets/x86_64-linux/lib/libcudnn_adv.so.9
sudo ln -sf /usr/local/cuda/targets/x86_64-linux/lib/libcudnn.so.9.4.0 /usr/local/cuda/targets/x86_64-linux/lib/libcudnn.so.9
```

### 3. **重新运行 `ldconfig`**

符号链接创建完成后，再次运行 `ldconfig` 来更新库缓存：

```bash
sudo ldconfig
```

这样应该可以解决符号链接的问题。如果你确认某些版本号或路径不同，请根据实际情况调整符号链接的目标路径。