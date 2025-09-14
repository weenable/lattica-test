#!/usr/bin/env python3
import sys
import time
from lattica import Lattica

def main():
    args = sys.argv[1:]
    bootstraps = [args[0]] if args else None
    req_cid = args[1] if args else None

    if bootstraps:
        # init
        lattica = Lattica.builder().with_bootstraps(bootstraps).build()

        # wait connected
        time.sleep(1)

        peers = lattica.get_providers(req_cid)
        print(f"get providers success, peers: {peers}")

        data = lattica.get_block(req_cid)
        with open("test.bin", "wb") as f:
            f.write(data)

    else:
        # init
        lattica = Lattica.builder().with_listen_addrs(["/ip4/0.0.0.0/tcp/18080","/ip4/0.0.0.0/udp/18080/quic-v1", "/ip4/0.0.0.0/tcp/0/ws"]).build()

        # wait connected
        time.sleep(1)

        # generate resource 10MB
        with open("test.bin", "rb") as f:
            data = f.read()

            # put block
            cid = lattica.put_block(data)
            print(f"put block success, cid {cid}")

            # start provider
            lattica.start_providing(cid)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()