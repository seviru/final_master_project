###############################################################
### Script that gets as input a specific gene cluster and It### 
### extracts all the needed info from that cluster          ###
###############################################################


### START THE MONGO CLIENT ###
# MANUALLY DO THIS: module load Python/3.7.2-GCCcore-8.2.0
from pymongo import MongoClient
client = MongoClient("fat01", 27017)


### USING THE CLUSTER NAME ###
import sys 
cluster_name = sys.argv[1]
unigenes_list = client.gmgc_clusters.members.find_one({"cl": cluster_name}, {"_id": 0, "clm": 1})["clm"]
best_hit_list = [] # List to store the best hits already found, in order not to repeat the best_hit sequence output


### FILE HANDLING THE OUTPUT FILES ###
from pathlib import Path
Path("./tables").mkdir(parents=True, exist_ok=True)
Path("./fastas").mkdir(parents=True, exist_ok=True)
table_outfile_path = "./tables/" + cluster_name + ".tsv"
fastas_outfile_path = "./fastas/" + cluster_name + ".fas"
import os
try:
    os.remove (table_outfile_path)
    os.remove (fastas_outfile_path)
except OSError:
    try:
        os.remove (fastas_outfile_path)
    except OSError:
        pass
table_outfile = open (table_outfile_path, "w")
fastas_outfile = open (fastas_outfile_path, "w")

### LOOP TO EXTRACT EACH UNIGENE INFORMATION AND SAVE IT ###
for unigene in unigenes_list:
    sequence = client.gmgc_unigenes.sequences.find_one({"u": unigene}, {"_id": 0, "sq": 1})["sq"]   # Retrieve aminoacid sequence

    try:    # Try to retrieve exact swissprot hit
        best_hit = client.gmgc_unigenes.sprot_exact.find_one({"u": unigene}, {"_id": 0, "spe": 1})["spe"]
        hit_flag = "swissprot_exact"
    except TypeError:

        try:    # Try to retrieve best swissprot hit
            best_hit = client.gmgc_unigenes.sprot_best.find_one({"u": unigene}, {"_id": 0, "spb":1})["spb"]["n"]
            hit_flag = "swissprot_best"
        except TypeError:

            try:    # Try to retrieve best trembl hit
                best_hit = client.gmgc_unigenes.trembl_best.find_one({"u": unigene}, {"_id":0, "trb":1})["trb"]["n"]
                hit_flag = "trembl_best"
            except TypeError:
                best_hit = None
                hit_flag = None

    ### NOT NEEDED ATM ###
    # try: # Try to retrieve nucleotide sequence #
    #     nt_seq = client.gmgc_unigenes.nt_seqs.find_one({"u": unigene}, {"_id": 0, "nt_sq": 1})["nt_sq"] #
    # except TypeError:  #
    #     nt_seq = None  #
    ######################

    if best_hit is not None: # Check if we have a best hit
        table_outfile.write(f"{unigene}\t{best_hit}\t{hit_flag}\n")

        if best_hit in best_hit_list: # If we have a best hit, check if we already have saved It's fasta
            fastas_outfile.write(f">{unigene}\n{sequence}\n")
        else: # If we don't, we add it to the list and look for Its info.
            best_hit_list.append(best_hit)
            try: # Try to retrieve the best hit sequence
                hit_seq = client.sprot.ft.find_one({"AC": best_hit}, {"_id": 0, "SQ": 1})["SQ"]
                fastas_outfile.write(f">{unigene}\n{sequence}\n>{best_hit} | {hit_flag}\n{hit_seq}\n")
            except TypeError:
                hit_seq = None
                fastas_outfile.write(f">{unigene}\n{sequence}\n")

table_outfile.close()
fastas_outfile.close()