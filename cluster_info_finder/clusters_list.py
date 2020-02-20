#!/usr/bin/env python3
##
## CPCantalapiedra 2020
## SVruibal 2020

# Script to retrieve all clusters based on 
# the user-specified minimum size.
# usage: clusters_list.py MIN_CL_SIZE > clusters.list

import sys
from pymongo import MongoClient

min_cl_size = int(sys.argv[1])

MONGO_SERVER = "fat01"
MONGO_PORT = 27017

query = {"nu": {"$gte": min_cl_size}}
fields = {"_id": 0, "cl": 1}

######
# MAIN

client = MongoClient(MONGO_SERVER, MONGO_PORT)

sys.stderr.write(f"Retrieving clusters of min size {min_cl_size}\n")

query = client.gmgc_clusters.members.find(query, fields, no_cursor_timeout=True)

num_clusters = 0
for cluster in query:

    num_clusters += 1

    if num_clusters % 10000 == 0:
        sys.stderr.write(f"Clusters processed: {num_clusters}\n")

    cl_id = cluster["cl"]

    sys.stdout.write(f"{cl_id}\n")

sys.stderr.write(f"Num clusters found: {num_clusters}\n")
sys.stderr.write("Finished.\n")

## END
