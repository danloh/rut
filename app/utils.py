# -*- coding: utf-8 -*-

import re

def split_str(s, delimiter=r'[,;，；]'):
    s = str(s)
    re_sp = re.split(delimiter, s)
    lst = [sp.strip() for sp in re_sp if sp.strip()]
    return lst


def str_to_dict(s, tail="Author", deltr=r'[,;，；]', sep=r'[()（）]'):
    lst = split_str(s, deltr)
    d = {}
    for i in lst:
        i_lst = split_str(i, sep)
        alst = [a for a in i_lst] + [str(tail)]
        key = alst[0]
        val = alst[1]
        d.setdefault(key, val)
    return d


def str_to_set(s, deltr=r'[,;，；]'):
    lst = split_str(s, deltr)
    st = set(t for t in lst)
    return st
