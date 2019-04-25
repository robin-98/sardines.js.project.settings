import os
import sys
import json

is_linking_modules = False
is_unlink = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'link':
        is_linking_modules = True
    elif sys.argv[1] == 'unlink':
        is_unlink = True

# module dependency relationships
# test -> (
#   (provider, driver) -> shoal -> (sardines, compiler)
# ) -> utils
sequence="sardines.utils.js sardines.compiler.js sardines.js sardines.shoal.js sardines.shoal.service-provider.http.js sardines.shoal.service-driver.http.js sardines.test.js"

local_dependencies = {}
local_dependencies["sardines-utils"]=""
local_dependencies["sardines-compiler"]="sardines-utils"
local_dependencies["sardines"]="sardines-utils"
local_dependencies["sardines-compiler"]="sardines-utils"
local_dependencies["sardines-shoal"]="sardines-utils sardines sardines-compiler"
local_dependencies["sardines-shoal-service-provider-http"]="sardines-utils sardines-shoal"
local_dependencies["sardines-shoal-service-driver-http"]="sardines-utils sardines-shoal"
local_dependencies["sardines-test"]="sardines-utils sardines sardines-compiler sardines-shoal sardines-shoal-service-provider-http sardines-shoal-service-driver-http"

package_version_dict = {}

def exec_cmd(cmd, proj):
    print('------------ in', proj, '-------------')
    print(cmd)
    os.system(cmd)
    print('')

dir_list = sequence.split(' ')
if is_unlink:
    dir_list.reverse()

for dir in dir_list:
    proj = dir.replace('.js', '').replace('.', '-')
    local_dep_list = local_dependencies[proj]

    print('=================== start', proj, '==================')
    if is_unlink:
        if proj != 'sardines-test':
            exec_cmd('npm unlink', proj)

    dependencies = {}
    if len(local_dep_list) > 0:
        dependencies["local"] = local_dep_list.split(' ')
    else:
        dependencies["local"] = []

    package = {}
    with open('./' + dir +'/package.json', 'r') as f:
        package = json.load(f)
        for (t, name) in [('dependencies', 'main'), ('devDependencies', 'dev')]:
            if t in package:
                dependencies[name] = []
                for k in package[t]:
                    if k not in dependencies["local"]:
                        dependencies[name].append(k + '@' + package[t][k])

    if is_linking_modules:
        with open('./' + dir +'/package.json', 'w') as f:
            package['name'] = proj
            for k in dependencies['local']:
                if k in package['dependencies'] and k in package_version_dict:
                    package['dependencies'][k] = "file:../" + package_version_dict[k]["folder"]
            json.dump(package, f, indent=4, sort_keys=True)

    package_version_dict[proj] = {"version": package['version'], "folder": dir}

    if is_linking_modules:
        exec_cmd('cd ' + dir + ' && rm -rf ./node_modules && rm -f ./package-lock.json', proj)

    if not is_unlink:
        for t in ['main', 'dev']:
            if t in dependencies:
                for package in dependencies[t]:
                    exec_cmd("cd " + dir + " && npm install " + package, proj)            

    for local_proj in dependencies["local"]:
        if is_unlink:
            exec_cmd("cd " + dir + " && npm unlink " + local_proj, proj)
        else:
            exec_cmd("cd " + dir + " && npm link " + local_proj, proj)

    if not is_unlink and proj != "sardines-test":
        exec_cmd("cd " + dir + " && npm link", proj)

    print('=================== end', proj, '==================')
    print('')
    print('')
