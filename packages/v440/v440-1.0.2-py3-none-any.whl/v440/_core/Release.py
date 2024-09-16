from __future__ import annotations

import functools
import types
import typing

import datahold
import scaevola

from . import utils


class Release(datahold.OkayList, scaevola.Scaevola):
    def __add__(self, other, /):
        other = type(self)(other)
        ans = self.copy()
        ans._data += other._data
        return ans

    def __getitem__(self, key):
        if type(key) is slice:
            return self._getitem_slice(key)
        else:
            return self._getitem_index(key)

    def __iadd__(self, other, /):
        self._data += type(self)(other)._data

    def __repr__(self) -> str:
        return "%s(%r)" % (type(self).__name__, str(self))

    def __setitem__(self, key, value):
        if type(key) is slice:
            self._setitem_slice(key, value)
        else:
            self._setitem_index(key, value)

    def __str__(self) -> str:
        return self.format()

    def _getitem_index(self, key):
        key = utils.toindex(key)
        if len(self) <= key:
            return 0
        return self._data[key]

    def _getitem_slice(self, key):
        key = utils.torange(key, len(self))
        ans = [self._getitem_index(i) for i in key]
        return ans

    def _setitem_index(self, key, value):
        key = utils.toindex(key)
        value = utils.numeral(value)
        length = len(self)
        if length > key:
            self._data[key] = value
            return
        if value == 0:
            return
        self._data.extend([0] * (key - length))
        self._data.append(value)

    def _setitem_slice(self, key, value):
        key = list(utils.torange(key, len(self)))
        value = self._tolist(value)
        if len(key) != len(value):
            e = "attempt to assign sequence of size %s to extended slice of size %s"
            e %= (len(value), len(key))
            raise ValueError(e)
        maximum = max(*key)
        ext = max(0, maximum + 1 - len(self))
        data = self.data
        data += [0] * ext
        for k, v in zip(key, value):
            data[k] = v
        while len(data) and not data[-1]:
            data.pop()
        self._data = data

    @staticmethod
    def _tolist(value):
        if utils.isiterable(value):
            value = [utils.numeral(x) for x in value]
            return value
        value = str(value).lower().strip()
        value = value.replace("_", ".")
        value = value.replace("-", ".")
        if value == "":
            return list()
        if value.startswith("v") or value.startswith("."):
            value = value[1:]
        value = value.split(".")
        if "" in value:
            raise ValueError
        value = [utils.numeral(x) for x in value]
        return value

    def bump(self, index=-1, amount=1):
        x = self._getitem_index(index) + amount
        self._setitem_index(index, x)
        if index != -1:
            self.data = self.data[: index + 1]

    @property
    def data(self):
        return list(self._data)

    @data.setter
    @utils.setterdeco
    def data(self, v):
        v = self._tolist(v)
        while v and v[-1] == 0:
            v.pop()
        self._data = v

    @data.deleter
    def data(self):
        self._data = []

    def extend(self, other, /):
        self += other

    def format(self, cutoff=None):
        format_spec = str(cutoff) if cutoff else ""
        i = int(format_spec) if format_spec else None
        ans = self[:i]
        if len(ans) == 0:
            ans += [0]
        ans = [str(x) for x in ans]
        ans = ".".join(ans)
        return ans

    @property
    def major(self) -> int:
        return self[0]

    @major.setter
    @utils.setterdeco
    def major(self, value: typing.Any):
        self[0] = value

    @major.deleter
    def major(self):
        del self[0]

    @property
    def micro(self) -> int:
        return self[2]

    @micro.setter
    @utils.setterdeco
    def micro(self, value: typing.Any):
        self[2] = value

    @micro.deleter
    def micro(self):
        del self[2]

    @property
    def minor(self) -> int:
        return self[1]

    @minor.setter
    @utils.setterdeco
    def minor(self, value: typing.Any):
        self[1] = value

    @minor.deleter
    def minor(self):
        del self[1]
