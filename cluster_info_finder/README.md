
# In this folder we have various scripts and subfolders where we will store plenty of data regarding the parsing of our MongoDB to extract specific information from gene clusters.

### settings_example.py:
A python script used as a config file. It must be configured properly and renamed to `settings.py`.

### cluster_finder.py:
It's a python script which querys to search all the clusters with more than 10 unigenes, and save all of the cluster names in a specified file.
<br />USAGE: 
```
python cluster_finder.py [-h] [--min_size MIN_SIZE]
                         [--min_sp_evalue MIN_SP_EVALUE]
                         [--partition_size PARTITION_SIZE]
			 > <OUTFILE>
```
NEEDED: Python 3.7. If It fails, try: 
```
module load Python/3.7.2-GCCcore-8.2.0`
```

### cluster_finder.launcher.sh:
It's a bash script used to run our `cluster_finder.py` script in a computation cluster environment.
<br />USAGE: (Inside the cluster)
```
sbatch  -o <OUTPUTFILE> 
	-t <HOURS:MINS:SECS_DEDICATED_TO_THE_TASK> 
	cluster_finder.launcher.sh`
```

### cluster_info_retriever.py: 
It's a python script which for a given input cluster name will search for information regarding all the unigenes It contains, creating a `FASTA` (.fas) file with the sequence of all the unigenes as well as the best protein hit from swissprot, and a `TABLE` (.tsv) file with the best hit for each unigene found. The `FASTA` file will be stored in a new created folder called "fastas" and the `TABLE` file will be stored in a new created folder called "tables".<br />USAGE: 
```
python cluster_info_retriever.py <CLUSTER_NAME>`
```
NEEDED: Python 3.7. If It fails, try: 
```
module load Python/3.7.2-GCCcore-8.2.0`
```

### cluster_info_retriever.launcher.sh: 
It's a script used to run our script `cluster_info_retriever.py` in a computation cluster environment.<br />USAGE: (Inside the cluster)
```
sbatch  -a 1-<CLUSTER_FILE_NUMBER_OF_LINES> 
	-o <SLURM_OUT_FOLDER>/%A_%a.out 
	-e <SLURM_ERROR_FOLDER>/%A_%a.err 
	-t <HOURS:MINS:SECS_DEDICATED_TO_THE_JOB> 
	cluster_info_retriever.launcher.sh 
	<FILENAME_WITH_THE_CLUSTER_NAMES_,_A.K.A._<OUTFILE>.txt>`
```
NEEDED: Already existing folders `<SLURM_OUT_FOLDER>` and `<SLURM_ERROR_FOLDER>`

### sbatch_chunks.sh: 
It's a script used to run more than 200.000 jobs at the same time in our slurm computational cluster. It's a little more complex to call than the other ones, since It needs more variables.<br />NEEDED: 
- `<CHUNKSIZE>`: Ammount of jobs that we want to send as if they were the same one.
- `<RECORDS>`: Number of individual jobs we wouls launch if we didnt group them. `(wc -l ../data/<OUTFILE>.txt | awk '{print $1});`
- `<JOBS>`: Number of jobs we will launch once we have grouped them `((records/chunksize)+1);`
<br />USAGE: 
```
sbatch  -a 1-${<JOBS>} 
	-t <TIME> 
	-o <SLURM_OUT_FOLDER>/%A_%a.out 
	-e <SLURM_ERROR_FOLDER>/%A_%a.err 
	./cluster_info_retriever.sbatch_chunks.sh 
	../data/<OUTFILE>.txt 
	${<CHUNKSIZE>} 
	${<RECORDS>} 
	cluster_info_retriever.launcher.sh
```

### &#60;OUTFILE>.txt: 
We will have a .txt file in this folder containing the clusters list which meet the requirements of the `cluster_finder.py` script and the partition they will go in the next step.

### ./&#60;SLURM_OUT_FOLDER>/: 
Folder where we will store the output from running in batch our script `cluster_info_retriever.launcher.sh` . In our case is `./slurm_out/`

### ./&#60;SLURM_ERROR_FOLDER>/:
Folder where we will store the errors from running in batch our script `cluster_info_retriever.launcher.sh` . In our case is `./slurm_err/`

### cluster_info_retriever.cheatsheet.sh:
Instructions on how to use `cluster_info_retriever.sbatch_chunks.sh` in more detail.
