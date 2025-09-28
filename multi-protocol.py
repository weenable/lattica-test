#!/usr/bin/env python3
import sys
import time
from lattica import Lattica

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

def main():
    args = sys.argv[1:]
    bootstrap_nodes = [args[0]] if args else []

    server_peer_id = ""
    if len(bootstrap_nodes) > 0:
        bootstrap_addr, server_peer_id = parse_multiaddr(bootstrap_nodes[0])

    if bootstrap_nodes:
        lattica = Lattica.builder() \
            .with_bootstraps(bootstrap_nodes) \
            .with_listen_addrs(["/ip4/0.0.0.0/tcp/19090"]) \
            .build()

    else:
        lattica = Lattica.builder().with_listen_addrs(["/ip4/0.0.0.0/tcp/19090"]).build()

    try:
        while True:
            if len(bootstrap_nodes) > 0:
                print("peer ip: ", lattica.get_peer_addresses(server_peer_id))
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()