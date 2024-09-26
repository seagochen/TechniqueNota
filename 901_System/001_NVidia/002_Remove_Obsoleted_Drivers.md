
- [0. 问题表述](#0-问题表述)
- [1. 切换到较低版本内核](#1-切换到较低版本内核)
- [2. 清理旧的 NVIDIA 驱动](#2-清理旧的-nvidia-驱动)
- [3. 手动修复 DKMS 问题](#3-手动修复-dkms-问题)
- [4. 移除 `nouveau` 模块](#4-移除-nouveau-模块)
- [5. 检查日志](#5-检查日志)


### 0. 问题表述

```bash
(base) vipuser@ubuntu22:~/Download$ sudo apt-get -y install cuda
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
cuda 已经是最新版 (11.8.0-1)。
下列软件包是自动安装的并且现在不需要了：
  libwpe-1.0-1 libwpebackend-fdo-1.0-1
使用'sudo apt autoremove'来卸载它(它们)。
升级了 0 个软件包，新安装了 0 个软件包，要卸载 0 个软件包，有 6 个软件包未被升级。
有 8 个软件包没有被完全安装或卸载。
解压缩后会消耗 0 B 的额外空间。
正在设置 nvidia-dkms-520 (520.61.05-0ubuntu1) ...
update-initramfs: deferring update (trigger activated)

A modprobe blacklist file has been created at /etc/modprobe.d to prevent Nouveau
from loading. This can be reverted by deleting the following file:
/etc/modprobe.d/nvidia-graphics-drivers.conf

A new initrd image has also been created. To revert, please regenerate your
initrd by running the following command after deleting the modprobe.d file:
/usr/sbin/initramfs -u

*****************************************************************************
*** Reboot your computer and verify that the NVIDIA graphics driver can   ***
*** be loaded.                                                            ***
*****************************************************************************

INFO:Enable nvidia
DEBUG:Parsing /usr/share/ubuntu-drivers-common/quirks/dell_latitude
DEBUG:Parsing /usr/share/ubuntu-drivers-common/quirks/lenovo_thinkpad
DEBUG:Parsing /usr/share/ubuntu-drivers-common/quirks/put_your_quirks_here
Removing old nvidia-520.61.05 DKMS files...
Deleting module nvidia-520.61.05 completely from the DKMS tree.
Loading new nvidia-520.61.05 DKMS files...
Building for 6.5.0-28-generic
Building for architecture x86_64
Building initial module for 6.5.0-28-generic
ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/nvidia-kernel-source-520.0.crash'
Error! Bad return status for module build on kernel: 6.5.0-28-generic (x86_64)
Consult /var/lib/dkms/nvidia/520.61.05/build/make.log for more information.
dpkg: 处理软件包 nvidia-dkms-520 (--configure)时出错：
 已安装 nvidia-dkms-520 软件包 post-installation 脚本 子进程返回错误状态 10
dpkg: 依赖关系问题使得 cuda-drivers-520 的配置工作不能继续：
 cuda-drivers-520 依赖于 nvidia-dkms-520 (>= 520.61.05)；然而：
  软件包 nvidia-dkms-520 尚未配置。

dpkg: 处理软件包 cuda-drivers-520 (--configure)时出错：
 依赖关系问题 - 仍未被配置
dpkg: 依赖关系问题使得 cuda-drivers 的配置工作不能继续：
 cuda-drivers 依赖于 cuda-drivers-520 (= 520.61.05-1)；然而：
  软件包 cuda-drivers-520 尚未配置。

dpkg: 处理软件包 cuda-drivers (--configure)时出错：
 依赖关系问题 - 仍未被配置
dpkg: 依赖关系问题使得 nvidia-driver-520 的配置工作不能继续：
 nvidia-driver-520 依赖于 nvidia-dkms-520 (= 520.61.05-0ubuntu1)；然而：
  软件包 nvidia-dkms-520 尚未配置。
```

从错误日志中可以看到，主要问题出在 `nvidia-dkms-520` 模块的编译失败，这导致 CUDA 驱动程序以及相关组件未能正确安装。这个问题可能是由于以下原因引起的：

1. **内核与 NVIDIA 驱动的不兼容**：你当前的内核版本为 `6.5.0-28-generic`，而 `nvidia-dkms-520` 可能不支持该内核版本。你可以尝试切换到一个已知兼容的内核版本（如 `5.x` 系列），或等待 NVIDIA 驱动更新支持新内核。

2. **旧的 NVIDIA 模块残留**：可能旧的 NVIDIA 驱动残留导致 DKMS 模块冲突，需清理旧模块。

3. **DKMS 编译问题**：驱动的 `dkms` 模块编译时出错，可能是系统配置或文件损坏。

以下是几个可能的解决方案：

### 1. 切换到较低版本内核
你可以尝试安装并切换到较低版本的内核（如 `5.x` 系列），并重新安装驱动程序。首先，查看系统中安装的内核：

```bash
dpkg --list | grep linux-image
```

如果有较低版本的内核，可以通过以下命令切换：

```bash
sudo apt install linux-image-5.x.x-generic
sudo reboot
```

切换到较低版本内核后，重新尝试安装 CUDA。

### 2. 清理旧的 NVIDIA 驱动
首先卸载当前的 NVIDIA 驱动：

```bash
sudo apt-get purge nvidia-*
sudo apt-get autoremove
```

然后重新安装 CUDA 驱动程序：

```bash
sudo apt-get install cuda
```

### 3. 手动修复 DKMS 问题
如果问题出现在 `nvidia-dkms` 模块的编译，你可以尝试以下步骤：

```bash
sudo dkms remove nvidia/520.61.05 --all
sudo apt-get install --reinstall nvidia-dkms-520
```

查看日志 `/var/lib/dkms/nvidia/520.61.05/build/make.log`，以进一步了解错误详情。

### 4. 移除 `nouveau` 模块
确认 `nouveau` 显卡驱动已被禁用，可以通过以下步骤禁用它：

```bash
sudo nano /etc/modprobe.d/blacklist-nouveau.conf
```

确保文件内容如下：

```
blacklist nouveau
options nouveau modeset=0
```

然后执行以下命令并重启系统：

```bash
sudo update-initramfs -u
sudo reboot
```

重启后重新尝试安装 NVIDIA 驱动。

### 5. 检查日志
如果上述步骤仍然无法解决问题，可以查看 `/var/lib/dkms/nvidia/520.61.05/build/make.log`，以获取更多详细的错误信息，然后根据日志中的具体错误信息进行进一步的修复。

请尝试这些步骤，之后再重新安装 CUDA。