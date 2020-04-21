#!/usr/bin/env python3
"""Script that gets as input a specific gene cluster and    
Its partition, and checks if the alignment or tree file 
has been built correctly, and makes a report.           
"""

import sys 
import os
import sys


### USING THE CLUSTER NAME ###
cluster_name = sys.argv[1]
partition_number = sys.argv[2]
filetype = sys.argv[3]
BASE_PATH = "../data/partitions"


### FILE HANDLING THE INPUT AND OUTPUT FILES ###
if filetype == "trees":
    check_infile = f"{BASE_PATH}/{partition_number}/{filetype}/{cluster_name}.tree"
elif filetype == "alignments":
    check_infile = f"{BASE_PATH}/{partition_number}/{filetype}/{cluster_name}.fas.alg"
else:
    sys.exit("Wrong format file to erase")
okfile = f"{BASE_PATH}/{partition_number}/{filetype}/{cluster_name}.ok"


### MAIN ###
sys.stdout.write(f"cluster\tpartition\tokfile\t{filetype}_files\n")

if (os.path.exists(okfile) and os.path.exists(check_infile)) : # If both files are correct we delete none
    sys.stdout.write(f"{cluster_name}\t{partition_number}\tY\tY\n")
elif os.path.exists(check_infile): # If we just have one file we delete It
    sys.stdout.write(f"{cluster_name}\t{partition_number}\tN\tY\n")
elif os.path.exists(okfile):
    sys.stdout.write(f"{cluster_name}\t{partition_number}\tY\tN\n")
else: # If there is none file we exit
    sys.stdout.write(f"{cluster_name}\t{partition_number}\tN\tN\n")


## END