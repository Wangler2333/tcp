#!/usr/bin/env python
# encoding=utf-8

import compileall


def compile_run():
    '''
    将当前目录下的py文件预编译为pyc文件
    :return:
    '''
    compileall.compile_dir(r'./')


if __name__ == '__main__':
    compile_run()
