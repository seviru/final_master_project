###############################################################
### Script to find all clusters with more than 10 unigenes, ###
### retrieve their name and store It on a file              ###
###############################################################

# MANUALLY DO THIS: module load Python/3.7.2-GCCcore-8.2.0
from pymongo import MongoClient
client = MongoClient("fat01", 27017)

query = client.gmgc_clusters.members.find({"nu": {"$gte": 10}}, {"_id": 0, "cl": 1})
import sys
for cluster in query: # We just want to store the cluster which have at least 1 unigene with an exact or best hit in swissprot
    swiss_hit = "N"
    unigenes_list = client.gmgc_clusters.members.find_one({"cl": cluster["cl"]}, {"_id": 0, "clm": 1})["clm"]
    for unigene in unigenes_list: # For all the unigenes of the cluster
        try:    # Try to retrieve exact swissprot hit
            client.gmgc_unigenes.sprot_exact.find_one({"u": unigene}, {"_id": 0, "spe": 1})["spe"]
            swiss_hit = "Y"
            break # If the cluster has at least 1 hit of sprot_exact we break to save that cluster
        except TypeError:

            try:    # Try to retrieve best swissprot hit
                client.gmgc_unigenes.sprot_best.find_one({"u": unigene}, {"_id": 0, "spb":1})["spb"]["n"]
                swiss_hit = "Y"
                break # If the cluster has at least 1 hit of sprot_best we break to save that cluster
            except TypeError:
                pass # If that unigene has not a hit on swissprot we check other unigene of the same cluster

    if swiss_hit is "Y": # If we have a swissprot hit we store the cluster on the file
        sys.stdout.write(f"{cluster['cl']}\n")