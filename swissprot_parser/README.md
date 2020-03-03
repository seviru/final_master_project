# uniprot_releases

Simple scripts to download uniprot releases

CPCantalapiedra 2018

#### DOWNLOAD

```
git clone https://github.com/Cantalapiedra/uniprot_releases.git
```

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

PREV_RELEASES_LIST	prev_releases.list
RELEASES_DIR	releases
```

##### Check current uniprot release

```
./check_current.sh
```

The script will report the current release 
found in the Uniprot server, and whether 
the release version has already been downloaded 
previously or if it is new

##### Download current uniprot release

```
./download_current.sh
```

The script just checks which is the current
release in the Uniprot server, and downloads
it. It doesn't check whether the release
has already been downloaded or not.
The release will be downloaded (overwriting) to
releases/RELEASE_VERSION
