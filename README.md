## Task3基础&提高

decoder.py用途：在127.0.0.1监听530端口处理dns请求，收到请求后解码并转发到8.8.8.8查询，随后输出结果

- [x] 支持解析A MX TXT NS CNAME
- [ ] 不支持AAAA - 本地无ipv6环境，无法测试
- [x] 支持解析多个返回

运行图片：

![](https://p.sda1.dev/19/884160efc69f227fd93bb063f0adf8e0/image.png)
