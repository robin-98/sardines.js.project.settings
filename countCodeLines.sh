#!/usr/bin/env bash
if [[ "$1" == "pure" ]];then
    find . -name "*.ts" -print|grep -v node_modules|grep -v lib|grep src|xargs cat|awk '{if (NF > 0 && substr($1, 0, 2) != "//" && substr($1, 0 , 1) != "*" && $1 != "}" && substr($1, 0, 2) != "/*") print }'|wc -l
else
    find . -name "*.ts" -print|grep -v node_modules|grep -v lib|grep src|xargs cat|awk '{if (NF > 0) print }'|wc -l
fi
