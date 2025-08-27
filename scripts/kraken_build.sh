#! /bin/bash

db_name="$1"

### Building kraken Database on local computer
# to install NCBI taxonomy
time kraken2-build --download-taxonomy --db $db_name --threads 30
# to download bacterial and archaeal library
time kraken2-build --download-library bacteria --db $db_name --threads 20
time kraken2-build --download-library archaea --db $db_name --threads 20
# to build the kraken database
time kraken2-build --build --db $db_name --threads 30
# to build the bracken database
time bracken_build -d $db_name -t 30