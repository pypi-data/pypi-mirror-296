#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of ofunctions package

"""
ofunctions is a general library for basic repetitive tasks that should be no brainers :)

Versioning semantics:
    Major version: backward compatibility breaking changes
    Minor version: New functionality
    Patch version: Backwards compatible bug fixes

"""

__intname__ = "ofunctions.misc"
__author__ = "Orsiris de Jong"
__copyright__ = "Copyright (C) 2014-2024 Orsiris de Jong"
__description__ = "Collection of various functions"
__licence__ = "BSD 3 Clause"
__version__ = "1.8.0"
__build__ = "2024042401"
__compat__ = "python2.7+"


import sys

# python 2.7 compat fixes
try:
    from typing import Optional, List, Any, Union, Callable
except ImportError:
    pass


# Restrict number n between minimum and maximum
restrict_numbers = lambda n, n_min, n_max: max(min(n_max, n), n_min)

# Get current function name, can take int argument to get higher caller names
# eg fn_name(1) will return caller name, fn_name(2) will return caller of caller name
fn_name = lambda n=0: sys._getframe(n + 1).f_code.co_name


def rot13(string):
    # type: (str) -> str
    """
    Rot13 for only A-Z and a-z characters
    """
    return "".join(
        [
            (
                chr(ord(n) + (13 if "Z" < n < "n" or n < "N" else -13))
                if ("a" <= n <= "z" or "A" <= n <= "Z")
                else n
            )
            for n in string
        ]
    )


def rot47(string):
    # type: (str) -> str
    """
    rot47 for alphanumeric characters
    """
    x = []
    for i in range(len(string)):
        j = ord(string[i])
        if 33 <= j <= 126:
            x.append(chr(33 + ((j + 14) % 94)))
        else:
            x.append(string[i])
    return "".join(x)


def bytes_to_string(bytes_to_convert, strip_null=False):
    # type: (List[int], bool) -> Optional[str]
    """
    Litteral bytes to string
    :param bytes_to_convert: list of bytes in integer format
    :param strip_null: Remove trailing and ending null bytes
    :return: resulting string
    """
    try:
        value = "".join(chr(i) for i in bytes_to_convert)
        if strip_null:
            return value.strip("\x00")
        return value
    # AttributeError when None object has no strip attribute
    except (ValueError, TypeError, AttributeError):
        return None


def time_is_between(current_time, time_range):
    # type: (str, tuple) -> bool
    """
    https://stackoverflow.com/a/45265202/2635443
    print(is_between("11:00", ("09:00", "16:00")))  # True
    print(is_between("17:00", ("09:00", "16:00")))  # False
    print(is_between("01:15", ("21:30", "04:30")))  # True
    """

    if time_range[1] < time_range[0]:
        return current_time >= time_range[0] or current_time <= time_range[1]
    return time_range[0] <= current_time <= time_range[1]


def convert_time_to_seconds(value):
    # type (str) -> int
    """
    Converts hh:mm:ss into seconds
    Works with higher than 24 hh values, eg 101:45:01 would be 101 hours, 45 min and 1 second
    """

    splitted = value.split(":")
    splitted = [int(value) for value in splitted]
    if len(splitted) == 2:
        return splitted[0] * 60 + splitted[1]
    elif len(splitted) == 3:
        return splitted[0] * 3600 + splitted[1] * 60 + splitted[2]


def reverse_dict(dictionary):
    # type: (dict) -> dict
    """
    Return a reversed dictionary ie {value: key}
    """
    return {value: key for key, value in dictionary.items()}


def get_key_from_value(haystack, needle):
    # type: (dict, str) -> str
    """
    Returns a dict key by it's value, ie get_key_from_value({key: value}, value) returns key
    """
    return next((k for k, v in haystack.items() if v == needle), None)


def deep_dict_update(dict_original, dict_update):
    # type: (dict, dict) -> dict
    """
    Update a nested dictionnary with another nested dictionnary
    Balant copy from https://stackoverflow.com/a/60435617/2635443
    """
    if isinstance(dict_original, dict) and isinstance(dict_update, dict):
        output = dict(dict_original)
        keys_original = set(dict_original.keys())
        keys_update = set(dict_update.keys())
        similar_keys = keys_original.intersection(keys_update)
        similar_dict = {
            key: deep_dict_update(dict_original[key], dict_update[key])
            for key in similar_keys
        }
        new_keys = keys_update.difference(keys_original)
        new_dict = {key: dict_update[key] for key in new_keys}
        output.update(similar_dict)
        output.update(new_dict)
        return output
    else:
        return dict_update


def iter_over_keys(d: dict, fn: Callable) -> dict:
    """
    Executz value=fn(value) on any key in a nested dict
    """
    if isinstance(d, dict):
        for key, value in d.items():
            if isinstance(value, dict):
                d[key] = iter_over_keys(value, fn)
            else:
                d[key] = fn(key, d[key])
    return d


