###############################################################
### Script to find all clusters with more than 10 unigenes  ###
### and retrieve info from those unigenes.                  ###
###############################################################

# MANUALLY DO THIS: module load Python/3.7.2-GCCcore-8.2.0
from pymongo import MongoClient
client = MongoClient("fat01", 27017)

unigenes_list = []  # Initialize an empty list where we will store all the unigenes
unigenes_info = {}  # Initialize an empty hash where we will store all the unigenes info

query = client.gmgc_clusters.members.find({"nu": {"$gte": 10}}, {"_id": 0, "clm": 1}).limit(1)

for clusters in query:  # Parser to extract all values from dictionaries and store them in a single column array
    unigenes_list.extend(clusters["clm"])

for unigene in unigenes_list:   # Iterator to find information regarding each gene in our unigenes_list
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
    try: # Try to retrieve nucleotide sequence
        nt_seq = client.gmgc_unigenes.nt_seqs.find_one({"u": unigene}, {"_id": 0, "nt_sq": 1})["nt_sq"]
    except TypeError:
        nt_seq = None
    unigenes_info[unigene] = {"sequence": sequence, "best_hit": best_hit, "hit_type": hit_flag, "nt_seq": nt_seq} # Store all retrieved info in a hash
    # print (unigenes_info[unigene])
