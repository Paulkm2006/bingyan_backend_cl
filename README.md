<<<<<<< HEAD
## Task2基础任务

### 1. DNS基础

#### 1. DNS的作用
>The goal of domain names is to provide a mechanism for naming resources
in such a way that the names are usable in different hosts, networks,
protocol families, internets, and administrative organizations

说人话：为不同资源、协议及网址提供统一的访问入口

再说直白一点：用一个容易记住的名称（域名）来代替复杂的IP地址等

#### 2. DNS查询流程

![](https://p.sda1.dev/19/7bf7620fd28fbefbffb9bc4d26f04e9d/image.png)

可以简单的概括为：
1. 客户端（如浏览器、应用）向本地解析器发送查询
2. 解析器先查询hosts（以及如果有的话，本地dns缓存）
3. 如果本地没有结果，就将请求发送到递归服务器（通常是运营商路由器自带的，当然也可以自己设置）
4. （如果没有缓存结果）递归服务器发送请求到根域名服务器(a-m.root-servers.net)
5. 根服务器返回顶级域名(TLD)运营商的服务器地址，继续递归发送请求
6. TLD服务器返回用户设置的权威服务器（如cloudflare）地址，继续递归请求对应ip
7. ip返回
8. 客户端建立请求

### 3.DNS服务器分类
1. 递归
- 用途：接收用户请求，递归查询直到得到ip
- 位置：公共提供商、ISP均有提供，甚至可以自建

2. 根服务器
- 用途：将请求转发到TLD服务器
- 位置：全球13个

3. TLD（顶级域）服务器
- 用途：管理TLD，将请求转发到权威服务器
- 位置：域名运营商（如.com位于Verizon）

4. 权威域名服务器
- 用途：存储DNS记录，返回IP
- 位置：依据用户自选

### 4. 报文格式
1. 标识位
![](https://p.sda1.dev/19/56784f5e1dacc7ceaba1540f81b6fc44/image.png)

Response：0标记请求，1标记应答

Opcode：操作码，0标准请求，1反向（ip查询域名），2查询服务器状态

Truncated：是否被截断

Recursion：指定是服务器（1）还是本地（0）来递归查询

![](https://p.sda1.dev/19/c2a435f098ec00b63b4045a8f454e02b/image.png)

1个查询，0个回应（代表客户端发送请求）

![](https://p.sda1.dev/19/4e5fbec5e9d30074e156e27ad987a2d8/image.png)
查询内容
Name：域名
Type：查询类型（1 A；28 AAAA；5 CNAME；15 MX）
Class：类（1为互联网）

## 2. dig使用
![](https://p.sda1.dev/19/afb1553170986ef47d41c9a07cf2ad60/image.png)
查询A记录（ipv4地址）

usage: `dig <@DNS server> <type> <options> domain`

`<@DNS server>`：覆盖本地设置的dns地址

`<type>`：查询类型（A AAAA MX CNAME等）

`<options>`：可选参数，如+tls（启用DoT）

## 3.Wireshark使用
![](https://p.sda1.dev/19/6b3a91393f145fde9297a8ac1791bae0/image.png)



### 参考资料：
[根服务器](https://www.iana.org/domains/root/servers)

[dns过程](https://www.cloudflare.com/learning/dns/what-is-a-dns-server/)

[dns数据包](https://fasionchan.com/network/dns/packet-format/)

[dns数据包2](https://cabulous.medium.com/dns-message-how-to-read-query-and-response-message-cfebcb4fe817)
=======
## Task1进阶分支

- [x] 命令行支持
- [x] 发送文件
- [x] 并发处理
- [ ] 限制请求频率
- [ ] 支持POST/GET

参考资料：
[argparse使用](https://docs.python.org/zh-cn/3/library/argparse.html)
>>>>>>> 7ed32548719e7eabc3478aa8b484d8d8788e98aa
