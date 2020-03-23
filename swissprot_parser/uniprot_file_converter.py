###############################################################
### Script that transforms our parsed swissprot file in a   ###
### way which we can use It easily to build up the next     ###
### analyses.                                               ###
###############################################################

### PARSING THE STDIN OF retrieve_uniprot_data.py ###
import json, sys

for line in sys.stdin:
    uniprot_old_line = json.loads(line)
    uniprot_new_line = {}
    uniprot_new_line[uniprot_old_line["AC"]] = uniprot_old_line
    del (uniprot_new_line[uniprot_old_line["AC"]]["AC"])
    sys.stdout.write(f"{uniprot_new_line}\n")
