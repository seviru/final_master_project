#!/usr/bin/env python3
"""Script that gets as input a specific alignment and
builds a newick format tree for It.
"""

import sys 
from pathlib import Path
import os
import subprocess


### USING THE CLUSTER NAME ###
cluster_name = sys.argv[1]
partition_number = sys.argv[2]
BASE_PATH = "../data/partitions"


### FILE HANDLING THE INPUT AND OUTPUT FILES ###
Path(f"{BASE_PATH}/{partition_number}/trees").mkdir(parents=True, exist_ok=True)   # Create the folders if they dont exist
alignment_infile = f"{BASE_PATH}/{partition_number}/alignments/{cluster_name}.fas.alg"
tree_outfile = f"{BASE_PATH}/{partition_number}/trees/{cluster_name}.tree"    # Set the file output path
okfile = f"{BASE_PATH}/{partition_number}/trees/{cluster_name}.ok"


### MAIN ###
if os.path.exists(okfile): # If we have an OKfile for our alignment we dont execute It
    pass
else:
    if os.path.exists(tree_outfile): # If we have an alignment file but without OKfile It must be wrong, so we delete It
        os.remove(tree_outfile)
    tree_cmd = f"FastTree {alignment_infile} > {tree_outfile}" # We execute the alignment
    returncode = subprocess.call(tree_cmd,shell=True, executable="/bin/bash") 
    if returncode is 0: # If the alignment finishes without an error we create an OKfile
        okfile_outfile = open(okfile, "w")
        okfile_outfile.write("OK\n")
        okfile_outfile.close()
    else: # If the alignment finishes without a correct return code, we remove both files
        try:
            os.remove(okfile)
            os.remove(tree_outfile)
        except OSError:
            try:
                os.remove(tree_outfile)
            except OSError:
                pass


## END