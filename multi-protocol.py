#!/usr/bin/env python3
import sys
import time
from lattica import Lattica

def main():
    args = sys.argv[1:]
    bootstraps = [args[0]] if args else None

    try:
        # init
        if bootstraps:
            lattica = Lattica.builder().with_bootstraps(bootstraps).build()
        else:
            lattica = Lattica.builder().build()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()