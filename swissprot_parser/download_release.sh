#! /bin/bash
## CPCantalapiedra 2018

release="$1";

UNIPROT_FTP=$(grep "^UNIPROT_FTP" config | cut -d $'\t' -f 2);
UNIPROT_RELNOTES=$(grep "^UNIPROT_RELNOTES" config | cut -d $'\t' -f 2);
UNIPROT_CURRENT=$(grep "^UNIPROT_CURRENT" config | cut -d $'\t' -f 2);

echo "Downloading $UNIPROT_RELNOTES from $UNIPROT_FTP ...";

ncftpget -v "$UNIPROT_FTP" ./ "$UNIPROT_RELNOTES";

##

RELNOTES=$(basename "$UNIPROT_RELNOTES");

#release=$(cat "$RELNOTES" | head -1 | cut -d $' ' -f 3);

echo "Release to download: $release";

##

RELEASES_DIR=$(grep "^RELEASES_DIR" config | cut -d $'\t' -f 2);

if [ ! -d "$RELEASES_DIR"/"$release" ]; then
	mkdir -p "$RELEASES_DIR"/"$release";
	if [ $? -ne 0 ]; then
		echo "Couldn't create "$RELEASES_DIR" directory.";
		exit -1;
	fi;
fi;

echo "Preparing to download uniprot $release to $RELEASES_DIR";

ncftpget -R "$UNIPROT_FTP" "$RELEASES_DIR"/"$release" "$UNIPROT_CURRENT"/uniprot_sprot.dat.gz

if [ $? -eq 0 ]; then
	PREV_RELEASES_LIST=$(grep "^PREV_RELEASES_LIST" config | cut -d $'\t' -f 2);
	if [ -f "$PREV_RELEASES_LIST" ]; then
		if !(grep -q -w "^$release" "$PREV_RELEASES_LIST"); then
			echo "$release" >> "$PREV_RELEASES_LIST";
		fi;
	else
		echo "$release" >> "$PREV_RELEASES_LIST";
	fi;
else
	echo "Downloaded of $release failed!";
fi;

echo "Finished.";

## END
