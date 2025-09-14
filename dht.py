#!/usr/bin/env python3
import sys
import time
from lattica import Lattica
import random

def main():
    args = sys.argv[1:]
    bootstraps = [args[0]] if args else None

    # wait connected
    time.sleep(1)

    if bootstraps:
        # init
        lattica = Lattica.builder().with_bootstraps(bootstraps).build()

        print("=== simple get test ===")
        result = lattica.get("name")
        if result:
            print(f"Name: {result.value}")

        print("=== subkey get test ===")
        votes_result = lattica.get("user_vote")
        if votes_result:
            for user, vote in votes_result.value.items():
                print(f"{user}: {vote.value}")

    else:
        # init
        lattica = Lattica.builder().build()

        # simple store
        lattica.store("name", "ween")

        # subkey store
        users = ["alice", "bob", "carol", "david"]
        for user in users:
            vote = random.choice(["yes", "no", "maybe"])
            lattica.store("user_vote", vote, subkey=user)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()