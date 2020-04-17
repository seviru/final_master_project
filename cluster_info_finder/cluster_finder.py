#!/usr/bin/env python3

"""Retrieve clusters (GMGC families) from MongoDB

Script to find all clusters (GMGC families) 
with minimum specified size (i.e. number of members or unigenes), 
retrieve their name and store it on a file.

Also, we will store only those clusters with hit to SwissProt.

The output is a list of clusters, including for each cluster
a partition number. Each partition will be shared by as many
clusters as specified in _PARTITION_SIZE
"""

__all__ = [] # no API
__author__ = "seviru"

import sys
from pymongo import MongoClient

from settings import MONGO_HOST, MONGO_PORT, CL_MIN_SIZE

# Constants

_PARTITION_SIZE = 10000      # Number of clusters we want to have on each partition

# Main

client = MongoClient(MONGO_HOST, MONGO_PORT)

try:
    partition_number = 0    # Number of partition we are writing in
    partition_counter = 0   # Partition counter to check we don't put more than needed files on each folder

    query = list(client.gmgc_clusters.members.find({"nu": {"$gte": CL_MIN_SIZE}}, {"_id": 0, "cl": 1}))

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
                    client.gmgc_unigenes.sprot_best.find_one({"u": unigene}, {"_id": 0, "spb":1})["spb"]["n"]
                    # TODO: filter by minimum evalue, score or identity
                    partition_counter += 1
                    sys.stdout.write(f"{cluster['cl']}\t{partition_number}\n")
                    break # If the cluster has at least 1 hit of sprot_best we save the cluster and check the next one
                
                except TypeError:
                    continue # If that unigene has not a hit on swissprot we check other unigene of the same cluster
                
        if partition_counter == _PARTITION_SIZE:
            partition_number += 1
            partition_counter = 0
finally:
    client.close()

## END
