#!/usr/bin/env python3
from lattica import Lattica, rpc_stream, ConnectionHandler
import time
import sys
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
        lattica = Lattica.builder().with_bootstraps([bootstrap]).build()

        # wait connected
        time.sleep(1)
        service = TestService(lattica)

        bootstrap_addr, server_peer_id = parse_multiaddr(bootstrap)

        stub = service.get_stub(server_peer_id)
        future = stub.stream_rpc()
        result = future.result()
        print(result.message)

    else:
        # init
        lattica = Lattica.builder().with_listen_addrs(["/ip4/0.0.0.0/tcp/19090","/ip4/0.0.0.0/udp/19090/quic-v1", "/ip4/0.0.0.0/tcp/0/ws"]).build()

        # wait connected
        time.sleep(1)
        TestService(lattica)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()