# In this folder we will store our scripts regarding the multiple tree building and annotating from our alignment files

#### tree_builder.py:
It's a python script which builds a tree for the alignment of a given cluster name.
<br />USAGE: 
```
python tree_builder.py  <CLUSTER_NAME> 
                        <PARTITION_WHERE_IT'S_STORED>`
```
NEEDED: Needs FastTree to align. If It isn't found, try: `module load FastTree/2.1.11-GCC-8.2.0-2.31.1`

#### tree_builder.launcher.sh:
It's a script used to run our script tree_builder.py in a computation cluster environment.
<br />USAGE: (Inside the cluster)
```
sbatch  -a 1-<CLUSTER_FILE_NUMBER_OF_LINES>%<MAX_NUMBER_OF_TASKS_RUNNING_AT_THE_SAME_TIME> 
        -o <SLURM_OUT_FOLDER>/%A_%a.out 
        -e <SLURM_ERROR_FOLDER>/%A_%a.err 
        -t <HOURS:MINS:SECS_DEDICATED_TO_THE_JOB> 
        tree_builder.launcher.sh 
        <FILENAME_WITH_THE_CLUSTER_NAMES_AND_PARTITIONS>
```
<br />NEEDED: Already existing folders &#60;SLURM_OUT_FOLDER> and &#60;SLURM_ERROR_FOLDER>

#### tree_builder.sbatch_chunks.sh:
It's a script used to run tree_builder.launcher.sh when we have more than 200.000 jobs to launch at once.
<br />NEEDED: 
- &#60;CHUNKSIZE>: Ammount of jobs that we want to send as if they were the same one.
- &#60;RECORDS>: Number of individual jobs we wouls launch if we didnt group them. `(wc -l ../data/<OUTFILE>.txt | awk '{print $1});`
- &#60;JOBS>: Number of jobs we will launch once we have grouped them. `((records/chunksize)+1);`
<br />USAGE: 
```
sbatch  -a 1-${<JOBS>} 
        -t <TIME> 
        -o <SLURM_OUT_FOLDER>/%A_%a.out 
        -e <SLURM_ERROR_FOLDER>/%A_%a.err 
        ./tree_builder.sbatch_chunks.sh 
        ../data/<OUTFILE>.txt 
        ${<CHUNKSIZE>} 
        ${<RECORDS>} tree_builder.launcher.sh` 
```

#### tree_builder.cheatsheet.sh:
Cheatsheet on how to use aligner.sbatch_chunks.sh
