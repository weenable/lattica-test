#!/usr/bin/env python3
import asyncio
import time
import sys
from lattica import Lattica, rpc_method, rpc_stream, rpc_stream_iter, ConnectionHandler
import pickle

class MockProtoRequest:
    def __init__(self, data=None):
        self.data = data
        self.timestamp = time.time()

    def SerializeToString(self):
        return pickle.dumps({
            'data': self.data,
            'timestamp': self.timestamp
        })

    def ParseFromString(self, data):
        parsed = pickle.loads(data)
        self.data = parsed['data']
        self.timestamp = parsed['timestamp']
        return self

class MockProtoResponse:
    def __init__(self, data=None, message=''):
        self.data = data
        self.message = message

    def SerializeToString(self):
        return pickle.dumps({
            'data': self.data,
            'message': self.message,
        })

    def ParseFromString(self, data):
        parsed = pickle.loads(data)
        self.message = parsed['message']
        self.data = parsed['data']
        return self


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
    @rpc_stream
    def stream_rpc(self, request: MockProtoRequest ) -> MockProtoResponse:
        return MockProtoResponse(
            message=f"Processed data of size {len(request.data)}",
            data=None
        )

def main():
    args = sys.argv[1:]
    bootstrap = args[0] if args else None

    if bootstrap:
        # init
        lattica = Lattica.builder().with_bootstraps([bootstrap]).with_listen_addrs(["/ip4/0.0.0.0/udp/19090/quic-v1"]).with_mdns(False).build()

        # wait connected
        time.sleep(1)
        service = TestService(lattica)

        bootstrap_addr, server_peer_id = parse_multiaddr(bootstrap)

        while True:
            total_size = 16 * 1024
            request = MockProtoRequest(data=bytearray(total_size))
            stub = service.get_stub(server_peer_id)
            start_time = time.time()
            future = stub.stream_rpc(request)
            result = future.result()
            transfer_time = (time.time() - start_time)*1000
            print(f"result: {result.message}")
            print(f"Total transfer time: {transfer_time:.2f}ms")
            time.sleep(1)

    else:
        # init
        lattica = Lattica.builder().with_mdns(False).with_listen_addrs(["/ip4/0.0.0.0/udp/19090/quic-v1"]).build()

        # wait connected
        TestService(lattica)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()