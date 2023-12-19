import functools
import os, os.path
from utils import open_any_enc

from webui_helper import webui_bind_func

def get_book_data(webroot: str, fname: str):
    fname = os.path.join(webroot, fname.lstrip('\\/'))
    if os.path.exists(fname):
        with open_any_enc(fname) as f:
            return str(f.read())
    raise FileNotFoundError(f'Can not find file "{fname}"')

def get_all_books(webroot: str, dir: str):
    ret = []
    dir = os.path.normpath(os.path.join(webroot, dir.lstrip('\\/')))
    with os.scandir(dir) as it:
        for entry in it:
            if entry.is_file() and entry.name.lower().endswith('.txt'):
                ret.append({"name": entry.name, "size": entry.stat().st_size})
    return ret

def get_progress(webroot: str, fname: str):
    pfile = os.path.join(webroot, fname.lstrip('\\/'))
    p = ''
    if os.path.exists(pfile):
        with open(pfile, 'r') as f:
            p = f.read()
    return p

def set_progress(webroot: str, fname: str, progress: str):
    pfile = os.path.join(webroot, fname.lstrip('\\/'))
    with open(pfile, 'w') as f:
        f.write(progress)

def bind_funcs(win, webroot):
    webui_bind_func(win, "get_book_data", functools.partial(get_book_data, webroot))
    webui_bind_func(win, "get_all_books", functools.partial(get_all_books, webroot))
    webui_bind_func(win, "get_progress", functools.partial(get_progress, webroot))
    webui_bind_func(win, "set_progress", functools.partial(set_progress, webroot))
