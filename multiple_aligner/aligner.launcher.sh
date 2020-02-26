#!/usr/bin/env bash

module load Python/3.7.2-GCCcore-8.2.0
module load MAFFT/7.429-GCC-8.2.0-2.31.1-with-extensions

### IF WE DON'T USE aligner.sbatch.sh WE HAVE TO UNCOMMENT THIS ###
#infile="$1";
#current=$(tail -n +${SLURM_ARRAY_TASK_ID} "$infile" | head -1);
#cluster=$(echo "$current" | cut -f 1);
#partition=$(echo "$current" | cut -f 2);

### IF WE USE aligner.sbatch.sh WE HAVE TO UNCOMMENT THIS ###
cluster="$1";
partition="$2";

### THIS LINE ALWAYS UNCOMMENTED ###
python aligner.py $cluster $partition

## END
