#!/usr/bin/env bash

module load Python/3.7.2-GCCcore-8.2.0

filetype="$2";
while IFS= read -r current; do
	cluster=$(echo "$current" | cut -f 1);
	partition=$(echo "$current" | cut -f 2);
	python failure_checker.py $cluster $partition $filetype
#	echo "$current ___ $cluster ___ $partition ___ $filetype"
done < "$1"

## END
