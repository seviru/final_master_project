##

__author__ = "CPCantalapiedra 2020"

"""Default settings

This file should be configured and renamed to "settings.py".
MONGO_HOST and MONGO_PORT are required to access the MongoDB.
CL_MIN_SIZE could be any positive integer (or 0), which is
the minimum size of the clusters to retrieve.
"""

MONGO_HOST = "localhost" # Set here the IP or host name to MongoDB
MONGO_PORT = 27017 # Set here the port to MongoDB
CL_MIN_SIZE = 3 # Set here the minimum size (number of members) of the clusters to retrieve
CL_PARTITION_SIZE = 10000 # Number of clusters to be included in the same partition
CL_MIN_SP_EVALUE = 1e-10 # at least one swissprot hit must reach 1e-10 evalue

## END
