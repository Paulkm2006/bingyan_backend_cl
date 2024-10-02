# Cyber Lighthouse任务仓库

## 完成进度：
- [x] Task1基本 - 分支Task1-basic
- [x] Task1提高 - 分支Task1-adv
- [x] Task2基本 - 分支Task2-basic
- [x] Task2提高 - （？）



## Task1基础分支

- [x] 简单的client，可自定义协议
- [x] 简单的server，通过更改配置文件改变监听端口、地址、类型

参考资料：
[socket使用](https://www.runoob.com/python3/python3-socket.html)
[调用其他文件中的class](https://stackoverflow.com/questions/4383571/importing-files-from-different-folder)

## Task1进阶分支

- [x] 命令行支持
- [x] 发送文件
- [ ] 并发处理
- [ ] 限制请求频率
- [ ] 支持POST/GET

参考资料：
[argparse使用](https://docs.python.org/zh-cn/3/library/argparse.html)

## Task2
详见 [task2.md](/task2.md)


## Task3基础&提高

- [x] 支持解析与编码A MX TXT NS CNAME AAAA
- [x] 支持解析多个返回
- [x] 支持存储不支持的type


运行图片：

![](https://p.sda1.dev/19/884160efc69f227fd93bb063f0adf8e0/image.png)

## Task4 基础&提高

客户端 query.py
- [x] 可指定服务器、端口
- [x] 支持指定是否进行递归
- [x] 支持tcp
- [x] 解析输出
- [x] 显示错误
- [x] 支持A AAAA MX CNAME NS TXT
- [x] 超时、重试

## Task5 基础&提高

- [x] 接受请求并返回查询结果
- [x] 可拒绝递归请求
- [x] 内存cache
- [x] cache根据ttl自动刷新