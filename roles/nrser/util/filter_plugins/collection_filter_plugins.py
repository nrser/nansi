from typing import *
import logging

import nansi.utils.collections
from nansi.utils.collections import TKey, TValue, find

TDefaultKey     = TypeVar('TDefaultKey')
TDefaultValue   = TypeVar('TDefaultValue')

from nansi.logging import get_plugin_logger

log = LOG = get_plugin_logger(__file__)
from nansi.logging.test import V

def defaults(
    overrides: Mapping[TKey, TValue],
    **defaults: Mapping[TDefaultKey, TDefaultValue]
) -> Mapping[Union[TKey, TDefaultKey], Union[TValue, TDefaultValue]]:
    '''
    >>> defaults(
    ...     {'path': '~/user/path'},
    ...     name = 'Default Name',
    ...     path = '/default/path',
    ... )
    ... 
    {'name': 'Default Name', 'path': '~/user/path'}
    
    Playbook usage:
    
    >>> user_args = { 'path': '~/user/path' }
    ... 
    >>> expr = """{{
    ...     user_args | defaults(
    ...         name = 'Default Name',
    ...         path = '/default/path',
    ...     )
    ... }}"""
    ... 
    >>> template(expr, user_args=user_args)
    ... 
    {'name': 'Default Name', 'path': '~/user/path'}
    
    '''
    return { **defaults, **overrides }

def _mapping_has_all(mapping, **key_values):
    '''Test if a `Mapping` has all key/value pairs in `key_values` (by
    equality).
    
    Or: is `key_values` a "sub-mapping" of `mapping` (as sets of key/value
    pairs)?
    
    >>> dct = {'A': 1, 'B': 2, 'C': 3}
    >>> _mapping_has_all(dct, A=1, B=2)
    True
    >>> _mapping_has_all(dct, A=1, B=1)
    False
    >>> _mapping_has_all(dct, A=1, D=4)
    False
    '''
    for key, value in key_values.items():
        if key not in mapping or mapping[key] != value:
            return False
    return True

def _mapping_has_any(mapping, **key_values):
    '''Test if a `Mapping` has any key/value pairs in `key_values` (by 
    equality).
    
    Or: does `key_values` intersect `mapping` (as sets of key/value pairs)?
    
    >>> dct = {'A': 1, 'B': 2, 'C': 3}
    >>> _mapping_has_all(dct, A=1, B=2)
    True
    >>> _mapping_has_all(dct, A=1, B=1)
    False
    >>> _mapping_has_all(dct, A=1, D=4)
    False
    '''
    for key, value in key_values.items():
        if key in mapping and mapping[key] == value:
            return True
    return False

def _iterable_has_all(itr, *items):
    '''Test if an interable includes all of `items` (by equality).
    
    >>> _iterable_has_all((1, 2, 3), 1, 3)
    True
    >>> _iterable_has_all((1, 2, 3), 1, 4)
    False
    '''
    missing = set(items)
    for item in itr:
        if item in missing:
            missing.remove(item)
        if len(missing) == 0:
            return True
    return False

def _iterable_has_any(itr, *items):
    '''Test if an interable includes all of `items` (by equality).
    
    >>> _iterable_has_any((1, 2, 3), 1, 3)
    True
    >>> _iterable_has_any((1, 2, 3), 1, 4)
    True
    '''
    for item in itr:
        if item in items:
            return True
    return False

def _object_has_all(obj, **attrs):
    '''Test if an object has all of `attrs` name/value pairs (by equality).
    
    >>> _object_has_all(Path('/a/b/c.txt'), name='c.txt', suffix='.txt')
    True
    >>> _object_has_all(Path('/a/b/c.txt'), name='c.txt', age=112)
    False
    '''
    for name, value in attrs.items():
        if not hasattr(obj, name) or getattr(obj, name) != value:
            return False
    return True

