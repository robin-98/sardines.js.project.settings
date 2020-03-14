#!/usr/bin/env bash
countLines() {
    extname=$1
    targetDir=$2
    countType=$3
    ( if [[ "$countType" == "pure" ]];then
          find . -name "*.${extname}" -print|grep -v node_modules|grep -v lib|grep "${targetDir}"|xargs cat|awk '{if (NF > 0 && substr($1,0,1) != "#" && substr($1, 0, 2) != "//" && substr($1, 0 , 1) != "*" && $1 != "}" && substr($1, 0, 2) != "/*") print }'|wc -l
      elif [[ "${countType}" == "noblank" ]];then
         find . -name "*.${extname}" -print|grep -v node_modules|grep -v lib|grep "${targetDir}"|xargs cat|awk '{if (NF > 0) print }'|wc -l
      else
         find . -name "*.${extname}" -print|grep -v node_modules|grep -v lib|grep "${targetDir}"|xargs cat|wc -l
      fi )|awk '{print $1}'
}

jsCnt=`countLines ts src $1`
echo JS code: ${jsCnt} lines

pyCnt=`countLines py . $1`
echo Py code: ${pyCnt} lines

mdCnt=`countLines md . $1`
echo Documentation: ${mdCnt} lines

echo All: `expr ${jsCnt} + ${pyCnt} + ${mdCnt}` lines
