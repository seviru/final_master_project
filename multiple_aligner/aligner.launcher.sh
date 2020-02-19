#!/usr/bin/env bash

module load MAFFT/7.429-GCC-8.2.0-2.31.1-with-extensions

infile="$1";

current=$(tail -n +${SLURM_ARRAY_TASK_ID} "$infile" | head -1);
cluster=$(echo "$current" | cut -f 1);
partition=$(echo "$current" | cut -f 2);

python aligner.py $cluster $partition

## END
