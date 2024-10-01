要在Windows上通过命令行配置防火墙规则以打开指定端口（如1883端口）以便让Mosquitto服务能够正常使用，可以使用`netsh`命令。下面是具体步骤：

1. **以管理员身份打开命令提示符**：
   - 在Windows开始菜单中搜索`cmd`，然后右键点击“命令提示符”，选择“以管理员身份运行”。

2. **使用`netsh`命令添加防火墙规则**：

```cmd
netsh advfirewall firewall add rule name="Open Port 1883 for Mosquitto" protocol=TCP dir=in localport=1883 action=allow
```

这个命令的作用是添加一个名为“Open Port 1883 for Mosquitto”的防火墙规则，允许入站TCP连接通过本地端口1883。

### 解释
- `netsh advfirewall firewall add rule`: 添加防火墙规则的命令。
- `name="Open Port 1883 for Mosquitto"`: 规则的名称，可以自定义。
- `protocol=TCP`: 指定协议为TCP。
- `dir=in`: 指定规则适用于入站连接。
- `localport=1883`: 指定本地端口为1883。
- `action=allow`: 允许此规则的连接。

### 删除防火墙规则
如果需要删除此规则，可以使用以下命令：

```cmd
netsh advfirewall firewall delete rule name="Open Port 1883 for Mosquitto"
```

### 查看当前防火墙规则
可以使用以下命令查看当前所有的防火墙规则：

```cmd
netsh advfirewall firewall show rule name=all
```

或者查看特定端口的规则：

```cmd
netsh advfirewall firewall show rule name="Open Port 1883 for Mosquitto"
```

这样就可以通过命令行配置Windows防火墙规则，打开1883端口以支持Mosquitto服务的使用。