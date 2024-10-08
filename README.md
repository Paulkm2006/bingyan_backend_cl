# Cyber Lighthouse任务仓库

## 完成进度：
- ✅ Task1基础
- ⚠️ Task1提高
- ✅ Task2
- ✅ Task3基础
- ✅ Task3提高
- ✅ Task4基础
- ✅ Task4提高
- ✅ Task5基础
- ⚠️ Task5提高
- ✅ Task6基础
- ⚠️ Task6提高

[开发日志](diary.md)

## 文件说明

```bash
.
├── cache
│   └── __init__.py # dns查询缓存模块
├── client
│   ├── __init__.py # socket客户端模块init，空
│   ├── tcp.py # tcp客户端模块
│   └── udp.py # udp客户端模块
├── decoder
│   ├── __init__.py # dns查询解码模块init，空
│   ├── fetch_data.py # 发送查询模块，将请求转发到dns服务器，并返回结果
│   └── process_query.py # 解码查询模块，将二进制解码为人类可读
├── generator
│   └── generate.py # dns查询生成模块
├── server
│   ├── __init__.py # socket服务端模块init，空
│   ├── tcp.py # tcp服务端模块
│   └── udp.py # udp服务端模块
├── README.md # 本文件
├── cache.pickle # 查询缓存
├── client.py # socket客户端
├── diary.md # 开发日志
├── query.py # dns查询器，支持命令传参/cli使用
├── query_server.py # dns服务器
├── requirements.txt # 依赖库
├── server.py # socket服务端
├── server_conf.yaml # socket服务端配置
└── task2.md # task2
```


## Task1 基础
- ✅ 简单的client，可自定义协议
- ✅ 简单的server，通过更改配置文件改变监听端口、地址、类型

参考资料：
[socket使用](https://www.runoob.com/python3/python3-socket.html)
[调用其他文件中的class](https://stackoverflow.com/questions/4383571/importing-files-from-different-folder)


## Task1 提高
- ✅ 命令行支持
- ✅ 发送文件
- ❌ 并发处理
- ❌ 限制请求频率
- ❓ 支持POST/GET

参考资料：
[argparse使用](https://docs.python.org/zh-cn/3/library/argparse.html)


## Task2
详见 [task2.md](/task2.md)


## Task3 基础
- ✅ 支持解析与编码A
- ✅ 支持解析多个返回
- ✅ 支持存储不支持的type


## Task3 提高
- ✅ 支持解析与编码MX TXT NS CNAME AAAA


## Task4 基础
- ✅ 可指定服务器、端口
- ✅ 支持指定是否进行递归
- ✅ 解析输出
- ✅ 显示错误
- ✅ 支持命令行处理


## Task4 提高
- ✅ 支持AAAA MX CNAME NS TXT
- ✅ 超时、重试
- ✅ 支持tcp


## Task5 基础
- ✅ 接受请求并返回查询结果
- ✅ 可拒绝递归请求
- ✅ 内存cache
- ✅ cache根据ttl自动刷新
- ✅ 可指定不缓存
- ✅ 支持超时重试
- ✅ 可本地部署


## Task5 提高
- ✅ 支持A AAAA MX CNAME TXT NS
- ✅ tcp查询
- ✅ 支持将缓存保存为文件（使用pickle处理）
- ✅ 支持重试、错误
- ❌ 负载均衡
- ❌ 并发


## Task6 基础
- ✅ 支持递归查询
- ✅ 支持历史记录
- ✅ 支持输出差异
- ✅ 支持收藏
- ✅ 添加排行榜


## Task6 提高
- ✅添加cli
- ❌发送查询记录
- ❌共享收藏夹