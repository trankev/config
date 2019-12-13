#!/bin/bash
# -*- coding: utf-8 -*-

set -o errexit
set -o nounset
set -o pipefail

function put_link {
    link=$1
    dest=$2
    [[ -e $(dirname ${dest}) ]] || mkdir -p $(dirname ${dest})
    if [[ -e ${dest} && $(readlink ${dest}) == ${config_folder}/${config_file} ]] ; then
        ln -sfn ${config_folder}/${config_file} ${dest}
    else
        ln -sbfn ${config_folder}/${config_file} ${dest}
    fi

}

pushd .
    cd ~/config
    git submodule update --init --recursive
popd

config_folder="${HOME}/config/config"
for config_file in $(ls ${config_folder}); do
    path="${HOME}/.$(echo ${config_file} | tr ':' '/')"
    put_link ${config_folder}/${config_file} ${path}
done

if [[ $# -ge 1 ]] ; then
    uncommonrc=${HOME}/config/uncommonrc/$1
    put_link ${uncommonrc} ${HOME}/.uncommonrc
fi


mkdir -p ~/.ssh/cm_socket

youcompleteme_folder=~/.vim/bundle/YouCompleteMe
if [ ! -f ${youcompleteme_folder}/third_party/ycmd/ycm_core.so ]; then
    python3 ${youcompleteme_folder}/install.py
fi