def _object_has_any(obj, **attrs):
    '''Test if an object has any of `attrs` name/value pairs (by equality).
    
    >>> _object_has_any(Path('/a/b/c.txt'), name='c.txt', suffix='.txt')
    True
    >>> _object_has_any(Path('/a/b/c.txt'), name='c.txt', age=112)
    True
    '''
    for name, value in attrs.items():
        if hasattr(obj, name) and getattr(obj, name) == value:
            return True
    return False

def has_all(obj, *args, **kwds):
    '''Routes: 
    
    1.  `collections.abc.Mapping`   -> `_mapping_has_all()`
    2.  `collections.abc.Iterable`  -> `_iterable_has_all()`
    3.  else                        -> `_object_has_all()`
    
    Returns a boolean in all cases.
    
    Playbook usage:
    
    >>> template(
    ...     "{{ stdout.splitlines() | has_all('one', 'three') }}",
    ...     stdout = "one\\ntwo\\nthree\\nfour",
    ... )
    True
    '''
    if isinstance(obj, Mapping):
        return _mapping_has_all(obj, *args, **kwds)
    elif isinstance(obj, Iterable):
        return _iterable_has_all(obj, *args, **kwds)
    else:
        return _object_has_all(obj, *args, **kwds)

def get(obj, name, *rest):
    len_rest = len(rest)
    if len_rest > 1:
        raise TypeError(
            f"get() takes from 2 to 3 positional arguments but "
            "{2+len(rest)} were given"
        )
    if isinstance(obj, (Sequence, Mapping)):
        if len_rest == 1:
            return obj.get(name, rest[0])
        return obj[name]
    else:
        return getattr(obj, name, *rest)

def has_any(obj, *args, **kwds):
    '''Routes: 
    
    1.  `collections.abc.Mapping`   -> `_mapping_has_any()`
    2.  `collections.abc.Iterable`  -> `_iterable_has_any()`
    3.  else                        -> `_object_has_any()`
    
    Returns a boolean in all cases.
    '''
    if isinstance(obj, Mapping):
        return _mapping_has_any(obj, *args, **kwds)
    elif isinstance(obj, Iterable):
        return _iterable_has_any(obj, *args, **kwds)
    else:
        return _object_has_any(obj, *args, **kwds)

def find_has_all(itr, *args, **kwds):
    '''Find first item in `itr` that passes `has_all(item, *args, **kwds)`.
    
    >>> animals = (
    ...     {'name': 'Hudie', 'type': 'cat', 'cute': True},
    ...     {'name': 'Mr. Sloth', 'type': 'sloth', 'cute': True},
    ... )
    
    >>> find_has_all(animals, name='Hudie', cute=True)
    {'name': 'Hudie', 'type': 'cat', 'cute': True}
    
    >>> find_has_all(animals, name='Mr. Sloth', type='small bear') is None
    True
    '''
    return find(lambda item: has_all(item, *args, **kwds), itr)

def find_has_any(itr, *args, **kwds):
    '''Find first item in `itr` that passes `has_any(item, *args, **kwds)`.
    
    >>> animals = (
    ...     {'name': 'Hudie', 'type': 'cat', 'cute': True},
    ...     {'name': 'Mr. Sloth', 'type': 'sloth', 'cute': True},
    ... )
    
    >>> find_has_any(animals, name='Hudie', cute=True)
    {'name': 'Hudie', 'type': 'cat', 'cute': True}
    
    >>> find_has_any(animals, name='Mr. Sloth', type='small bear')
    {'name': 'Mr. Sloth', 'type': 'sloth', 'cute': True}
    '''
    return find(lambda item: has_any(item, *args, **kwds), itr)

class FilterModule:
    def filters(self):
        return dict(
            # dict_merge is included by Ansible as `combine`.
            # 
            # https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#combining-hashes-dictionaries
            # 
            defaults        = defaults,
            dig             = nansi.utils.collections.dig,
            find_has_all    = find_has_all,
              find_by       = find_has_all,
            find_has_any    = find_has_any,
            has_all         = has_all,
            has_any         = has_any,
            get             = get,
        )

if __name__ == '__main__':
    import doctest
    from pathlib import Path
    from nansi.utils.doctesting import template_for_filters
    template = template_for_filters(FilterModule)
    doctest.testmod()
