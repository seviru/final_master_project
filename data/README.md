
# In this folder we have all the data stored from executing the scripts on our different folders
### DISCLAIMER: If you don't see anything in this folder is due to me not uploading the data files on purpose. If you want to check on them, feel free to contact me
_____________________________________________________________________________________________________________________________
#### &#60;OUTFILE>.txt (a.k.a. cluster_list.txt):
>We have a .txt file containing the clusters list which meet the requirements of "../cluster_info_finder/cluster_finder.py" script and the partition they will be saved in the next step.<br />`CREATED BY: cluster_finder.launcher.sh`

#### ./partitions/ :
>Folder where we will store all the output data. We decided to make partitions in order not to have a vast ammount of files (10.000+) on the same folder.<br />`CREATED BY: cluster_info_retriever.launcher.sh`

#### ./partitions/<PARTITION_NUMBER>/fastas/:
>Folder where we will store the FASTA (.fas) files of all the genes on each cluster from <OUTFILE>.txt . Besides, the fasta files for each cluster will have the fasta of the hits for the proteins of the cluster, if available.<br />`CREATED BY: cluster_info_retriever.launcher.sh`

#### ./partitions/<PARTITION_NUMBER>/tables/:
>Folder where we will store the TABLE (.tsv) files of all the genes on each cluster from <OUTFILE>.txt . Each <table&#62; file has 4 columns: Unigene_name, Best_protein_hit_name, best_protein_hit_type (swissprot exact, swissprot best or trembl best in that order of preference), and if best_hit_sequence_available.<br />`CREATED BY: cluster_info_retriever.launcher.sh`

#### ./partitions/<PARTITION_NUMBER>/alignments/:
>Folder where we will store the ALIGNMENT (.alg) files of all the genes on each cluster from <OUTFILE>.txt.<br />`CREATED BY: aligner.launcher.sh`

#### ./partitions/<PARTITION_NUMBER>/trees/:
>Folder where we will store the TREES (.tree) files for each cluster from <OUTFILE>.txt.<br />`CREATED BT: tree_builder.launcher.sh`

#### &#60;UNIPROT_RELEASE>.tar.gz:
>Compressed folder with all the specific information of uniprot for the given release.<br />`CREATED BY: download_current.sh OR download_release.sh`

#### &#60;UNIPROT_RELEASE>.dat.gz:
>File with the information regarding the swissprot information of the given release.<br />`CREATED BY: Unpacking <UNIPROT_RELEASE>.tar.gz`

#### &#60;UNIPROT_RELEASE>.json:
>File with the information regarding the swissprot information of the given release in a .json format.<br />`CREATED BY: retrieve_uniprot_data.py`
