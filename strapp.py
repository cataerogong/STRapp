from datetime import datetime
import os
import os.path
import sys
import argparse
import shlex
import traceback
from webui import webui

from utils import open_any_enc

from webui_helper import comment_js_file, is_port_valid, webui_run_js, webui_show_html


APP_NAME = 'STRapp'
APP_VER = 'v0.2.0'
APP_DESC = 'STRapp - 让 SimpleTextReader 像本地应用程序一样运行'

LOG_FILE = APP_NAME + ".log"

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  # 判断当前执行程序是否是PyInstaller打包后的exe
    BUNDLE_DIR = sys._MEIPASS
    PROG_FILE = os.path.abspath(sys.executable)
else:
    BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROG_FILE = os.path.abspath(sys.argv[0])
PROG_NAME = os.path.splitext(os.path.basename(PROG_FILE))[0]
PROG_DIR = os.path.dirname(PROG_FILE)
ARGS_FILE = os.path.join(PROG_DIR, PROG_NAME + '.args')
LOG_FILE = os.path.join(PROG_DIR, PROG_NAME + '.log')
CUR_DIR = os.path.abspath(os.getcwd())


def log_ex(e: Exception):
	msg = traceback.format_exc()
	print(msg)
	with open(LOG_FILE, 'a') as l:
		l.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + msg + '\n')

def main():
	# 读取命令行参数
	parser = argparse.ArgumentParser(description=APP_DESC, add_help=False)
	parser.add_argument('-r', '--webroot', default='', help='网页根目录（支持相对路径或绝对路径）[默认: 当前目录]')
	parser.add_argument('-s', '--startpage', metavar='HTML_FILE', default='index.html', help='应用主页 [默认: index.html]')
	parser.add_argument('-p', '--port', type=int, default=0, help='端口 [默认: 随机]')
	parser.add_argument('-b', '--browser', default='any', help='使用的浏览器（必须是本机已安装的）[默认: 系统缺省浏览器][可选项: chrome, firefox, edge, safari, chromium, opera, brave, vivaldi, epic, yandex]')
	parser.add_argument('--width', type=int, default=0, help='窗口宽度 [默认: 上次运行时宽度]')
	parser.add_argument('--height', type=int, default=0, help='窗口高度 [默认: 上次运行时高度]')
	parser.add_argument('--js', metavar='ADD-ON.JS', nargs='*', default=[],  help='加载后执行 js 脚本文件（支持相对路径或绝对路径，支持多个文件）')
	parser.add_argument('--del-js', metavar='SCRIPT.JS', nargs='*', default=[], help='禁止主页加载的 js 脚本文件名（支持多个文件名）')
	parser.add_argument('--stre', action='store_true', help='启用针对 SimpleTextReader-enhance 特定补丁')
	parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')
	parser.epilog = '【*注意*】如果网页会用到浏览器存储（如cookie,LocalStorage,indexdb），则必须指定端口(-p,--port)'
	cfg = None
	if (os.path.exists(ARGS_FILE)):
		with open_any_enc(ARGS_FILE) as f:
			s = f.read()
		cfg = parser.parse_args(shlex.split(s, comments=True, posix=(os.name == 'posix')))
		print('args file:', cfg)
	cfg = parser.parse_args(namespace=cfg)
	print('args:', cfg)
	help_msg = f'<pre style="font-size:1rem;color:gray">{parser.format_help()}</pre><hr>[ <a href="https://github.com/cataerogong/STRapp" target="_blank">项目主页</a> ]'

	WEB_ROOT = os.path.normpath(os.path.join(CUR_DIR, cfg.webroot))
	START_PAGE = os.path.normpath(os.path.join(WEB_ROOT, cfg.startpage))
	BROWSER = webui.browser.__dict__.get(cfg.browser, webui.browser.any)

	# Create a window object
	MyWindow = webui.window()

	def show_html(html: str):
		webui_show_html(MyWindow, html, browser=BROWSER)

	def show_msg(msg: str='', add_help: bool=True):
		show_html(f'''<html>
			<head><meta charset="UTF-8" /><title>{APP_NAME} {APP_VER}</title></head>
			<body style="background:#fdf3df;">{msg}<hr>{help_msg if add_help else ""}</body>
			</html>''')

	if (cfg.help):
		show_msg()
	elif not is_port_valid(cfg.port):
		show_msg(f'<h1>端口被占用！</h1>【端口】{cfg.port}<br />请检查 -p 参数')
	elif not os.path.exists(START_PAGE):
		show_msg(f'<h1>应用主页文件不存在！</h1>【应用主页】{START_PAGE}<br />请检查 -r 和 -s 参数')
	else:
		MyWindow.set_port(cfg.port)
		MyWindow.set_size(cfg.width, cfg.height)
		MyWindow.set_root_folder(WEB_ROOT)
		# read page content
		with open_any_enc(START_PAGE) as f:
			html = str(f.read())
		if cfg.stre:
			import stre
			# bind
			stre.bind_funcs(MyWindow, WEB_ROOT)
			# patch page
			html = stre.patch_html(html)
		# del js
		for js in cfg.del_js:
			print('Comment js:', js)
			html = comment_js_file(html, js)
		# show page
		show_html(html)
		# run js
		try:
			if cfg.stre:
				stre.run_js(MyWindow)
			for js_file in [os.path.normpath(os.path.join(CUR_DIR, j)) for j in cfg.js]:
				webui_run_js(MyWindow, js_file)
		except Exception as e:
			log_ex(e)
			# show_msg(repr(e), False)

	# Wait until all windows are closed
	webui.wait()

	print('Bye')

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		log_ex(e)
