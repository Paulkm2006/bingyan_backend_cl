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
- ⌛ Task6基础
- ⌛ Task6提高



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
- ✅ udp支持并发（直接使用sendto）
- ✅ 支持A AAAA MX CNAME TXT NS
- ✅ tcp查询
- ✅ 支持将缓存保存为文件（使用pickle处理）
- ✅ 支持重试、错误
- ❌ 负载均衡

