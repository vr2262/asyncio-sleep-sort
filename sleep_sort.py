#!/usr/bin/env python3
"""Async version of the infamous sleep sort."""
import argparse
import asyncio


async def sleepy(value):
    """Wait for as long as the value, then return it."""
    return await asyncio.sleep(float(value), result=value)


async def main(input_values, live=False):
    """Fire off an async timer for each input value.

    If live == True, print the values as they come back.
    """
    result = []
    for sleeper in asyncio.as_completed(map(sleepy, input_values)):
        awoken = await sleeper
        if live:
            print(awoken)
        result.append(awoken)
    print(' '.join(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('values', nargs='+')
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.values, args.live))
