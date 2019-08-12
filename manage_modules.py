#!/usr/bin/env python3
import os
import sys
import json

is_save = False
message = None
if len(sys.argv) > 1:
    if sys.argv[1] == 'save':
        is_save = True
        if len(sys.argv) > 2:
            message = sys.argv[2]
        else:
            message = '"sardine project automatic save point"'

sequence="sardines.core.js sardines.built-in-services.js sardines.compile-time-tools.js sardines.shoal.js sardines.shoal.service-provider.http.js sardines.shoal.service-driver.http.js"


def get_proj_name(dir):
    return dir.replace('.js', '').replace('.', '-')

def exec_cmd(cmd, dir):
    print('------------ in', dir, '-------------')
    print(cmd)
    os.system('cd ' + dir + ';' + cmd + '; cd -')
    print('')

dir_list = sequence.split(' ')

for dir in dir_list:
    if is_save:
        exec_cmd('git add . ; git commit -m ' + message + ' ; git push origin master', dir)


