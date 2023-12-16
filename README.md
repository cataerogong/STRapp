# STRapp - 让 SimpleTextReader 像本地应用程序一样运行

无须部署 Web 服务，只要有浏览器，即可让 SimpleTextReader 网页像本地应用程序一样运行。

## 安装&运行

1. 下载 SimpleTextReader

    * @henryxrl 的原版: https://github.com/henryxrl/SimpleTextReader/releases

    * 我的修改版: https://github.com/cataerogong/SimpleTextReader/releases

    下载并解压缩到某个目录。

2. 下载 strapp.exe

    将 strapp.exe 放到 SimpleTextReader 目录下，就是和 SimpleTextReader 的 index.html 同一个目录下。

3. 运行 strapp.exe，可以有多种方式：

    * 在命令提示符窗口中运行

    ```
    cd /d D:\path\to\SimpleTextReader
    strapp.exe -p 8000
    ```

    或者

    * 创建 strapp.exe 的快捷方式，然后修改快捷方式，在“目标”中添加参数 `-p 8000`

## strapp.exe 详细参数说明

```
usage: strapp [-r WEBROOT] [-s HTML_FILE] [--js JS_FILE] [-p PORT] [-b BROWSER]
              [--width WIDTH] [--height HEIGHT] [-h]

options:
  -r WEBROOT, --webroot WEBROOT
                        网页根目录（支持相对路径或绝对路径） [默认: 当前目录]
  -s HTML_FILE, --startpage HTML_FILE
                        应用主页 [默认: index.html]
  --js JS_FILE          加载后执行 js 脚本文件（支持相对路径或绝对路径）
  -p PORT, --port PORT  端口 [默认: 随机]
  -b BROWSER, --browser BROWSER
                        使用的浏览器（必须是本机已安装的） [默认: 系统缺省浏览器]
                        [可选项: chrome, firefox, edge, safari, chromium, opera, brave, vivaldi, epic, yandex]
  --width WIDTH         窗口宽度 [默认: 上次运行时宽度]
  --height HEIGHT       窗口高度 [默认: 上次运行时高度]
  -h, --help            显示帮助信息

【*注意*】如果网页会用到浏览器存储（如cookie,LocalStorage,indexdb），则必须指定端口(-p,--port)，因为不同的端口会被浏览器视为不同的网站。
```

## 彩蛋

* SPA (Single-page Application)

    其实，对于单静态页面的网页应用，都可以用 STRapp 来运行。只要把 strapp.exe 放到网页目录下，然后用恰当的参数运行 strapp.exe 就可以了。

## 感谢

* [WebUI2](github.com/webui-dev/python-webui/)
