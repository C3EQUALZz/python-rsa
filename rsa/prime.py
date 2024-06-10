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

"""Numerical functions related to primes.

Implementation based on the book Algorithm Design by Michael T. Goodrich and
Roberto Tamassia, 2002.
"""

import rsa.helpers
import rsa.randnum
import math
import sympy

__all__ = ["get_prime", "are_relatively_prime"]


def get_prime(n_bits: int) -> int:
    """Returns a prime number that can be stored in 'nbits' bits.

    >>> from sympy import isprime
    >>> p = get_prime(128)
    >>> isprime(p-1)
    False
    >>> isprime(p)
    True
    >>> isprime(p+1)
    False

    >>> from rsa.helpers import common
    >>> common.bit_size(p) == 128
    True
    """

    assert n_bits > 3  # the loop will hang on too small numbers

    while True:
        integer = rsa.randnum.read_random_odd_int(n_bits)

        # Test for primeness
        if sympy.isprime(integer):
            return integer


def are_relatively_prime(a: int, b: int) -> bool:
    """Returns True if a and b are relatively prime, and False if they
    are not.

    >>> are_relatively_prime(2, 3)
    True
    >>> are_relatively_prime(2, 4)
    False
    """

    return math.gcd(a, b) == 1


if __name__ == "__main__":
    print("Running doctests 1000x or until failure")
    import doctest

    for count in range(1000):
        (failures, tests) = doctest.testmod()
        if failures:
            break

        if count % 100 == 0 and count:
            print("%i times" % count)

    print("Doctests done")
