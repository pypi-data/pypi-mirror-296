import datetime
import functools
import tomllib

import datahold
import tomli_w

__all__ = ["Holder"]
_TYPES = (bool, datetime.datetime, datetime.date, datetime.time, str, int, float)


def _copy(value):
    if type(value) is dict:
        return _copy_dict(value)
    if type(value) is list:
        return _copy_list(value)
    if type(value) in _TYPES:
        return value
    raise TypeError("type %r is not allowed" % type(value))


def _copy_dict(value):
    return _copy_dict_1(**value)


def _copy_dict_1(**kwargs):
    for k in kwargs.keys():
        kwargs[k] = _copy(kwargs[k])
    return kwargs


def _copy_list(value):
    return [_copy(v) for v in value]


def _get_keys(keys, /):
    if issubclass(type(keys), str):
        return [keys]
    else:
        return list(keys)


class Holder(datahold.OkayDict):

    def __delitem__(self, keys):
        keys = _get_keys(keys)
        if not keys:
            self.clear()
            return
        ans = self._data
        while len(keys) > 1:
            ans = ans[keys.pop(0)]
        del ans[keys[0]]

    def __getitem__(self, keys):
        keys = _get_keys(keys)
        ans = self._data
        for k in keys:
            ans = ans[k]
        ans = _copy(ans)
        return ans

    def __init__(self, string="") -> None:
        self._data = tomllib.loads(str(string))

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, str(self))

    def __setitem__(self, keys, value):
        keys = _get_keys(keys)
        if not keys:
            self.data = value
            return
        value = _copy(value)
        ans = self._data
        while len(keys) > 1:
            ans = ans[keys.pop(0)]
        ans[keys[0]] = value

    def __str__(self) -> str:
        return tomli_w.dumps(self._data)

    @functools.wraps(dict.clear)
    def clear(self):
        return self._data.clear()

    @property
    def data(self):
        return _copy_dict(self._data)

    @data.setter
    def data(self, value):
        self._data = _copy_dict(value)

    @data.deleter
    def data(self):
        self.clear()

    def dump(self, file):
        with open(file, "w") as s:
            s.write(str(self))

    @staticmethod
    def fromdict(dictionary):
        ans = Holder()
        ans.data = dictionary
        return ans

    def get(self, *keys, default=None):
        try:
            return self[keys]
        except KeyError:
            return default

    @classmethod
    def load(cls, file):
        with open(file, "r") as s:
            text = s.readlines()
        return cls(text)

    def setdefault(self, *keys, default):
        if not keys:
            return _copy_dict(self._data)
        keys = list(keys)
        ans = self._data
        while len(keys) > 1:
            k = keys.pop(0)
            if type(ans) is dict and type(keys[0]) is str:
                ans.setdefault(k, {})
            ans = ans[k]
        if type(ans) is dict:
            return ans.setdefault(keys[0], default)
        return ans[keys[0]]
