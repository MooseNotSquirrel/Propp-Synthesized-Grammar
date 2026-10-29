#!/usr/bin/env python3
"""
tables.py -- the one reader of the normalized data set (DataProtocol.md, decision 4).

Programs read Data/tables/ through this module and never the readers' raw files. Rows come back as dicts, in
the order the builder read them. `files(name, patterns, reader)` gives a table's rows file by file, for the files
an older program's glob patterns named, in the order that program read them, so that a program moved onto the
tables reads exactly what it read before (T3).
"""
import collections
import fnmatch
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.join(HERE, 'tables')
_CACHE = {}


def rows(name):
    """every row of a table, as dicts, in the builder's order"""
    if name not in _CACHE:
        lines = open(os.path.join(TABLES, name + '.tsv'), encoding='utf-8').read().split('\n')
        head = lines[0].split('\t')
        _CACHE[name] = [dict(zip(head, l.split('\t'))) for l in lines[1:] if l]
    return _CACHE[name]


def local(story):
    """the story's id as the raw files spell it"""
    return story.split(':', 1)[1]


def _by_file(name):
    key = name + '#files'
    if key not in _CACHE:
        d = collections.OrderedDict()
        for r in rows(name):
            d.setdefault(r['file'], []).append(r)
        _CACHE[key] = d
    return _CACHE[key]


P = os.path.dirname(os.path.dirname(HERE))


def file_rows(name, path):
    """a table's rows from one raw file, named by its full path as an older program built it, in line order"""
    return _by_file(name).get(os.path.relpath(path, P).replace(os.sep, '/'), [])


def native(path):
    """the sort key an older program used: its globbed paths, sorted with this platform's separator"""
    return path.replace('/', os.sep)


def files(name, patterns, reader=None):
    """the rows of the files each pattern names (paths relative to StoryLanguage, '%s' for the reader), pattern by
    pattern, each pattern's files sorted as glob's sorted() sorted them, each file's rows in their order"""
    d = _by_file(name)
    for pat in patterns:
        p = pat % reader if reader and '%s' in pat else pat
        for f in sorted((f for f in d if fnmatch.fnmatchcase(f, p)), key=native):
            for r in d[f]:
                yield r


def sorted_files(name, patterns, reader=None):
    """as files(), but all the patterns' files sorted together, as one sorted() of their union"""
    d = _by_file(name)
    ps = [pat % reader if reader and '%s' in pat else pat for pat in patterns]
    for f in sorted({f for f in d for p in ps if fnmatch.fnmatchcase(f, p)}, key=native):
        for r in d[f]:
            yield r
