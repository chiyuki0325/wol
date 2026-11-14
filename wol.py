import socket
import struct
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from hashlib import sha256
import time
import math

app = FastAPI()

app.mount("/res", StaticFiles(directory="res"), name="res")

# index.html
@app.get("/")
async def index():
    return HTMLResponse(
        open("index.html", "r", encoding="utf-8").read()
    )


MAC_ADDRESS = "2A:02:6F:04:1E:EC"  # 替换为目标电脑的MAC地址
IP_ADDRESS = "192.168.3.255"  # 可选，可以指定目标IP或使用广播

def wake_on_lan(mac_address, ip_address=None, port=9):
    """
    Generated with DeepSeek
    发送WOL魔术包唤醒指定MAC地址的电脑

    参数:
        mac_address: 目标电脑的MAC地址(格式如'2A:02:6F:04:1E:EC'或'2A-02-6F-04-1E-EC')
        ip_address: 广播地址(默认为None，会使用局域网广播)
        port: 端口号(默认为9)
    """
    # 格式化MAC地址
    mac = mac_address.replace(":", "").replace("-", "")
    if len(mac) != 12:
        raise ValueError("MAC地址格式不正确")

    # 创建魔术包(6个0xFF + 16个目标MAC地址)
    data = b"FF" * 6 + (mac * 16).encode()
    magic_packet = b""
    for i in range(0, len(data), 2):
        magic_packet += struct.pack("B", int(data[i : i + 2], 16))

    # 创建socket并发送数据包
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        target_ip = ip_address or "255.255.255.255"
        sock.sendto(magic_packet, (target_ip, port))

    print(f"Sending magic packet to {mac_address}")

@app.post("/wol-trigger")
async def wol(request: Request):
    hash_req = (await request.body()).decode("utf-8")
    timestamp = str(math.floor(time.time() / 100))
    hash_expected = sha256(timestamp.encode()).hexdigest()
    if hash_req != hash_expected:
        print(timestamp)
        print(hash_req, hash_expected)
        return Response(status_code=403, content="Forbidden")
    try:
        wake_on_lan(MAC_ADDRESS, IP_ADDRESS)
        return Response(status_code=200, content="OK")
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=500, content="Internal Server Error")
