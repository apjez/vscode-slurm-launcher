#!/bin/bash

SLURM_ROOT=/path/to/slurm/install

PORT=$(shuf -i 50000-60000 -n 1);
while $(nc -zvw2 localhost ${PORT} &> /dev/null)
do
  PORT=$(shuf -i 50000-60000 -n 1)
done

# Create a random string to append to the job name for mapping
HASH=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13; echo)

${SLURM_ROOT}/bin/sbatch -J"vscode-${HASH}" ${RG_VSC_LAUNCH} -o %x.out  --wrap "declare -px > /tmp/env.sh; /usr/sbin/sshd -D -p ${PORT} -f /dev/null -h ${HOME}/.ssh/id_rsa"

while [[ -z "$(${SLURM_ROOT}/bin/squeue --me --name="vscode-${HASH}" --states=R -h -O NodeList)" ]]; do
  /usr/bin/sleep 5
done

ALLOC_HOST=$(${SLURM_ROOT}/bin/scontrol show hostnames $(${SLURM_ROOT}/bin/squeue --me --name="vscode-${HASH}" --states=R -h -o %N) | head -n1)

nc -w 300 ${ALLOC_HOST} ${PORT}

${SLURM_ROOT}/bin/scancel --name="vscode-${HASH}"
rm "vscode-${HASH}.out"
