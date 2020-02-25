#!/usr/bin/env bash

module load Python/3.7.2-GCCcore-8.2.0;

### IF WE DON'T USE cluster_info_retriever.sbatch.sh WE HAVE TO UNCOMMENT THIS ###
#infile="$1";
#current=$(tail -n +${SLURM_ARRAY_TASK_ID} "$infile" | head -1);
#current="$1";
#cluster=$(echo "$current" | cut -f 1);
#partition=$(echo "$current" | cut -f 2);

### IF WE USE cluster_info_retriever.sbatch.sh WE HAVE TO UNCOMMENT THIS ###
cluster="$1";
partition="$2";
python cluster_info_retriever.py $cluster $partition;

## END


