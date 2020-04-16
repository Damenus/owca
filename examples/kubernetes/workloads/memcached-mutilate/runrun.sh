sudo docker run -it --net=host --rm --cpus=1 --memory=42g memcached -t 1 -m 42G

sudo docker run -it --rm --net=host --cpus=1 --memory=1g 100.64.176.12:80/wca/mutilate:master /bin/bash -c "shopt -s extglob; ./mutilate -T 1 -s 127.0.0.1:11211 -v -r 34285714 -V 1000 --loadonly ; ./mutilate -c 1 -T 1 -t 1 -s 127.0.0.1:11211 --noload --scan 0:0:0 -r 34285714 -V 1000 -u 0 "

pagemon do wyświetlania page