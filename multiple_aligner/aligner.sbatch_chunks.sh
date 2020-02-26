#!/usr/bin/env bash
## CPCantalapiedra 2020

clusterlist="$1";
chunk="$2";
max="$3";
script="$4";

idx="$SLURM_ARRAY_TASK_ID";
# Use the index to compute an interval of rows to process
# based on "chunk" size
# example:
# idx = 1; chunk = 100
# start = 1; end = 100; next = 101
start=$(( 1 + ((idx - 1) * chunk) ));
end=$(( start + chunk - 1 ));
if [ "$end" -gt "$max" ]; then
    end=$max;
fi;
next=$(( end + 1 ));

#printf "Slurm index: ${SLURM_ARRAY_TASK_ID}\n" 1>&2;
#printf "Processing $clusterlist from $start to $end...\n" 1>&2;

rows=$(sed -n "${start},${end}p;${next}q" "$clusterlist");

numrows=$(echo "$rows" | wc -l);
#printf "Total rows: ${numrows}\n" 1>&2;

PATH="$PATH":/home/svruibal/final_master_project/multiple_aligner

echo "$rows" | while read row; do
    eval "${script} ${row}";
#	printf "${row}\n" 1>&2
done;

#printf "Finished.\n" 1>&2;

## END
