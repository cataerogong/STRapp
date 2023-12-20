import functools
import os, os.path
from strapp import BUNDLE_DIR
from utils import open_any_enc

from webui_helper import append_html, comment_js_file, webui_bind_func, webui_run_js


def _get_book_data(webroot: str, fname: str):
    fname = os.path.join(webroot, fname.lstrip('\\/'))
    print('Loading book:', fname)
    if os.path.exists(fname):
        with open_any_enc(fname) as f:
            return str(f.read())
    raise FileNotFoundError(f'Can not find file "{fname}"')

def _get_all_books(webroot: str, dir: str):
    ret = []
    dir = os.path.normpath(os.path.join(webroot, dir.lstrip('\\/')))
    with os.scandir(dir) as it:
        for entry in it:
            if entry.is_file() and entry.name.lower().endswith('.txt'):
                ret.append({"name": entry.name, "size": entry.stat().st_size})
    return ret

def _get_progress(webroot: str, fname: str):
    pfile = os.path.join(webroot, fname.lstrip('\\/'))
    # print('Loading progress:', pfile)
    p = ''
    if os.path.exists(pfile):
        with open(pfile, 'r') as f:
            p = f.read()
    return p

def _set_progress(webroot: str, fname: str, progress: str):
    pfile = os.path.join(webroot, fname.lstrip('\\/'))
    # print('Saving progress:', pfile)
    with open(pfile, 'w') as f:
        f.write(progress)

def patch_html(html):
    js = ["scripts/webdav.js", "scripts/enh-db.js", "scripts/enh-bookshelf.js", "scripts/enh-webdav.js"]
    for j in js:
        html = comment_js_file(html, j)
    return html

def bind_funcs(win, webroot):
    webui_bind_func(win, "get_book_data", functools.partial(_get_book_data, webroot))
    webui_bind_func(win, "get_all_books", functools.partial(_get_all_books, webroot))
    webui_bind_func(win, "get_progress", functools.partial(_get_progress, webroot))
    webui_bind_func(win, "set_progress", functools.partial(_set_progress, webroot))

def run_js(win):
    js_file = os.path.normpath(os.path.join(BUNDLE_DIR, 'stre.js'))
    webui_run_js(win, js_file)
