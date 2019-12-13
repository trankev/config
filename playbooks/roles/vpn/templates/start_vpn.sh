#!/bin/bash

set -ex
sudo -s -- <<EOF
set -ex
ipsec up mappy
echo "c mappy" > /var/run/xl2tpd/l2tp-control
ip route add {{ vpn_host }} via 192.168.1.1
while ! ip route add default dev ppp0; do
    sleep 0.3
done
EOF

