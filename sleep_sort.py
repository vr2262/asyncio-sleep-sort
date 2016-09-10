#!/usr/bin/env python3
"""Async version of the infamous sleep sort.

Turns out this is a roundabout heap sort:
https://stackoverflow.com/questions/39398312
"""
import argparse
import asyncio
from asyncio import as_completed


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


async def printy(value):
    """Like sleepy, but it prints the value before returning."""
    result = await sleepy(value)
    print(result)
    return result


async def main(input_values, live=False):
    """Fire off an async timer for each input value."""
    f = printy if live else sleepy
    print(' '.join([await v for v in as_completed(map(f, input_values))]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('values', nargs='+')
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.values, args.live))
