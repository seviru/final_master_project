# In this folder we will store our scripts regarding the multiple alignment of the fastas previously extracted from our MongoDB

#### aligner.py: 
>It's a python script which makes a multiple alignment for the fasta of a given cluster name.<br />USAGE: `python aligner.py <CLUSTER_NAME> <PARTITION_WHERE_IT'S_STORED>`<br />NEEDED: Needs Mafft to align. If It isn't found, try: `module load MAFFT/7.429-GCC-8.2.0-2.31.1-with-extensions`

#### aligner.launcher.sh:
>It's a script used to run our script aligner.py in a computation cluster environment.<br />USAGE: (Inside the cluster)`sbatch -a 1-<CLUSTER_FILE_NUMBER_OF_LINES>%<MAX_NUMBER_OF_TASKS_RUNNING_AT_THE_SAME_TIME> -o <SLURM_OUT_FOLDER>/%A_%a.out -e <SLURM_ERROR_FOLDER>/%A_%a.err -t <HOURS:MINS:SECS_DEDICATED_TO_THE_JOB> aligner.launcher.sh <FILENAME_WITH_THE_CLUSTER_NAMES_AND_PARTITIONS>`<br />NEEDED: Already existing folders &#60;SLURM OUT FOLDER> and &#60;SLURM ERROR FOLDER>

#### aligner.sbatch_chunks.sh:
>It's a script used to run aligner.launcher.sh when we have more than 200.000 jobs to launch at once.<br />NEEDED: &#60;CHUNKSIZE>: Ammount of jobs that we want to send as if they were the same one.<br />&#60;RECORDS>: Number of individual jobs we wouls launch if we didnt group them: `(wc -l ../data/<OUTFILE>.txt | awk '{print $1});`<br />&#60;JOBS>: Number of jobs we will launch once we have grouped them:`((records/chunksize)+1);`<br />USAGE: `sbatch -a 1-${<JOBS>} -t <TIME> -o <SLURM_OUT_FOLDER>/%A_%a.out -e <SLURM_ERROR_FOLDER>/%A_%a.err ./aligner.sbatch_chunks.sh ../data/<OUTFILE>.txt ${<CHUNKSIZE>} ${<RECORDS>} aligner.launcher.sh` 

#### aligner.cheatsheet.sh:
>Cheatsheet on how to use aligner.sbatch_chunks.sh
