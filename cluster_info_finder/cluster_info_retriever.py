#!/usr/bin/env python3
"""Script that gets as input a specific gene cluster and It
extracts all the needed info from that cluster, such as
fasta sequences for all the members of that cluster and
a table with different information of the hits of those cluster
sequences to uniprot.
"""
import sys 
import os
from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT, CL_MIN_SP_EVALUE
from pathlib import Path

__all__ = [] # no API
__author__ = "seviru"


### START THE MONGO CLIENT ###
client = MongoClient(MONGO_HOST, MONGO_PORT)


### USING THE CLUSTER NAME ###
cluster_name = sys.argv[1]
partition_number = sys.argv[2]

sys.stderr.write(f"Running cluster {cluster_name} at partition {partition_number}\n")

unigenes_list = client.gmgc_clusters.members.find_one({"cl": cluster_name}, {"_id": 0, "clm": 1})["clm"]
best_hit_hash = set() # List to store the best hits already found, and if they have a sequence, in order not to repeat the best_hit sequence search
BASE_PATH = "../data/partitions"


### FILE HANDLING THE OUTPUT FILES ###
Path(f"{BASE_PATH}/{partition_number}/tables").mkdir(parents=True, exist_ok=True)   # Create the folders if they dont exist
Path(f"{BASE_PATH}/{partition_number}/fastas").mkdir(parents=True, exist_ok=True)
table_outfile_path = f"{BASE_PATH}/{partition_number}/tables/{cluster_name}.tsv"    # Set the file output path
fastas_outfile_path = f"{BASE_PATH}/{partition_number}/fastas/{cluster_name}.fas"

try:    # Remove the folders if they exist, to not mix already existing files
    os.remove(table_outfile_path)
    os.remove(fastas_outfile_path)
except OSError:
    try:
        os.remove(fastas_outfile_path)
    except OSError:
        pass
table_outfile = open(table_outfile_path, "w")
fastas_outfile = open(fastas_outfile_path, "w")


### MAIN ###
try:
    for unigene in unigenes_list:
        sequence = client.gmgc_unigenes.sequences.find_one({"u": unigene}, {"_id": 0, "sq": 1})["sq"]   # Retrieve aminoacid sequence
        suffix = client.gmgc_unigenes.suffixes.find_one({"u": unigene}, {"_id": 0, "sfx": 1})["sfx"] # Retrieve unigene suffix

        try:    # Try to retrieve exact swissprot hit
            best_hit = client.gmgc_unigenes.sprot_exact.find_one({"u": unigene}, {"_id": 0, "spe": 1})["spe"]
            hit_flag = "spe"
            hit_name = best_hit
            evalue = "-"
            score = "-"
            identity = "-"
            query_covery = "-"
            target_covery = "-"
        except TypeError:

            try:    # Try to retrieve best swissprot hit
                best_hit = client.gmgc_unigenes.sprot_best.find_one({"u": unigene}, {"_id": 0, "spb":1})["spb"]
                hit_flag = "spb"
                hit_name = best_hit["n"]
                evalue = best_hit["ev"]
                score = best_hit["sc"]
                identity = best_hit["pi"]
                query_covery = best_hit["qc"]
                target_covery = best_hit["tc"]
            except TypeError:

                try:    # Try to retrieve best trembl hit
                    best_hit = client.gmgc_unigenes.trembl_best.find_one({"u": unigene}, {"_id":0, "trb":1})["trb"]
                    hit_flag = "trb"
                    hit_name = best_hit["n"]
                    evalue = best_hit["ev"]
                    score = best_hit["sc"]
                    identity = best_hit["pi"]
                    query_covery = best_hit["qc"]
                    target_covery = best_hit["tc"]
                except TypeError:
                    best_hit = None
                    hit_flag = "-"
                    hit_name = "-"
                    evalue = "-"
                    score = "-"
                    identity = "-"
                    query_covery = "-"
                    target_covery = "-"

        ### NOT NEEDED ATM ###
        # try: # Try to retrieve nucleotide sequence #
        #     nt_seq = client.gmgc_unigenes.nt_seqs.find_one({"u": unigene}, {"_id": 0, "nt_sq": 1})["nt_sq"] #
        # except TypeError:  #
        #     nt_seq = None  #
        ######################

        if best_hit is not None:
            if hit_name in best_hit_hash: # If we have a best hit, check if we already have saved It's fasta
                fastas_outfile.write(f">{unigene}\n{sequence}\n")
            else: # If we don't, we add it to the list and look for Its info.
                if evalue == "-" or float(evalue) <= CL_MIN_SP_EVALUE:
                    try:
                        hit_seq = client.sprot.ft.find_one({"AC": hit_name}, {"_id": 0, "SQ": 1})["SQ"]
                        fastas_outfile.write(f">{unigene}\n{sequence}\n>{hit_name}\n{hit_seq}\n")
                        best_hit_hash.add(hit_name)
                    except TypeError:
                        hit_seq = None
                        fastas_outfile.write(f">{unigene}\n{sequence}\n")
                else:
                    fastas_outfile.write(f">{unigene}\n{sequence}\n")                    

        else:
            fastas_outfile.write(f">{unigene}\n{sequence}\n")
            
        table_outfile.write(f"{unigene}\t{suffix}\t{hit_flag}\t{hit_name}\t{evalue}\t{score}\t{identity}\t{query_covery}\t{target_covery}\n")

finally:
    table_outfile.close()
    fastas_outfile.close()
    client.close()


## END
