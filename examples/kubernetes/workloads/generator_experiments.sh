#!/usr/bin/env bash

current_date=$(date +%Y%m%d_%H%M%S)
mkdir $current_date

for ((count=13; count>=1; count--))
do

  records=$((1200000000/$count));value=1000;update=0;qps=10000;

  memory=$((1500000/$count));

  echo "Run memcached"
  for i in $(seq 1 $count); do
    sudo docker run -d --name=memcached-$i --net=host --rm --cpus=1 --cpuset-cpus=$((18+$i)) --memory=${memory}m memcached -t 1 -m $memory -v --port 112$((10+$i)); done

  sleep 10s;

  echo "Run mutilate"
  for j in $(seq 1 $count); do
    sudo docker run --name mutilate-stress-$j -d --rm --net=host --cpus=1 --cpuset-cpus=0-17 --memory=1g 100.64.176.12:80/wca/mutilate:master /bin/bash -c "./mutilate -T 1 -s 127.0.0.1:112$((10+$j)) -v -r $records -V $value --loadonly; ./mutilate -T 1 -s 127.0.0.1:112$((10+$j)) -v -r $records -V $value --scan $qps:$qps:0 --noload -u $update"; done

#  echo "EXP"
#  for k in $(seq 1 $count); do
#    sudo docker run --name mutilate-stress-$k -d --rm --net=host --cpus=1 --cpuset-cpus $cpus --memory=1g 100.64.176.12:80/wca/mutilate:master ./mutilate -T 1 -s 127.0.0.1:1121$i -v -r $records -V $value --scan $qps:$qps:0 --noload -u $update; done

  if  [ "$count" -eq "5" ] ; then
    sleep 150m;
  elif [ "$count" -eq "4" ] ; then
    sleep 190m;
  elif [ "$count" -eq "3" ] ; then
    sleep 240m;
  elif [ "$count" -eq "2" ] ; then
    sleep 330m;
  elif [ "$count" -eq "1" ] ; then
    sleep 2000m;
  else
    sleep 120m;
  fi

  sudo docker logs mutilate-stress-1 &> ${current_date}/log-${count}.log

  sudo docker kill memcached-{1..13}

  sleep 10s;

done
