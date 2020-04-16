#for i in 10g 15g 30g 40g 50g 60g 75g 80g
#do
#  kubectl --context cluster3 scale --replicas 8 statefulset memcached-mutilate-wss-"${i}"
#  sleep 40m
#  kubectl --context cluster3 scale --replicas 0 statefulset memcached-mutilate-wss-"${i}"
#  sleep 15s
#done
#
#for i in 10g 40g 50g 75g
#do
#    for j in 5 25 1 05
#    do
#      kubectl --context cluster3 scale --replicas 8 statefulset memcached-mutilate-wss-"${i}"-update-0"${j}"
#      sleep 40m
#      kubectl --context cluster3 scale --replicas 0 statefulset memcached-mutilate-wss-"${i}"-update-0"${j}"
#      sleep 15s
#    done
#done
#
#for i in 50g 60g 75g 80g
#do
#  kubectl --context cluster3 scale --replicas 8 statefulset memcached-mutilate-wss-"${i}"
#  sleep 80m
#  kubectl --context cluster3 scale --replicas 0 statefulset memcached-mutilate-wss-"${i}"
#  sleep 15s
#done

#for ((i = 1 ; i <= 30 ; i++)); do
#  kubectl --context cluster3 scale --replicas $i statefulset memcached-mutilate-wssm;
#  sleep 80m
#done

for ((i = 5 ; i <= 30 ; i++)); do
  kubectl --context cluster3 scale --replicas $i statefulset memcached-mutilate-wssm-"${i}";
  sleep 60m;
  kubectl --context cluster3 scale --replicas 0 statefulset memcached-mutilate-wssm-"${i}";
  sleep 10s;
done

for ((i = 5 ; i <= 30 ; i++)); do kubectl --context cluster3 scale --replicas $i statefulset memcached-mutilate-wssm-"${i}"; sleep 10s; kubectl --context cluster3 scale --replicas 0 statefulset memcached-mutilate-wssm-"${i}"; sleep 1s; done

for ((i = 5 ; i <= 30 ; i++)); do kubectl scale --replicas $i statefulset memcached-mutilate-wssm-"${i}"; sleep 60m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssm-"${i}"; sleep 20s; done

kubectl scale --replicas 11 statefulset memcached-mutilate-wssg-11; sleep 120m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-11; sleep 20s;
kubectl scale --replicas 10 statefulset memcached-mutilate-wssg-10; sleep 120m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-10; sleep 20s;
kubectl scale --replicas 9 statefulset memcached-mutilate-wssg-9; sleep 120m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-9; sleep 20s;
kubectl scale --replicas 8 statefulset memcached-mutilate-wssg-8; sleep 120m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-8; sleep 20s;
kubectl scale --replicas 7 statefulset memcached-mutilate-wssg-7; sleep 120m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-7; sleep 20s;
kubectl scale --replicas 6 statefulset memcached-mutilate-wssg-6; sleep 120m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-6; sleep 20s;
kubectl scale --replicas 5 statefulset memcached-mutilate-wssg-5; sleep 150m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-5; sleep 20s;
kubectl scale --replicas 4 statefulset memcached-mutilate-wssg-4; sleep 190m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-4; sleep 20s;
kubectl scale --replicas 3 statefulset memcached-mutilate-wssg-3; sleep 240m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-3; sleep 20s;
kubectl scale --replicas 2 statefulset memcached-mutilate-wssg-2; sleep 330m; kubectl scale --replicas 0 statefulset memcached-mutilate-wssg-2; sleep 20s;
kubectl scale --replicas 1 statefulset memcached-mutilate-wssg-1;

kubectl scale --replicas 12 statefulset memcached-mutilate-wss-ddr-g-12; sleep 70m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-12; sleep 20s;
kubectl scale --replicas 11 statefulset memcached-mutilate-wss-ddr-g-11; sleep 70m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-11; sleep 20s;
kubectl scale --replicas 10 statefulset memcached-mutilate-wss-ddr-g-10; sleep 70m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-10; sleep 20s;
kubectl scale --replicas 9 statefulset memcached-mutilate-wss-ddr-g-9; sleep 70m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-9; sleep 20s;
kubectl scale --replicas 8 statefulset memcached-mutilate-wss-ddr-g-8; sleep 70m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-8; sleep 20s;
kubectl scale --replicas 7 statefulset memcached-mutilate-wss-ddr-g-7; sleep 70m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-7; sleep 20s;
kubectl scale --replicas 6 statefulset memcached-mutilate-wss-ddr-g-6; sleep 70m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-6; sleep 20s;
kubectl scale --replicas 5 statefulset memcached-mutilate-wss-ddr-g-5; sleep 100m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-5; sleep 20s;
kubectl scale --replicas 4 statefulset memcached-mutilate-wss-ddr-g-4; sleep 140m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-4; sleep 20s;
kubectl scale --replicas 3 statefulset memcached-mutilate-wss-ddr-g-3; sleep 190m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-3; sleep 20s;
kubectl scale --replicas 2 statefulset memcached-mutilate-wss-ddr-g-2; sleep 280m; kubectl scale --replicas 0 statefulset memcached-mutilate-wss-ddr-g-2; sleep 20s;
kubectl scale --replicas 1 statefulset memcached-mutilate-wss-ddr-g-1;




while [ true ]; do kubectl --context cluster3 logs memcached-mutilate-wssf-4-0 mutilate -f; done

while [ true ]; do sudo docker logs mutilate-stress-1 -f; done



