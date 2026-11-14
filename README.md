![](res/wol.png)

因为有小登感兴趣我这个远程开机是怎么实现的，于是把它传到 GitHub 上来了。

<img width="1875" height="882" alt="图片" src="https://github.com/user-attachments/assets/1b443632-ed0d-4f0d-a645-89c44f28b66b" />

特性：

- 通过网页来走 Wake-on-LAN 唤醒局域网内指定设备（wol.py）
  - 没有身份认证鉴权
  - 推荐走 VPN
- 原神启动界面
- 命令行版本（wol-instant.py）
- 因为我的某些设备时间经常抽风，所以服务端与客户端时间差距过大会报错提醒
