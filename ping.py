#!/usr/bin/env python3
import sys
import time
from lattica import Lattica
import asyncio

async def print_peer_info(node, node_name):
    print(f"\n{node_name}:")
    peers = node.get_all_peers()

    for peer_id in peers:
        peer_info = node.get_peer_info(peer_id)
        if peer_info:
            print(f"    - RTT: {peer_info.rtt_ms}ms")
            print(f"    - last_seen: {peer_info.last_seen}")
            if peer_info.decay_3:
                print(f"    - decay_3: {peer_info.decay_3}ms")
            if peer_info.decay_10:
                print(f"    - decay_10: {peer_info.decay_10}ms")
            if peer_info.failures:
                print(f"    - failures: {peer_info.failures}")
            if peer_info.failure_rate:
                print(f"    - failure_rate: {peer_info.failure_rate}")

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

async def main():
    args = sys.argv[1:]
    bootstrap = args[0] if args else None

    if bootstrap:
        # init
        lattica = Lattica.builder().with_bootstraps([bootstrap]).build()

        # wait connected
        time.sleep(1)

        bootstrap_addr, server_peer_id = parse_multiaddr(bootstrap)

        for i in range(1, 20):
            print(f"\nPing test {i}/20:")

            before_rtt = lattica.get_peer_rtt(server_peer_id)
            print(f"  - Before RTT: {before_rtt}s")

            # wait for next ping finish
            await asyncio.sleep(1)

            after_rtt = lattica.get_peer_rtt(server_peer_id)
            print(f"  - After RTT: {after_rtt}s")

            if before_rtt is not None and after_rtt is not None:
                diff = abs(after_rtt - before_rtt)
                print(f"  - RTT Change: {diff:.6f}s")

            peer_info = lattica.get_peer_info(server_peer_id)
            if peer_info:
                print(f"  - Current Server RTT: RTT={peer_info.rtt_ms}ms")
                addresses = lattica.get_peer_addresses(server_peer_id)
                print(f"  - Server address count: {len(addresses)}")

        print("\nfinal info:")
        await print_peer_info(lattica, "client")


    else:
        # init
        lattica = Lattica.builder().with_listen_addrs(["/ip4/0.0.0.0/tcp/18080","/ip4/0.0.0.0/udp/18080/quic-v1", "/ip4/0.0.0.0/tcp/0/ws"]).build()

        # wait connected
        time.sleep(1)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    asyncio.run(main())