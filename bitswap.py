#!/usr/bin/env python3
import sys
import time
from lattica import Lattica

def generate_resource():
    with open("test_10m.bin", "wb") as f:
        f.write(b"\0" * 10 * 1024 * 1024)

def main():
    args = sys.argv[1:]
    bootstrap_nodes = args if args else []

    if bootstrap_nodes:
        lattica = Lattica.builder() \
            .with_bootstraps(bootstrap_nodes) \
            .build()



    else:
        # init lattica
        lattica = Lattica.builder().build()

        # generate file resource
        generate_resource()

        # put block


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()