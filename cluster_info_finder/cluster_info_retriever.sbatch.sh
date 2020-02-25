##
##

outdir="slurm_out"
mkdir "$outdir"
errdir="slurm_err"
mkdir "$errdir"

## TEST

chunksize=100; # number of clusters to process in each task                                                                                                                                                                                                           
records=$(wc -l ../data/part_cluster_list.txt | awk '{print $1}'); # total number of clusters to process                                                                                                                                                
jobs=$(( (records / chunksize) + 1 )); # number of array tasks                                                                                                                                                                                                        
echo "$records";
                                                                                                                                                                                                                                                            
echo "$jobs";
                                                                                                                                                                                                                                                              
sbatch -a 1-${jobs} --nice=2 \
       -t 1-12:00:00 \
       -o "$outdir"/%A_%a.out \
       -e "$errdir"/%A_%a.err \
       ./sbatch_chunks.sh \
       ../data/part_cluster_list.txt \
       ${chunksize} \
	${records} \
	cluster_info_retriever.launcher.sh


##RUN ALL


chunksize=30; # number of clusters to process in each task                                                                                                                                                                                                           
records=$(wc -l ../data/cluster_list.txt | awk '{print $1}'); # total number of clusters to process                                                                                                                                                
jobs=$(( (records / chunksize) + 1 )); # number of array tasks                                                                                                                                                                                                        
echo "$records";
                                                                                                                                                                                                                                                            
echo "$jobs";
                                                                                                                                                                                                                                                              
sbatch -a 1-${jobs} --nice=2 \
       -t 1-12:00:00 \
       -o "$outdir"/%A_%a.out \
       -e "$errdir"/%A_%a.err \
       ./sbatch_chunks.sh \
       ../data/cluster_list.txt \
       ${chunksize} \
	${records} \
	cluster_info_retriever.launcher.sh

## END
