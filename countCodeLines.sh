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

tsCnt=`countLines ts src $1`
if [ $tsCnt -gt 0 ];then
    echo TypeScript code: ${tsCnt} lines
fi

jsCnt=`countLines js src $1`
if [ $jsCnt -gt 0 ];then
    echo JavaScript code: ${jsCnt} lines
fi

jsTestCnt=`countLines js test $1`
tsTestCnt=`countLines ts test $1`
jsonTestCnt=`countLines json test $1`
confTestCnt=`countLines conf test $1`
testCnt=`expr ${jsTestCnt} + ${tsTestCnt} + ${jsonTestCnt} + ${confTestCnt}`
if [ $testCnt -gt 0 ];then
    echo Test code: ${testCnt} lines
fi

pyCnt=`countLines py . $1`
if [ $pyCnt -gt 0 ];then
    echo Python code: ${pyCnt} lines
fi

mdCnt=`countLines md . $1`
if [ $mdCnt -gt 0 ];then
    echo Documentation: ${mdCnt} lines
fi

echo All: `expr ${tsCnt} + ${jsCnt} + ${testCnt} + ${pyCnt} + ${mdCnt}` lines
