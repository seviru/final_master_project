"""
Script that gets as input a specific gene cluster and    
Its partition, and checks if the alignment ir tree file 
has been built correctly. If It hasn't, It removes the 
wrongly written files.                               
"""

### USING THE CLUSTER NAME ###
import sys 
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
import os

if (os.path.exists(okfile) and os.path.exists(check_infile)) : # If both files are correct we delete none
    sys.exit(0)
elif os.path.exists(check_infile): # If we just have one file we delete It
    os.remove(check_infile)
elif os.path.exists(okfile):
    os.remove(okfile)
else: # If there is none file we exit
    sys.exit(0)

## END