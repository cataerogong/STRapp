import json
from os import PathLike
import os
import re
import socket
from webui import webui

from utils import open_any_enc


WEBUI_HELPER_JS = '''
/**
 *
 * @param {str} fname Backend bind name
 * @param  {...any} args
 * @returns
 */
async function webui_call_func(fname, ...args) {
    try {
        let ret = JSON.parse(await webui.call(fname, JSON.stringify(args)));
        if (ret.status == "succ") {
            return ret.retval;
        } else {
            throw Error("Backend-Error: " + ret.msg);
        }
    } catch (e) {
        // console.log(e);
        throw e;
    }
}
'''


def is_port_valid(p: int) -> bool:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind(('127.0.0.1', p))
		return True
	except OSError:
		return False
	finally:
		s.close()


def append_html(html: str, append_str: str) -> str:
	""" 在页面末尾 "</html>" 前插入字符串

    append_str</html>
	"""
	p = html.lower().rfind('</html>')
	if p >= 0:
		html = html[:p] + append_str + html[p:]
	return html


def append_js(html: str, js_file: str = '', js_str: str = '') -> str:
    """ 在页面末尾 "</html>" 前插入 "载入 js_file 和 js_str" 的 <script> 语句

    <script src="js_file"></script>
    <script>
    js_str
    </script>
    </html>
    """
    if js_file:
        html = append_html(html, f'<script src="{js_file}"></script>\n')
    if js_str:
        html = append_html(html, f'<script>\n{js_str}\n</script>\n')
    return html


def inject_webui_js(html: str) -> str:
    """ 在 html 末尾增加载入 webui 功能的代码 """
    return append_js(html, '/webui.js', WEBUI_HELPER_JS)

def comment_html(html: str, regex_to_comment: str, regex_flags=re.IGNORECASE) -> str:
    """ 在 html 内搜索正则表达式并注释掉

    "some string" => "<!-- some string -->"
    """
    m = re.search(regex_to_comment, html, regex_flags)
    if m:
        return html[:m.start()] + '<!-- ' + html[m.start():m.end()] + ' -->' + html[m.end():]
    else:
        print(regex_to_comment)
        return html

def comment_js_file(html: str, js_file: str) -> str:
    """ 将 html 内加载 js_file 的语句注释掉

    "<script src="js_file"></script>" => "<!-- <script src="js_file"></script> -->"
    """
    safe_str = js_file.replace('.', '\\.')
    return comment_html(html, f'''<script\\s+.+{safe_str}["']>\\s*</script>''')

def webui_show_html(win: webui.window, html: str, browser: webui.browser = webui.browser.any, append_webui_js: bool = True):
    """ 打开浏览器并展示 html 页面内容

    Args:
        win (webui.window): 浏览器窗口对象
        html (str): 页面内容字符串
        browser (webui.browser): 浏览器类型
        append_webui_js (bool): 是否在 HTML 末尾插入 webui 功能 js 代码
    """
    if append_webui_js:
        html = inject_webui_js(html)
    win.show(html, browser)

def webui_bind_func(win: webui.window, name: str, f, debug: bool = False):
    def wrapper(e: webui.event):
        args_j = e.window.get_str(e, 0)
        if debug:
            print(f"Call from JavaScript: {name} {args_j}")
        args = json.loads(args_j) if args_j else []
        try:
            retval = f(*args)
            if debug:
                print('Return:', repr(retval))
            return json.dumps({'status': 'succ', 'retval': retval}, ensure_ascii=False)
        except Exception as ex:
            return json.dumps({'status': 'fail', 'msg': repr(ex)}, ensure_ascii=False)
    win.bind(name, wrapper)
    print('webui bind:', name)

def webui_run_js(win: webui.window, js_file: PathLike):
    """ 在页面执行 js 脚本

    Args:
        js_file (PathLike): js 脚本文件

    Returns:
        (any) js return value

    Raises:
        FileNotFoundError:
		Exception: js error
    """
    if not os.path.exists(js_file):
        raise FileNotFoundError(js_file)
    with open_any_enc(js_file) as f:
        print("webui run js:", js_file)
        res = win.script(str(f.read()))
        if res.error is True:
            raise Exception(f'webui run js "{js_file}" error: {repr(res.data)}')
        return res.data
