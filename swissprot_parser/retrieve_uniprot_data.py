#!/usr/bin/env python3
## CPCantalapiedra 2019

import sys, gzip, json, pprint

UP_ID_FIELD = "ID"
UP_AC_FIELD = "AC"
UP_DE_FIELD = "DE"
UP_FT_FIELD = "FT"
UP_SQ_FIELD = "SQ"
UP_END_FIELD = "//"

JSON_EC_FIELD = "EC"

uniprot_filename = sys.argv[1]

sys.stderr.write("Input file "+uniprot_filename+"\n")

def f_parse_infile(in_filename):
    records_read = 0
    record = {}
    cur_ft_dict = None
    seq_found = False
    
    with gzip.open(uniprot_filename, 'rt') as uniprot_file:
        
        for uniprot_line in uniprot_file:

            #if records_read>=1: break
            #sys.stderr.write(uniprot_line)
            
            if uniprot_line.startswith(UP_ID_FIELD):
                uniprot_id = uniprot_line.strip().split()[1]
                record = {UP_ID_FIELD:uniprot_id}
                #sys.stderr.write(str(uniprot_id)+"\n")
                
            elif uniprot_line.startswith(UP_AC_FIELD):
                record[UP_AC_FIELD] = uniprot_line.strip().split()[1].replace(";", "")

            elif uniprot_line.startswith(UP_DE_FIELD) and "EC=" in uniprot_line:
                record[JSON_EC_FIELD] = uniprot_line.strip().split()[1].replace("EC=", "").replace(";", "")

            elif uniprot_line.startswith(UP_END_FIELD):
                records_read+=1
                seq_found = False
                sys.stderr.write("Records read "+str(records_read)+"\n")
                yield record
                
            elif uniprot_line.startswith(UP_FT_FIELD):
                #sys.stderr.write(uniprot_line)
                uniprot_data = uniprot_line[5:]

                if uniprot_data.startswith(" "):
                    ft_type = None
                    cur_ft_dict["ann"] = cur_ft_dict["ann"]+""+uniprot_data.strip()

                else:
                    print(uniprot_data)
                    uniprot_data = uniprot_data.strip().split()
                    ft_type = uniprot_data[0]

                    ft_dict = {"ft":ft_type, "s":uniprot_data[1],
                               "e":uniprot_data[2], "ann":" ".join(uniprot_data[3:])}

                    if UP_FT_FIELD in record:
                        record[UP_FT_FIELD].append(ft_dict)
                    else:
                        record[UP_FT_FIELD] = [ft_dict]

                    cur_ft_dict = ft_dict

            elif uniprot_line.startswith(UP_SQ_FIELD):
                seq_found = True
            else:
                if seq_found and uniprot_line.startswith(" "):
                    if UP_SQ_FIELD in record:
                        record[UP_SQ_FIELD] = "".join([record[UP_SQ_FIELD], uniprot_line.strip().replace(" ", "")])
                    else:
                        record[UP_SQ_FIELD] = uniprot_line.strip().replace(" ", "")
                else:
                    pass # other fields


up_records = f_parse_infile(uniprot_filename)

for up_record in up_records:
    #for rec in up_record:
    #    if rec == "FT":
    #        for ft in up_record[rec]:
    #            print "\t".join([ft["ft_type"], ft["start"], ft["end"], ft["annot"]])   
    print(json.dumps(up_record))

sys.stderr.write("Finished.\n")

## END
