#!/usr/bin/env python3
"""Async version of the infamous sleep sort.

Turns out this is a roundabout heap sort:
https://stackoverflow.com/questions/39398312
"""
import argparse
import asyncio


class FloatSpecialZero(float):
    """Like float, but never compares equal to 0.

    This is because asyncio.sleep treats 0 as a special case and returns
    immediately.

    https://github.com/python/cpython/blob
    /e6d0995cc9f3416e7b10b3965e8cdf35a7eebf90/Lib/asyncio/tasks.py#L506
    """

    def __eq__(self, other):
        return super().__eq__(other) if other else False


async def sleepy(value):
    """Wait for as long as the value, then return it."""
    return await asyncio.sleep(FloatSpecialZero(value), result=value)


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
