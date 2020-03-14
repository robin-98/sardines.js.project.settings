#!/usr/bin/env python3
import os
import sys
import json

is_save = False
is_publish = False
is_link = False
is_unlink = False
target_name = None
message = '"sardine project automatic save point"'
if len(sys.argv) > 1:
    if sys.argv[1] == 'save':
        is_save = True
    if sys.argv[1] == 'link':
        is_link = True
    if sys.argv[1] == 'unlink':
        is_unlink = True
    if sys.argv[1] == 'publish':
        is_publish = True
        is_save = True
        is_link = True

if len(sys.argv) > 2:
    target_name = sys.argv[2]


sequence="sardines.core.js sardines.built-in-services.js sardines.compile-time-tools.js sardines.shoal.js sardines.service-provider.http.js sardines.service-driver.http.js state-engine sardines.test.js"
packages = {
    "state-engine": {
        "name": "state-engine",
        "links": [],
        "linkSelf": False,
    },
    "sardines.core.js": {
        "name": "sardines-core",
        "links": [],
        "linkSelf": True,
    },
    "sardines.built-in-services.js": {
        "name": "sardines-built-in-services",
        "links": ["sardines.core.js"],
        "linkSelf": True,
    },
    "sardines.compile-time-tools.js": {
        "name": "sardines-compile-time-tools",
        "links": ["sardines.core.js"],
        "linkSelf": True,
    },
    "sardines.shoal.js": {
        "name": "sardines-shoal",
        "links": ["sardines.core.js", "sardines.built-in-services.js", 'sardines.compile-time-tools.js'],
        "linkSelf": False,
    },
    "sardines.service-provider.http.js": {
        "name": "sardines-service-provider-http",
        "links": ["sardines.core.js"],
        "linkSelf": False,
    },
    "sardines.service-driver.http.js": {
        "name": "sardines-service-driver-http",
        "links": ["sardines.core.js"],
        "linkSelf": False,
    }
}


def get_proj_name(dir):
    return dir.replace('.js', '').replace('.', '-')

def exec_cmd(cmd, dir):
    print('------------ in', dir, '-------------')
    print(cmd)
    os.system('cd ' + dir + ';' + cmd + '; cd -')
    print('')

dir_list = sequence.split(' ')

for dir in dir_list:
    if target_name is not None and target_name != dir:
        continue

    if is_save:
        exec_cmd('git add . ; git commit -m ' + message + ' ; git push origin master', dir)
    if is_publish:
        if dir == "sardines.test.js":
            continue
        exec_cmd('rm -rf node_modules', dir)
        exec_cmd('npm i', dir)
        exec_cmd('npm version patch && npm publish', dir)
    if is_link and dir in packages:
        pkgSettings = packages[dir]
        for link in pkgSettings['links']:
            linkedPkgName = packages[link]["name"]
            exec_cmd('npm link '+linkedPkgName, dir)
        if pkgSettings["linkSelf"]:
            exec_cmd('npm link', dir)
    if is_unlink and dir in packages:
        if packages[dir]["linkSelf"]:
            exec_cmd('npm unlink', dir)

    

