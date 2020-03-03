#! /bin/bash
## CPCantalapiedra 2018

UNIPROT_FTP=$(grep "^UNIPROT_FTP" config | cut -d $'\t' -f 2);
UNIPROT_RELNOTES=$(grep "^UNIPROT_RELNOTES" config | cut -d $'\t' -f 2);

##

echo "Downloading $UNIPROT_RELNOTES from $UNIPROT_FTP ...";

ncftpget -v "$UNIPROT_FTP" ./ "$UNIPROT_RELNOTES";

##

RELNOTES=$(basename "$UNIPROT_RELNOTES");

release=$(cat "$RELNOTES" | head -1 | cut -d $' ' -f 3);

echo "Current release: $release";

PREV_RELEASES_LIST=$(grep "^PREV_RELEASES_LIST" config | cut -d $'\t' -f 2);

if [ -f "$PREV_RELEASES_LIST" ]; then
        if grep -q -w "^$release" "$PREV_RELEASES_LIST"; then
                echo "Release $release already exists.";
        else
                echo "Release $release is new. (1)";
        fi;
else
	echo "Release $release is new. (2)";
fi;

## END
