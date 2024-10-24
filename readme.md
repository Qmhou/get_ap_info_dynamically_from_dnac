get_ap_info_dynamically(ap_name) 函数通过调用 Cisco DNA Center API，
动态获取指定 AP 的详细信息，包括与 AP 连接的交换机信息。该函数的主要步骤如下：

加载配置：从 dnac.yaml 文件中加载 DNA Center 的相关配置信息（如 IP 地址、用户名、密码）。
获取认证 Token：通过 DNA Center API 进行身份认证，获取 x-auth-token，用于后续的 API 调用。
获取设备详情：使用 AP 名称查询设备详情，获取 AP 的 nwDeviceId。
获取丰富的设备信息：使用 nwDeviceId 调用设备丰富信息 API，提取与 AP 相关的详细信息，
包括 AP 名称（ap_name）、交换机名称（switch_name）、交换机 IP 地址（switch_ip）、连接端口（connect_port）。
返回 AP 信息：返回一个包含 AP 名称、交换机名称、交换机 IP 和连接端口的字典 ap_info，可用于后续操作，如 SSH 修复任务。

参数：
ap_name：触发日志中 AP 的名称，作为查询设备详情的依据。
返回值：
返回一个包含 ap_name, switch_name, switch_ip, connect_port 的字典，如果获取失败，返回 None。
示例：
```python
复制代码
ap_info = get_ap_info_dynamically("A1-320-3")
if ap_info:
    print(f"AP 名称: {ap_info['ap_name']}, 交换机名称: {ap_info['switch_name']}, 交换机 IP: {ap_info['switch_ip']}, 连接端口: {ap_info['connect_port']}")
else:
    print("无法获取 AP 信息")
这个函数在 AP 掉线时可以用来自动获取相关设备的信息，并替代手动查询或静态文件查询。
```

```yaml
dnac:
  ip: "1.1.1.1"
  username: "username"
  password: "password"

```