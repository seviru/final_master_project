"""
Script that gets as input a specific gene cluster and
Its partition, and makes a multiple alignment for the
fasta file of that cluster.
"""

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
okfile = f"{BASE_PATH}/{partition_number}/alignments/{cluster_name}.ok"

### MAIN ###
import os
import subprocess   # To run bash commands inside Python

if os.path.exists(okfile): # If we have an OKfile for our alignment we dont execute It
    pass
else:
    if os.path.exists(alignment_outfile): # If we have an alignment file but without OKfile It must be wrong, so we delete It
        os.remove(alignment_outfile)
    alignment_cmd = f"mafft --anysymbol --auto {fasta_infile} > {alignment_outfile}" # We execute the alignment
    returncode = subprocess.call(alignment_cmd,shell=True, executable="/bin/bash") 
    if returncode is 0: # If the alignment finishes without an error we create an OKfile
        okfile_outfile = open (okfile, "w")
        okfile_outfile.write("OK\n")
        okfile_outfile.close()
    else: # If the alignment finishes without a correct return code, we remove both files
        try:
            os.remove(okfile)
            os.remove(alignment_outfile)
        except OSError:
            try:
                os.remove(alignment_outfile)
            except OSError:
                pass

## END