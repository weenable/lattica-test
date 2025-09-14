#!/usr/bin/env python3
import sys
import time
from lattica import Lattica

def main():
    args = sys.argv[1:]
    bootstraps = [args[0]] if args else None
    req_cid = args[0] if args else None

    # wait connected
    time.sleep(1)

    if bootstraps:
        # init
        lattica = Lattica.builder().with_bootstraps(bootstraps).build()

        peers = lattica.get_providers(req_cid)
        print(f"get providers success, peers: {peers}")

        data = lattica.get_block(req_cid)
        with open("test.bin", "wb") as f:
            f.write(data)

    else:
        # init
        lattica = Lattica.builder().build()

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