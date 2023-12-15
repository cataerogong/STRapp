from datetime import datetime
import os
import os.path
import sys
import argparse
import socket
from webui import webui

from utils import open_any_enc

APP_VER = '0.1.1'

CUR_DIR = os.path.abspath(os.getcwd())
APP_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]

def is_port_valid(p: int):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind(('127.0.0.1', p))
		return True
	except OSError:
		return False
	finally:
		s.close()

def show_msg_win(win: webui.window, msg: str, browser):
	win.show(f'<html><head><meta charset="UTF-8" /><title>{APP_NAME} v{APP_VER}</title></head><body style="background:#fdf3df;color:#111111;">{msg}<script src="/webui.js"></script></body></html>', browser)

def main():
	# 读取命令行参数
	parser = argparse.ArgumentParser(description='STRapp - 让 SimpleTextReader 像本地应用程序一样运行', add_help=False)
	parser.add_argument('-r', '--webroot', default='', help='网页根目录（支持相对路径或绝对路径）[默认: 当前目录]')
	parser.add_argument('-s', '--startpage', metavar='HTML_FILE', default='index.html', help='应用主页 [默认: index.html]')
	parser.add_argument('--js', metavar='JS_FILE', help='加载后执行 js 脚本文件（支持相对路径或绝对路径）')
	parser.add_argument('-p', '--port', type=int, default=0, help='端口 [默认: 随机]')
	parser.add_argument('-b', '--browser', default='any', help='使用的浏览器（必须是本机已安装的）[默认: 系统缺省浏览器][可选项: chrome,firefox,edge,safari,chromium,opera,brave,vivaldi,epic,yandex]')
	parser.add_argument('--width', default=0, help='窗口宽度 [默认: 上次运行时宽度]')
	parser.add_argument('--height', default=0, help='窗口高度 [默认: 上次运行时高度]')
	parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')
	parser.epilog = '【*注意*】如果网页会用到浏览器存储（如cookie,LocalStorage,indexdb），则必须指定端口(-p,--port)'
	cfg = parser.parse_args()
	print('args:', cfg)
	help_msg = f'<pre style="font-size:1rem;color:gray">{parser.format_help()}</pre>'

	WEB_ROOT = os.path.normpath(os.path.join(CUR_DIR, cfg.webroot))
	START_PAGE = os.path.normpath(os.path.join(WEB_ROOT, cfg.startpage))
	BROWSER = webui.browser.__dict__.get(cfg.browser, webui.browser.any)

	# Create a window object
	MyWindow = webui.window()
	MyWindow.set_port(cfg.port)
	MyWindow.set_size(cfg.width, cfg.height)
	MyWindow.set_root_folder(WEB_ROOT)

	if (cfg.help):
		show_msg_win(MyWindow, help_msg, BROWSER)
	elif not is_port_valid(cfg.port):
		show_msg_win(MyWindow, f'<h1>端口已被占用！</h1>PORT: ({cfg.port})<hr>{help_msg}', BROWSER)
	elif not os.path.exists(START_PAGE):
		show_msg_win(MyWindow, f'<h1>应用主页文件不存在！</h1>START_PAGE: ({START_PAGE})<hr>{help_msg}', BROWSER)
	else:
		# 在页面末尾增加载入 webui.js，关闭窗口时才能结束进程
		with open_any_enc(START_PAGE) as f:
			html = str(f.read())
			html = html.replace('</html>', '<script src="/webui.js"></script></html>')
			MyWindow.show(html, BROWSER)
		# print('js-file:', cfg.js)
		if (cfg.js):
			js_file = os.path.normpath(os.path.join(CUR_DIR, cfg.js))
			if os.path.exists(js_file):
				with open_any_enc(js_file) as f:
					MyWindow.script(f.read())

	# Wait until all windows are closed
	webui.wait()

	print('Bye')

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		import traceback
		msg = traceback.format_exc()
		print(msg)
		with open(os.path.join(CUR_DIR, APP_NAME + '.log'), 'a') as l:
			l.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + msg + '\n')
