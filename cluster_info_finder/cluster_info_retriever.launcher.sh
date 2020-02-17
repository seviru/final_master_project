#!/usr/bin/env bash

module load Python/3.7.2-GCCcore-8.2.0;

while IFS=$'\t' read -r -a line; do
#	echo "Full line is: $line"
#	echo "First column is: ${line[0]}"
#	echo "Second column is: ${line[1]}"
	cluster="${line[0]}";
	partition="${line[1]}";
	python cluster_info_retriever.py $cluster $partition
#	sbatch -t 00:05:00 ./processor.sh $cluster $partition;
done < "$1" 



## END
