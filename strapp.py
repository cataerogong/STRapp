import argparse
import os

from webwin import WebWinApp, open_any_enc

__version__ = "1.0.0"
__app_name__ = 'STRapp'
__app_desc__ = '让 SimpleTextReader 像本地应用程序一样运行'


class STReHandler:
    def __init__(self, webroot):
        self.webroot = webroot

    def get_book_data(self, fname: str):
        fname = os.path.normpath(os.path.join(self.webroot, fname.lstrip('\\/')))
        print(f'Loading book: {fname}')
        if os.path.exists(fname):
            with open_any_enc(fname) as f:
                return str(f.read())
        raise FileNotFoundError(f'Can not find file "{fname}"')

    def get_all_books(self, dir: str):
        ret = []
        dir = os.path.normpath(os.path.join(self.webroot, dir.lstrip('\\/')))
        with os.scandir(dir) as it:
            for entry in it:
                if entry.is_file() and entry.name.lower().endswith('.txt'):
                    ret.append({"name": entry.name, "size": entry.stat().st_size})
        return ret

    def get_progress(self, fname: str):
        pfile = os.path.normpath(os.path.join(self.webroot, fname.lstrip('\\/')))
        # print(f'Loading progress: {pfile}')
        p = ''
        if os.path.exists(pfile):
            with open(pfile, 'r') as f:
                p = f.read()
        return p

    def set_progress(self, fname: str, progress: str):
        pfile = os.path.normpath(os.path.join(self.webroot, fname.lstrip('\\/')))
        # print(f'Saving progress: {pfile}')
        with open(pfile, 'w') as f:
            f.write(progress)


class STRapp(WebWinApp):
    def adjust_argparser(self):
        self.argparser.del_argument('--mainpage')
        self.argparser.del_argument('--size')
        self.argparser.mod_argument('--webroot', metavar='STR_ROOT', help='SimpleTextReader 主目录 [默认：当前目录]')
        self.argparser.mod_argument('--del-js', help=argparse.SUPPRESS)
        self.argparser.mod_argument('--run-js', help=argparse.SUPPRESS)
        self.argparser.add_argument('--stre', action='store_true', help='启用 SimpleTextReader-enhance 单机增强模式')
        self.argparser.epilog = '【*注意*】用到了浏览器存储（如cookie,LocalStorage,indexdb），必须固定端口(--port)，否则会丢失设置。'

    def apply_args(self):
        # 设置固定参数
        self.args.mainpage = 'index.html'
        if self.args.stre:
            self.args.del_js.extend(["scripts/webdav.js",
                                    "scripts/enh-db.js",
                                    "scripts/enh-bookshelf.js",
                                    "scripts/enh-webdav.js",
                                    "scripts/enhance-db.js",
                                    "scripts/enhance.js"])
            self.args.run_js.append(os.path.join(self.BUNDLE_DIR, 'stre.js'))
        super().apply_args()

    def bind_all(self):
        if self.args.stre:
            self.mainwin.bind_object(STReHandler(self.mainwin.webroot), 'stre')


if __name__ == '__main__':
    app = STRapp(__app_name__, __version__, __app_desc__)
    app.run()
    app.wait()
