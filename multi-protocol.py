#!/usr/bin/env python3
import sys
import time
from lattica import Lattica

def main():
    args = sys.argv[1:]
    bootstrap_nodes = args if args else []

    if bootstrap_nodes:
        lattica = Lattica.builder() \
            .with_bootstraps(bootstrap_nodes) \
            .build()

    else:
        lattica = Lattica.builder().build()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()