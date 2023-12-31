## v1.0.0

* 将应用框架完善成了一个独立的 package [webwin](https://github.com/cataerogong/webwin)，精简本项目的代码

## v0.3.0-wip

* [+] 增加从参数文件中读取运行参数

  如果在程序目录下存在与程序同名的 `.args` 文件（`程序名.args`），则先从该文件中读取运行参数，再读取命令行中的参数。

  优先级：命令行参数 > 参数文件 > 参数默认值

  参数文件格式：同命令行参数格式，可以换行

* [*] PyInstaller 打包参数更改

  `-w` 改为 `-c`，增加 `--hide-console hide-early` 参数，双击执行时不会显示 console 窗口，在命令行窗口执行时能显示 console 信息，方便调试和查找问题。

* [+] 增加 webui 相关的辅助代码，以方便前后端通讯

  后台增加 `webui_helper.py` 模块，前端应用主页增加插入 js 代码 `WEBUI_HELPER_JS`。

* [+] 增加 SimpleTextReader-enhance (v1.6.0-wip+) 适配

  利用 webui2 将 云端书库 改为 本地书架，替换掉首页的 浏览器缓存书架。

  原来 云端书库 的文件夹功能暂时还没想好怎么实现，暂缺。

## v0.2.0

* [+] 增加 ico

## v0.1.1

* [!] bugfix: 运行 `strapp.exe -h` 报错

  PyInstaller 打包成 exe 时使用 `-w` 参数打包成图形界面程序，没有 console 窗口可供输出 help 信息，导致报错。

  改为显示一个帮助网页。

## v0.1.0

  第一个可用的版本