def replace_in_iterable(
    src,
    original,
    replacement=None,
    callable_wants_key=False,
    callable_wants_root_key=False,
    _root_key="",
    _parent_key=None,
):
    # type: (Union[dict, list], Union[str, Callable], Any, bool, bool, str, Any) -> Union[dict, list]
    """
    Recursive replace data in a struct

    Replaces every instance of string original with string replacement in a list/dict

    If original is a callable function, it will replace every value with original(value)
    If original is a callable function and callable_wants_key == True,
      it will replace every value with original(key, value) for dicts
      and with original(value) for any other data types

    If callable_wants_full_key, we'll hand the full key path to Callable in dot notation, eg section.subsection.key instead of key
    _root_key is used internally to pass full dot notation
    _parent_key is used internally and allows to pass parent_key to Callable when dealing with lists


    This is en enhanced version of the following if iter_over_keys
    """

    def _replace_in_iterable(key, _src):
        if isinstance(_src, (dict, list)):
            _src = replace_in_iterable(
                _src,
                original,
                replacement,
                callable_wants_key,
                callable_wants_root_key=callable_wants_root_key,
                _root_key=_sub_key,
                _parent_key=key,
            )
        elif isinstance(original, Callable):
            if callable_wants_key:
                if callable_wants_root_key:
                    _src = original(
                        "{}.{}".format(_root_key, key) if _root_key else key, _src
                    )
                else:
                    _src = original(key, _src)
            else:
                _src = original(_src)
        elif isinstance(_src, str) and isinstance(replacement, str):
            _src = _src.replace(original, replacement)
        else:
            _src = replacement
        return _src

    if isinstance(src, dict):
        for key, value in src.items():
            _sub_key = "{}.{}".format(_root_key, key) if _root_key else key
            src[key] = _replace_in_iterable(key, value)
    elif isinstance(src, list):
        result = []
        _sub_key = _root_key
        for entry in src:
            result.append(_replace_in_iterable(_parent_key, entry))
        src = result
    else:
        src = _replace_in_iterable(None, src)
    return src


