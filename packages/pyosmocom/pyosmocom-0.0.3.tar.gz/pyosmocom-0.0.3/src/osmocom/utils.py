# -*- coding: utf-8 -*-

""" osmocom: various utilities
"""

import json
import string
import datetime
import argparse
from io import BytesIO
from typing import Optional, List, NewType

# Copyright (C) 2009-2010  Sylvain Munaut <tnt@246tNt.com>
# Copyright (C) 2021 Harald Welte <laforge@osmocom.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# just to differentiate strings of hex nibbles from everything else
Hexstr = NewType('Hexstr', str)

def h2b(s: Hexstr) -> bytearray:
    """convert from a string of hex nibbles to a sequence of bytes"""
    return bytearray.fromhex(s)


def b2h(b: bytearray) -> Hexstr:
    """convert from a sequence of bytes to a string of hex nibbles"""
    return ''.join(['%02x' % (x) for x in b])


def h2i(s: Hexstr) -> List[int]:
    """convert from a string of hex nibbles to a list of integers"""
    return [(int(x, 16) << 4)+int(y, 16) for x, y in zip(s[0::2], s[1::2])]


def i2h(s: List[int]) -> Hexstr:
    """convert from a list of integers to a string of hex nibbles"""
    return ''.join(['%02x' % (x) for x in s])


def h2s(s: Hexstr) -> str:
    """convert from a string of hex nibbles to an ASCII string"""
    return ''.join([chr((int(x, 16) << 4)+int(y, 16)) for x, y in zip(s[0::2], s[1::2])
                    if int(x + y, 16) != 0xff])


def s2h(s: str) -> Hexstr:
    """convert from an ASCII string to a string of hex nibbles"""
    b = bytearray()
    b.extend(map(ord, s))
    return b2h(b)


def i2s(s: List[int]) -> str:
    """convert from a list of integers to an ASCII string"""
    return ''.join([chr(x) for x in s])


def swap_nibbles(s: Hexstr) -> Hexstr:
    """swap the nibbles in a hex string"""
    return ''.join([x+y for x, y in zip(s[1::2], s[0::2])])


def rpad(s: str, l: int, c='f') -> str:
    """pad string on the right side.
    Args:
            s : string to pad
            l : total length to pad to
            c : padding character
    Returns:
            String 's' padded with as many 'c' as needed to reach total length of 'l'
    """
    return s + c * (l - len(s))


def lpad(s: str, l: int, c='f') -> str:
    """pad string on the left side.
    Args:
            s : string to pad
            l : total length to pad to
            c : padding character
    Returns:
            String 's' padded with as many 'c' as needed to reach total length of 'l'
    """
    return c * (l - len(s)) + s


def half_round_up(n: int) -> int:
    return (n + 1)//2


def str_sanitize(s: str) -> str:
    """replace all non printable chars, line breaks and whitespaces, with ' ', make sure that
    there are no whitespaces at the end and at the beginning of the string.

    Args:
            s : string to sanitize
    Returns:
            filtered result of string 's'
    """

    chars_to_keep = string.digits + string.ascii_letters + string.punctuation
    res = ''.join([c if c in chars_to_keep else ' ' for c in s])
    return res.strip()


def is_hex(string: str, minlen: int = 2, maxlen: Optional[int] = None) -> bool:
    """
    Check if a string is a valid hexstring
    """

    # Filter obviously bad strings
    if not string:
        return False
    if len(string) < minlen or minlen < 2:
        return False
    if len(string) % 2:
        return False
    if maxlen and len(string) > maxlen:
        return False

    # Try actual encoding to be sure
    try:
        _try_encode = h2b(string)
        return True
    except:
        return False

class hexstr(str):
    """Class derived from 'str', represeting a string of hexadecimal digits. It differs in that
    comparisons are case-insensitive, and it offers encoding-free conversion from hexstr to bytes
    and vice-versa."""
    def __new__(cls, s: str):
        if not all(c in string.hexdigits for c in s):
            raise ValueError('Input must be hexadecimal digits only')
        # store as lower case digits
        return super().__new__(cls, s.lower())

    def __eq__(self, other: str) -> bool:
        # make sure comparison is done case-insensitive
        return str(self) == other.lower()

    def __getitem__(self, val) -> 'hexstr':
        # make sure slicing a hexstr will return a hexstr
        return hexstr(super().__getitem__(val))

    def to_bytes(self) -> bytes:
        """return hex-string converted to bytes"""
        s = str(self)
        if len(s) & 1:
            raise ValueError('Cannot convert hex string with odd number of digits')
        return h2b(s)

    @classmethod
    def from_bytes(cls, bt: bytes) -> 'hexstr':
        """instantiate hex-string from bytes"""
        return cls(b2h(bt))

#########################################################################
# ARGPARSE HELPERS
#########################################################################

def auto_int(x):
    """Helper function for argparse to accept hexadecimal integers."""
    return int(x, 0)

def _auto_uint(x, max_val: int):
    """Helper function for argparse to accept hexadecimal or decimal integers."""
    ret = int(x, 0)
    if ret < 0 or ret > max_val:
        raise argparse.ArgumentTypeError('Number exceeds permited value range (0, %u)' %  max_val)
    return ret

def auto_uint7(x):
    return _auto_uint(x, 127)

def auto_uint8(x):
    return _auto_uint(x, 255)

def auto_uint16(x):
    return _auto_uint(x, 65535)

def is_hexstr_or_decimal(instr: str) -> str:
    """Method that can be used as 'type' in argparse.add_argument() to validate the value consists of
    [hexa]decimal digits only."""
    if instr.isdecimal():
        return instr
    if not all(c in string.hexdigits for c in instr):
        raise ValueError('Input must be [hexa]decimal')
    if len(instr) & 1:
        raise ValueError('Input has un-even number of hex digits')
    return instr

def is_hexstr(instr: str) -> str:
    """Method that can be used as 'type' in argparse.add_argument() to validate the value consists of
    an even sequence of hexadecimal digits only."""
    if not all(c in string.hexdigits for c in instr):
        raise ValueError('Input must be hexadecimal')
    if len(instr) & 1:
        raise ValueError('Input has un-even number of hex digits')
    return instr

def is_decimal(instr: str) -> str:
    """Method that can be used as 'type' in argparse.add_argument() to validate the value consists of
    an even sequence of decimal digits only."""
    if not instr.isdecimal():
        raise ValueError('Input must decimal')
    return instr


class JsonEncoder(json.JSONEncoder):
    """Extend the standard library JSONEncoder with support for more types."""

    def default(self, o):
        if isinstance(o, (BytesIO, bytes, bytearray)):
            return b2h(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def all_subclasses(cls) -> set:
    """Recursively get all subclasses of a specified class"""
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])
