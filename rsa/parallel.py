#  Copyright 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Functions for parallel computation on multiple cores.

Introduced in Python-RSA 3.1.

.. note::

    Requires Python 2.6 or newer.

"""

import multiprocessing as mp
from multiprocessing.connection import Connection

import rsa.prime
import sympy
import rsa.randnum

__all__ = ["get_prime"]


def _find_prime(nbits: int, pipe: Connection) -> None:
    """Finds a prime number and sends it through the pipe."""
    while True:
        integer = rsa.randnum.read_random_odd_int(nbits)

        if sympy.isprime(integer):
            pipe.send(integer)
            return


def get_prime(nbits: int, pool_size: int) -> int:
    """Returns a prime number that can be stored in 'nbits' bits.

    Works in multiple threads at the same time.

    >>> import sympy
    >>> p = get_prime(128, 3)
    >>> sympy.isprime(p-1)
    False
    >>> sympy.isprime(p)
    True
    >>> sympy.isprime(p+1)
    False

    >>> from rsa.helpers import common
    >>> common.bit_size(p) == 128
    True
    """
    pipe_recv, pipe_send = mp.Pipe(duplex=False)
    procs = [mp.Process(target=_find_prime, args=(nbits, pipe_send)) for _ in range(pool_size)]

    try:
        for p in procs:
            p.start()

        result = pipe_recv.recv()
    finally:
        pipe_recv.close()
        pipe_send.close()

        for p in procs:
            p.terminate()
            p.join()

    return result


if __name__ == "__main__":
    print("Running doctests 100x or until failure")
    import doctest

    for count in range(100):
        failures, tests = doctest.testmod()
        if failures:
            break

        if count % 10 == 0 and count:
            print(f"{count} times")

    print("Doctests done")