class DotDict(dict):
    """
    A dictionary supporting dot notation
    Modified version of https://stackoverflow.com/a/23689767/2635443
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __dir__ = dict.keys

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DotDict(value)

    def lookup(self, dot_key):
        """
        Lookup value in a nested structure with a single key, e.g. "a.b.c"
        Equivalent of using __getattr__ = dict.get
        """
        path = list(reversed(dot_key.split(".")))
        dct = self
        while path:
            key = path.pop()
            if isinstance(dct, dict):
                dct = dct[key]
            elif isinstance(dct, list):
                dct = dct[int(key)]
            else:
                raise KeyError(key)
        return dct


def is_nan(var):
    # type: (Any) -> bool
    """
    Simple check if a variable is a numpy NaN
    based on the simple check where (nan is nan) gives True but (nan == nan) gives False
    """
    # pylint: disable=R0124 (comparison-with-itself)
    return not var == var


class BytesConverter(float):
    """
    float subclass that adds multiple properties in order to make computer guys life easier
    Internal always reasons in byte unit represented as float
    So why float ? Because on multiple python versions, int is limited to 2**32, which is only 4GB

    Converting bytes to other units:

    kilobytes = BytesConverter(2049).kbytes
    print(kilobytes)
    > 2

    terabits = BytesConverter(1000000000000).tbits
    print(terabits)
    > 7.2

    Getting human readable output

    print(BytesConverter(4350580).human)
    > 4.1 MB
    Getting bytes from human readable input

    print(BytesConverter("64 KB"))
    > 65536
    """

    # We need to respect international system of units standards https://physics.nist.gov/cuu/Units/binary.html
    byte_units = [
        "EB",
        "EiB",
        "PB",
        "PiB",
        "TB",
        "TiB",
        "GB",
        "GiB",
        "MB",
        "MiB",
        "KB",
        "KiB",
        "B",
    ]
    bits_units = [
        "Eb",
        "Eib",
        "Pb",
        "Pib",
        "Tb",
        "Tib",
        "Gb",
        "Gib",
        "Mb",
        "Mib",
        "Kb",
        "Kib",
        "b",
    ]

    """
     We'll keep bytes and bits measures the same here, except we'll multiply or divide by 8 later for bits
    """
    units = {
        "b": 8,
        "B": 1,
        "KB": 10**3,
        "Kb": 10**3,
        "KiB": 1024,
        "Kib": 1024,
        "MB": 10**6,
        "Mb": 10**6,
        "MiB": 1024**2,
        "Mib": 1024**2,
        "GB": 10**9,
        "Gb": 10**9,
        "GiB": 1024**3,
        "Gib": 1024**3,
        "TB": 10**12,
        "Tb": 10**12,
        "TiB": 1024**4,
        "Tib": 1024**4,
        "PB": 10**15,
        "Pb": 10**15,
        "PiB": 1024**5,
        "Pib": 1024**5,
        "EB": 1000**18,
        "Eb": 1000**18,
        "EiB": 1024**6,
        "Eib": 1024**6,
    }

    def __new__(cls, value, *args, **kwargs):
        """
        Creates a new int type object
        We can give an int parameter (which will be bytes) or a str parameter (like '500KB') which will be translated to bytes
        """

        # If a string was given, we'll try to convert it's unit to bytes
        if isinstance(value, str):
            converted_value = None
            for unit in cls.byte_units + cls.bits_units:
                result = value.split(unit)
                if len(result) == 2:
                    converted_value = float(result[0]) * cls.units[unit]
                    if unit in cls.bits_units:
                        converted_value /= 8
                    break
            if not converted_value and converted_value != 0:
                needs_raise = False
                try:
                    converted_value = float(value)
                # Here we intercept the original ValueError and replace it with ours
                except ValueError:
                    needs_raise = True
                if needs_raise:
                    raise ValueError(
                        'Given string "{}" cannot be converted to bytes'.format(value)
                    )
            value = converted_value
        if value < 0:
            raise ValueError("Negative bytes should not exist")
        return super(cls, cls).__new__(cls, value)

    def _from_units_to_bytes(self, string):
        # Check if we have value:
        value = None
        for unit in self.byte_units + self.bits_units:
            result = string.split(unit)
            if len(result) == 2:
                value = float(result[0]) * self.units[unit]
                if unit in self.bits_units:
                    value /= 8
                break
        if not value:
            needs_raise = False
            try:
                return float(string)
            except ValueError:
                needs_raise = True
            if needs_raise:
                raise ValueError(
                    'Given string "{}" cannot be converted to bytes'.format(string)
                )
        return value

    def _from_bytes_to_unit(self, unit):
        result = round(self / self.units[unit], 1)
        if unit in self.bits_units:
            result *= 8
        return result

    @property
    def bytes(self):
        return self

    @property
    def bits(self):
        return round(self * 8, 0)

    @property
    def kbytes(self):
        return self._from_bytes_to_unit("KiB")

    @property
    def kbits(self):
        return self._from_bytes_to_unit("Kib")

    @property
    def mbytes(self):
        return self._from_bytes_to_unit("MiB")

    @property
    def mbits(self):
        return self._from_bytes_to_unit("Mib")

    @property
    def gbytes(self):
        return self._from_bytes_to_unit("GiB")

    @property
    def gbits(self):
        return self._from_bytes_to_unit("Gib")

    @property
    def tbytes(self):
        return self._from_bytes_to_unit("TiB")

    @property
    def tbits(self):
        return self._from_bytes_to_unit("Tib")

    @property
    def pbytes(self):
        return self._from_bytes_to_unit("PiB")

    @property
    def pbits(self):
        return self._from_bytes_to_unit("Pib")

    @property
    def ebytes(self):
        return self._from_bytes_to_unit("EiB")

    @property
    def ebits(self):
        return self._from_bytes_to_unit("Eib")

    def _to_human(self, units):
        """
        Converts an int / float to a human readable format with less than 5 significant digits
        """
        for unit in units:
            operation = self.units[unit]

            result = self / operation
            if unit in self.bits_units:
                result *= 8

            # Check whether the int part of our result is to small
            if len(str(result).split("e-")) == 2:
                continue
            integer_result = str(result).split(".")[0]
            if integer_result == "0":
                continue
            if len(integer_result) <= 4:
                return "{} {}".format(round(result, 1), unit)
        return "{} {}".format(result, unit)

    @property
    def human_bytes(self):
        """
        Convert to any bytes unit (1000) from byte_unit list
        """
        unit_list = [unit for unit in self.byte_units if "i" not in unit]
        return self._to_human(unit_list)

    @property
    def human_iec_bytes(self):
        """
        Convert to any bibytes unit (1024) from byte_unit list
        """
        unit_list = [unit for unit in self.byte_units if "i" in unit]
        return self._to_human(unit_list)

    @property
    def human(self):
        return self.human_bytes

    @property
    def human_bits(self):
        unit_list = [unit for unit in self.bits_units if "i" not in unit]
        return self._to_human(unit_list)

    @property
    def human_iec_bits(self):
        unit_list = [unit for unit in self.bits_units if "i" in unit]
        return self._to_human(unit_list)


# for current fn name, specify 0 or no argument.
# for name of caller of current func, specify 1.
# for name of caller of caller of current func, specify 2. etc.
# Balantly copied from https://stackoverflow.com/a/31615605/2635443
fn_name = lambda n=0: sys._getframe(n + 1).f_code.co_name
