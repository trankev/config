#!/bin/bash

set -ex

sudo -s -- <<EOF
ip route del default dev ppp0
echo "d mappy" > /var/run/xl2tpd/l2tp-control
ipsec down mappy
EOF
