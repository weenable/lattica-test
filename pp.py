import socket
import time
import threading
import argparse

# ===== UDP Ping Server =====
def run_server(host='0.0.0.0', port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"✅ Ping Server started on {host}:{port}")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"📩 Received {len(data)} bytes from {addr}")
        sock.sendto(data, addr)  # 回射
        print(f"📤 Sent echo to {addr}")

# ===== UDP Ping Client =====
def run_client(server_ip, port=9999, count=5, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    for i in range(count):
        msg = f"ping-{i}-{time.time()}".encode()
        start = time.time()
        sock.sendto(msg, (server_ip, port))

        try:
            data, _ = sock.recvfrom(1024)
            end = time.time()
            rtt = (end - start) * 1000
            print(f"Reply from {server_ip}: seq={i} time={rtt:.2f} ms")
        except socket.timeout:
            print(f"Request timeout for seq={i}")

        time.sleep(1)

    sock.close()

# ===== Main Entrypoint =====
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple UDP Ping tool")
    parser.add_argument("--mode", choices=["server", "client"], required=True)
    parser.add_argument("--host", default="0.0.0.0", help="Server host (for server mode)")
    parser.add_argument("--port", type=int, default=9999, help="Port to use")
    parser.add_argument("--target", help="Server IP for client mode")
    parser.add_argument("--count", type=int, default=5, help="Ping count")
    args = parser.parse_args()

    if args.mode == "server":
        run_server(args.host, args.port)
    else:
        if not args.target:
            print("Error: --target is required in client mode")
        else:
            run_client(args.target, args.port, args.count)
