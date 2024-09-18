Mosquitto，也就是MQTT，是一种轻量级的IoT领域广泛使用的消息中间件。在Debian系Linux中，虽然可以使用`apt`安装MQTT

```sh
sudo apt install mosquitto mosquitto-clients
```

但是在某些情况，比如说IoT设备属于定制设备，或者离线情况下，那么编译mosquitto就显得很有必要了。

@[toc]
# 安装前准备

首先要确保下述依赖包已经安装上
* build-essential
* cmake
* libssl-dev
* libc-ares-dev
* uuid-dev
* xsltproc
* docbook-xsl

这些可以通过下载源码或者安装包来安装，不过如果能访问网络的情况下，也可以执行`apt`命令进行安装:

```sh
sudo apt update
sudo apt install -y git build-essential cmake libssl-dev libc-ares-dev uuid-dev xsltproc docbook-xsl
```

# 下载和编译

除了从Eclipse下载源码，还可以从Github下载MQTT的代码

 ```sh
 git clone https://github.com/eclipse/mosquitto.git
 cd mosquitto
 ```

然后进入工程目录，执行下述命令

```sh
mkdir build
cd build
cmake ..
```

CMAKE成功后，再执行编译命令

```sh
make
```

这个时候，在build的src目录下，有编译好的mosquitto主程序，在client目录下有发布和接受程序，另外在lib下有编译的库文件，以便于你进行二次开发。

此外，也可以执行

```sh
sudo make install
```

将MQTT安装到Linux系统中，如果那样的话，你还需要执行下述工作:

# 后续工作

```sh
sudo ldconfig
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

