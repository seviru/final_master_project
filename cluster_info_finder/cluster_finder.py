###############################################################
### Script to find all clusters with more than 10 unigenes, ###
### retrieve their name and store It on a file              ###
###############################################################

# MANUALLY DO THIS: module load Python/3.7.2-GCCcore-8.2.0
from pymongo import MongoClient
client = MongoClient("fat01", 27017)

query = client.gmgc_clusters.members.find({"nu": {"$gte": 10}}, {"_id": 0, "cl": 1}).limit(100)

import sys
partition_size = 10      # Number of clusters we want to have on each partition
partition_number = 0    # Number of partition we are writing in
partition_counter = 0   # Partition counter to check we don't put more than needed files on each folder

for cluster in query: # We just want to store the cluster which have at least 1 unigene with an exact or best hit in swissprot
    unigenes_list = client.gmgc_clusters.members.find_one({"cl": cluster["cl"]}, {"_id": 0, "clm": 1})["clm"]
    for unigene in unigenes_list: # For all the unigenes of the cluster
        try:    # Try to retrieve exact swissprot hit
            client.gmgc_unigenes.sprot_exact.find_one({"u": unigene}, {"_id": 0, "spe": 1})["spe"]
            partition_counter += 1
            sys.stdout.write(f"{cluster['cl']}\t{partition_number}\n")
            break # If the cluster has at least 1 hit of sprot_exact we save the cluster and check the next one
        except TypeError:

            try:    # Try to retrieve best swissprot hit
                client.gmgc_unigenes.sprot_best.find_one({"u": unigene}, {"_id": 0, "spb":1})["spb"]["n"]
                partition_counter += 1
                sys.stdout.write(f"{cluster['cl']}\t{partition_number}\n")
                break # If the cluster has at least 1 hit of sprot_best we save the cluster and check the next one
            except TypeError:
                continue # If that unigene has not a hit on swissprot we check other unigene of the same cluster
    if partition_counter == partition_size:
        partition_number += 1
        partition_counter = 0