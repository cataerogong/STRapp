import chardet

def detect_enc(filename, default_encoding='ascii'):
    """ 自动识别文件编码

    :param default_encoding: (str) 万一没有识别出文件编码时使用的缺省编码
    """
    r = None
    with open(filename, 'rb') as f:
        d = chardet.UniversalDetector()
        for l in f:
            d.feed(l)
            if d.done:
                break
        r = d.close()
    # 经常把 GBK 识别成 GB2312，gb18030 > gbk > gb2312
    return (d.LEGACY_MAP.get(r['encoding'].lower(), r['encoding']) if r and r['encoding'] else default_encoding)

def open_any_enc(filename, mode='r', default_encoding='ascii'):
    """ open “自动识别文件编码”版本

    :param default_encoding: (str) 万一没有识别出文件编码时使用的缺省编码
    """
    return open(filename, mode, encoding=detect_enc(filename, default_encoding))
