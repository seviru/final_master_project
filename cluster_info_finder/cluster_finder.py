###############################################################
### Script to find all clusters with more than 10 unigenes, ###
### retrieve their name and store It on a file              ###
###############################################################

# MANUALLY DO THIS: module load Python/3.7.2-GCCcore-8.2.0
from pymongo import MongoClient
client = MongoClient("fat01", 27017)

query = client.gmgc_clusters.members.find({"nu": {"$gte": 10}}, {"_id": 0, "cl": 1})

import sys
for cluster in query:
    sys.stdout.write(f"{cluster['cl']}\n")