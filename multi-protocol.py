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

    if bootstrap_nodes:
        lattica = Lattica.builder() \
            .with_bootstraps(bootstrap_nodes) \
            .with_listen_addrs(["/ip4/0.0.0.0/udp/17070/quic-v1"]) \
            .with_relay_servers(["/ip4/47.236.20.72/tcp/18080/p2p/12D3KooWSo67G9nW1hSrzZpVESn1Q8wDshF2Uyh8qfcg5D6yJ74q"]) \
            .with_protocol("/12D3KooWEP3aVZo1XQztmjX14nwJUJUt3bdLaCEuwGhAYWpCzLBo") \
            .with_dcutr(True) \
            .build()

    else:
        lattica = Lattica.builder().with_listen_addrs(["/ip4/0.0.0.0/tcp/19090"]).build()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()