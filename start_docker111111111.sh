#!/bin/bash
set -eu

#DOCKER_IMAGE=dannadori/vcclient:20230602_014557
DOCKER_IMAGE=vcclient

### DEFAULT VAR ###
DEFAULT_EX_PORT=18888
DEFAULT_USE_GPU=on # on|off
DEFAULT_USE_LOCAL=off # on|off
### ENV VAR ###
EX_PORT=${EX_PORT:-${DEFAULT_EX_PORT}}
USE_GPU=${USE_GPU:-${DEFAULT_USE_GPU}}
USE_LOCAL=${USE_LOCAL:-${DEFAULT_USE_LOCAL}}





#!/bin/bash

command="docker run -it --rm --gpus all --shm-size=1024M \
    -v `pwd`/docker_vcclient/weights:/weights \
    -e EX_IP=`hostname -I` \
    -e EX_PORT=${EX_PORT} \
    -e LOCAL_UID=$(id -u $USER) \
    -e LOCAL_GID=$(id -g $USER) \
    -p ${EX_PORT}:18888 \
    $DOCKER_IMAGE -p 18888 --https true \
        --content_vec_500 pretrain/checkpoint_best_legacy_500.pt  \
        --hubert_base pretrain/hubert_base.pt \
        --hubert_soft pretrain/hubert/hubert-soft-0d54a1f4.pt \
        --nsf_hifigan pretrain/nsf_hifigan/model \
        --hubert_base_jp pretrain/rinna_hubert_base_jp.pt \
        --model_dir model_dir"

echo "The command is: $command"

#eval "$command"

"
docker run -it --rm --gpus all --shm-size=1024M     -v /mnt/c/Users/whousethispc/Desktop/master/Voice Changer Projectttt/voice-changer/docker_vcclient/weights:/weights     -e EX_IP=192.168.191.96      -e EX_PORT=18888     -e LOCAL_UID=1000     -e LOCAL_GID=1000     -p 18888:18888     vcclient -p 18888 --https true         --content_vec_500 pretrain/checkpoint_best_legacy_500.pt          --hubert_base pretrain/hubert_base.pt         --hubert_soft pretrain/hubert/hubert-soft-0d54a1f4.pt         --nsf_hifigan pretrain/nsf_hifigan/model         --hubert_base_jp pretrain/rinna_hubert_base_jp.pt         --model_dir model_dir

"
