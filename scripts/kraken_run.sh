#! /bin/bash

## Run kraken2 to generate report file for paired-end reads
ls ~/Desktop/vlad_hstrain/vlad_absolute_quant/EMS_QUO1013582/*_R1_001.fastq.gz > R1_files
ls ~/Desktop/vlad_hstrain/vlad_absolute_quant/EMS_QUO1013582/*_R2_001.fastq.gz > R2_files
paste -d' ' R1_files R2_files > in_files
rm R1_files R2_files

while read -r line; 
do
kraken2 --db /home/mohini/Downloads/kraken2_newDB/ --threads 34 --paired --gzip-compressed --output report_file/$(basename "$line" | 
cut -d'_' -f1,2)_res --report report_file/$(basename "$line" | cut -d'_' -f1,2).report $line

# generate bracken files from Kraken report
bracken -d /home/mohini/Downloads/bracken_database/ -i report_file/$(basename "$line" | cut -d'_' -f1,2).report -o report_file/$(basename "$line" | cut -d'_' -f1,2).bracken -t 10
done < in_files