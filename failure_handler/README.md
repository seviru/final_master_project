
# In this folder we will store our scripts regarding the erasing of files which may have been a wrong output from certain scripts, such as alignment or tree building.

failure_terminator.py: It's a python script which finds the files which have not an "OK" corresponding one and deletes them.
		It deletes OK files if they haven't a corresponding file as well.
		USAGE: $python failure_terminator.py <CLUSTER_NAME> <PARTITION_NAME> <FILETYPE>
		<FILETYPE>: It can be "alignments" or "trees".
failure_terminator.launcher.sh: It's a script used to run our failure_terminator.py in a recursive way for a given clusters list.
		USAGE: $./failure_terminator.launcher.sh <CLUSTERS_LIST> <FILETYPE>
		<FILETYPE>: It can be "alignments" or "trees".
failure_checker.py: It's a python script which makes a report in a text file of the cluster family and if the alignment or tre files have correctly generated.
		USAGE: $python failure_checker.py <CLUSTER_NAME> <PARTITION_NAME> <FILETYPE>
		<FILETYPE>: It can be "alignments" or "trees".
failure_checker.launcher.sh: Its a script used to run our failure_checker.oy in a recursive way for a given clusters list.
		USAGE: $./failure_checker.launcher.sh <CLUSTERS_LIST> <FILETYPE>
		<FILETYPE>: It can be "alignments" or "trees".
