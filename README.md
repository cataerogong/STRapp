# STRapp - 让 SimpleTextReader 像本地应用程序一样运行

无须部署 Web 服务，只要有浏览器，即可让 SimpleTextReader 网页像本地应用程序一样运行。

## 安装&运行

1. 下载 SimpleTextReader

    * @henryxrl 的原版: https://github.com/henryxrl/SimpleTextReader/releases

    * 我的修改版: https://github.com/cataerogong/SimpleTextReader/releases

    下载并解压缩到某个目录。

2. 下载 `strapp.exe`

    将 `strapp.exe` 放到 SimpleTextReader 目录下，就是和 SimpleTextReader 的 `index.html` 同一个目录下。

3. 运行 `strapp.exe`，可以有多种方式：

    * 在命令提示符窗口中运行
    
      > 该模式下可以看到后台程序的运行输出信息

      ```
      cd /d D:\path\to\SimpleTextReader
      strapp.exe --port 8000
      ```

    * 快捷方式运行

      创建 `strapp.exe` 的快捷方式，然后修改快捷方式，在“目标”中添加参数 `--port 8000`

    * 使用参数文件运行

      在 `strapp.exe` 同目录下创建一个 `strapp.args` 文件，用记事本打开后添加 `--port 8000` 并保存，然后双击 `strapp.exe` 运行

## strapp.exe 详细参数说明

```
usage: strapp.exe [-h] [--webroot STR_ROOT] [--port PORT] [--browser BROWSER] [--stre]

options:
  -h, --help          show this help message and exit
  --webroot STR_ROOT  SimpleTextReader 主目录 [默认：当前目录]
  --port PORT         端口 [默认: 随机]
  --browser BROWSER   使用的浏览器（必须是本机已安装的）[默认: 系统缺省浏览器][可选项: NoBrowser, any, chrome, firefox, edge, safari,
                      chromium, opera, brave, vivaldi, epic, yandex, ChromiumBased]
  --stre              启用 SimpleTextReader-enhance 单机增强模式

【*注意*】用到了浏览器存储（如cookie,LocalStorage,indexdb），必须固定端口(--port)，否则会丢失设置。
```

* `--stre` SimpleTextReader-enhance 单机增强模式

  配合我的[修改版](https://github.com/cataerogong/SimpleTextReader/releases)(v1.6.0+)，可以直接读取本机硬盘上的文本文件，让 STRe 变成了一个独立的单机版txt小说阅读器。

## 彩蛋

* SPA (Single-page Application)

  其实，对于单静态页面的网页应用，都可以用 STRapp 来运行。只要把 `strapp.exe` 放到网页目录下，然后用恰当的参数运行 `strapp.exe` 就可以了。

## 感谢

* [webui](github.com/webui-dev/python-webui/)
