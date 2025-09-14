#!/usr/bin/env python3
from lattica import Lattica, rpc_method, ConnectionHandler
import time
import sys

def parse_multiaddr(addr_str: str):
    if not addr_str.startswith('/'):
        raise ValueError(f"Invalid multiaddr format: {addr_str}")

    parts = addr_str.strip().split('/')
    if len(parts) < 6:
        raise ValueError(f"Incomplete multiaddr: {addr_str}")

    peer_id = None
    for i, part in enumerate(parts):
        if part == 'p2p' and i + 1 < len(parts):
            peer_id = parts[i + 1]
            break

    if not peer_id:
        raise ValueError(f"No peer ID found in multiaddr: {addr_str}")

    return addr_str, peer_id

class TestService(ConnectionHandler):
    @rpc_method
    def add(self, a: int, b: int) -> int:
        return a + b

def main():
    args = sys.argv[1:]
    bootstrap = args[0] if args else None

    # wait connected
    time.sleep(1)

    if bootstrap:
        # init
        lattica = Lattica.builder().with_bootstraps([bootstrap]).build()
        service = TestService(lattica)

        bootstrap_addr, server_peer_id = parse_multiaddr(bootstrap)

        stub = service.get_stub(server_peer_id)
        future = stub.add(10, 20)
        result = future.result()
        print(f"10 + 20 = {result}")

    else:
        # init
        lattica = Lattica.builder().with_listen_addrs(["/ip4/0.0.0.0/tcp/18080","/ip4/0.0.0.0/udp/18080/quic-v1", "/ip4/0.0.0.0/tcp/0/ws"]).build()
        TestService(lattica)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()