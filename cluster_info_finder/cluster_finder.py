#!/usr/bin/env python3

"""Retrieve clusters (GMGC families) from MongoDB

Script to find all clusters (GMGC families) 
with minimum size (i.e. number of members or unigenes), 
specified as argument or by CL_MIN_SIZE.

Also, we will store only those clusters with hit to SwissProt.

In the output, along with the cluster name, a "partition number" is included for each cluster
Each partition will be shared by as many clusters as specified as argument or in CL_PARTITION_SIZE.
This number can be used, for example, to store clusters data under a tree of directories.
"""

__all__ = [] # no API
__author__ = "seviru"

import sys, argparse
from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT, CL_MIN_SIZE, CL_PARTITION_SIZE

### ARGUMENTS HANDLING
parser = argparse.ArgumentParser(description='Retrieve clusters with SwissProt hits, and organize them in partitions.')
parser.add_argument('--min_size', type=int, default=CL_MIN_SIZE,
                    help='minimum size of a cluster to be reported')
parser.add_argument('--min_sp_evalue', type=float, default=1e-1,
                    help='minimum e-value of SwissProt hit to report the cluster')
parser.add_argument('--partition_size', type=int, default=CL_PARTITION_SIZE,
                    help='number of clusters to include in a single partition')
args = parser.parse_args()

### MAIN
client = MongoClient(MONGO_HOST, MONGO_PORT)

try:
    partition_number = 0    # Number of partition we are writing in
    partition_counter = 0   # Partition counter to check we don't put more than needed files on each folder

    query = list(client.gmgc_clusters.members.find({"nu": {"$gte": args.min_size}}, {"_id": 0, "cl": 1}))

    for cluster in query:

        # We just want to store the cluster which have at least 1 unigene with an exact or best hit in swissprot
        
        unigenes_list = client.gmgc_clusters.members.find_one({"cl": cluster["cl"]}, {"_id": 0, "clm": 1})["clm"]
        for unigene in unigenes_list: # For all the unigenes of the cluster

            # Check if exact swissprot hit
            try:
                client.gmgc_unigenes.sprot_exact.find_one({"u": unigene}, {"_id": 0, "spe": 1})["spe"]
                partition_counter += 1
                sys.stdout.write(f"{cluster['cl']}\t{partition_number}\n")
                break # If the cluster has at least 1 hit of sprot_exact we save the cluster and check the next one
            
            except TypeError:

                # Check if best swissprot hit
                try:
                    spb_hit = client.gmgc_unigenes.sprot_best.find_one({"u": unigene}, {"_id": 0, "spb":1})
                    spb_n = spb_hit["spb"]["n"]
                    spb_ev = spb_hit["spb"]["ev"]
                    if spb_ev <= args.min_sp_evalue:
                        partition_counter += 1
                        sys.stdout.write(f"{cluster['cl']}\t{partition_number}\n")
                        break # If the cluster has at least 1 hit of sprot_best we save the cluster and check the next one
                
                except TypeError:
                    continue # If that unigene has not a hit on swissprot we check other unigene of the same cluster
                
        if partition_counter == CL_PARTITION_SIZE:
            partition_number += 1
            partition_counter = 0
            
finally:
    client.close()

## END
