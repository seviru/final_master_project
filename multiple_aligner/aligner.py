###############################################################
### Script that gets as input a specific gene cluster and   ### 
### Its partition, and makes a multiple alignment for the   ###
### fasta file of that cluster.                             ###
###############################################################

### MANUALLY DO: module load MAFFT/7.429-GCC-8.2.0-2.31.1-with-extensions

### USING THE CLUSTER NAME ###
import sys 
cluster_name = sys.argv[1]
partition_number = sys.argv[2]
BASE_PATH = "../data/partitions"

### FILE HANDLING THE INPUT AND OUTPUT FILES ###
from pathlib import Path
Path(f"{BASE_PATH}/{partition_number}/alignments").mkdir(parents=True, exist_ok=True)   # Create the folders if they dont exist
fasta_infile = f"{BASE_PATH}/{partition_number}/fastas/{cluster_name}.fas"
alignment_outfile = f"{BASE_PATH}/{partition_number}/alignments/{cluster_name}.fas.alg"    # Set the file output path

import os
try:    # Remove the folders if they exist, to not mix already existing files
    os.remove (alignment_outfile)
except OSError:
    pass

### DO THE ALIGNMENT AND SAVE IT###
import subprocess   # To run bash commands inside Python
alignment_cmd = f"mafft --auto {fasta_infile} > {alignment_outfile}"
subprocess.call(alignment_cmd,shell=True, executable="/bin/bash")