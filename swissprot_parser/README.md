# uniprot_releases

Simple scripts to download uniprot releases

CPCantalapiedra 2018
CPCantalapiedra 2020
SVRuibal 2020

##### Dependencies

This scripts use ncftpget to connect to the Uniprot FTP server.

```
sudo apt-get install ncftp
```

#### HOWTO


##### Config file

Prior to use for the first time 
(or if some Uniprot values change) 
check and configure the values within 
a plain text file called config. Example:

```
cat config

UNIPROT_FTP	ftp.uniprot.org
UNIPROT_RELNOTES	pub/databases/uniprot/relnotes.txt
UNIPROT_CURRENT	pub/databases/uniprot/knowledgebase
UNIPROT_PREVREL pub/databases/uniprot/previous_releases

PREV_RELEASES_LIST	prev_releases.list
RELEASES_DIR	releases
```

##### Check current uniprot release

```
check_current.sh
```

The script will report the current release 
found in the Uniprot server, and whether 
the release version has already been downloaded 
previously or if it is new

##### Download current uniprot release

```
download_current.sh
```

The script just checks which is the current
release in the Uniprot server, and downloads
its 'uniprot_sprot.data.gz'. 
It doesn't check whether the release
has already been downloaded or not.
The release will be downloaded (overwriting) to
'releases/RELEASE'.
RELEASE is usually YEAR_MONTH (e.g. 2018_09).

##### Download a specific uniprot release

```
download_release.sh RELEASE
```
The script downloads the 'uniprot_sprot-only.tar.gz' 
from the specified RELEASE.
The file will be downloaded to 'releases/RELEASE'
RELEASE is usually YEAR_MONTH (e.g. 2018_09).
The 'uniprot_sprot.dat.gz' file can be extracted from 
the downloaded file. For example:
```
tar -zxf releases/2018_09/uniprot_sprot-only2018_09.tar.gz releases/2018_09/uniprot_sprot.dat.gz
```

##### Parse SwissProt annotation data to a JSON file

```
retrieve_uniprot_data.py uniprot_sprot.dat.gz > JSON_FILE
```
This scripts parses the SwissProt data file and retrieves the "FT"
annotations, as well as the sequence "SQ" and EC number "EC".
Example:
```
retrieve_uniprot_data.py releases/2018_09/uniprot_sprot.dat.gz > sprot.2018_09.json

head -1 sprot.2018_09.json 

{"ID": "001R_FRG3G", "AC": "Q6GZX4", "FT": [{"ft": "CHAIN", "s": "1", "e": "256", "ann": "/note=\"Putative transcription factor 001R\"/id=\"PRO_0000410512\""}, {"ft": "COMPBIAS", "s": "14", "e": "17", "ann": "/note=\"Poly-Arg\""}], "SQ": "MAFSAEDVLKEYDRRRRMEALLLSLYYPNDRKLLDYKEWSPPRVQVECPKAPVEWNNPPSEKGLIVGHFSGIKYKGEKAQASEVDVNKMCCWVSKFKDAMRRYQGIQTCKIPGKVLSDLDAKIKAYNLTVEGVEGFVRYSRVTKQHVAAFLKELRHSKQYENVNLIHYILTDKRVDIQHLEKDLVKDFKALVESAHRMRQGHMINVKYILYQLLKKHGHGPDGPDILTVKTGSKGVLYDDSFRKIYTDLGWKFTPL"}
```

##### Parse SwissProt annotation data to a JSON file with different format
```
retrieve_uniprot_data.py uniprot_sprot.dat.gz | uniprot_file_converter > JSON_FILE
```

uniprot_file_converter used as a pipeline makes all our entries for the file have
the structure of {ACCESSION_NUMBER : {ALL_THE_DATA_FOR_THAT_ACCESSION_NUMBER}}

Example:
```
retrieve_uniprot_data.py releases/2018_09/uniprot_sprot.dat.gz | uniprot_file_connverter > sprot.2018_09.json

head -1 sprot.2018_09.json 

{'Q6GZX4': {'ID': '001R_FRG3G', 'FT': [{'ft': 'CHAIN', 's': '1', 'e': '1', 'ann': 'Putative transcription factor 001R./FTId=PRO_0000410512.'}, {'ft': 'COMPBIAS', 's': '14', 'e': '14', 'ann': 'Poly-Arg.'}], 'SQ': 'MAFSAEDVLKEYDRRRRMEALLLSLYYPNDRKLLDYKEWSPPRVQVECPKAPVEWNNPPSEKGLIVGHFSGIKYKGEKAQASEVDVNKMCCWVSKFKDAMRRYQGIQTCKIPGKVLSDLDAKIKAYNLTVEGVEGFVRYSRVTKQHVAAFLKELRHSKQYENVNLIHYILTDKRVDIQHLEKDLVKDFKALVESAHRMRQGHMINVKYILYQLLKKHGHGPDGPDILTVKTGSKGVLYDDSFRKIYTDLGWKFTPL'}}
```