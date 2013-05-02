#!/usr/bin/env bash
set -e 

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

version_name=$(date +%F.%H.%M.%S)
server="kjetil@kjetilvalle.com"
target="/home/kjetil/web/beertistics"

function info {
    echo -e "\n\033[32m$1\033[0m"
}

info "STAGING"
ssh ${server} "mkdir ${target}/${version_name}"
scp -r beertistics/* ${server}":"${target}"/"${version_name}"/"

info "UPDATING DEPENDENCIES"
scp -r requirements.txt ${server}":"${target}/
ssh ${server} "workon beertistics && cd ${target} && pip install -q -r requirements.txt"

info "RESTARTING"
scp -r beertistics.wsgi ${server}":"${target}/
ssh ${server} "cd ${target} && unlink beertistics && ln -s ${version_name} beertistics"
ssh -t ${server} "sudo service apache2 reload"

info "FINISHED"