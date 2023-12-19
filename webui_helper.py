import json
from webui import webui


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
    print(f'webui bind:', name)
