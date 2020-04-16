#!/usr/bin/env zsh
time=1585875813
time=$1

url=http://100.64.176.35:30900/api/v1/query?

queries=(
'avg%20by(app)%20(apm_memcached_qps)'
'avg%20by(app)%20(apm_memcached_latency)'
'(sum%20by(app)%20(avg_over_time(task_wss_referenced_bytes[15s])))/1000000000'
)

data=''

for query in $queries
do
  data+=$(curl -s $url'query='$query'&time='$time | jq '.data.result[0].value[1]')
done

echo ${data//\"/ }
