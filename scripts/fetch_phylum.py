import sys
from ete3 import NCBITaxa

input_file = sys.argv[1]
output_file = sys.argv[2]

def get_phylum_names(taxids):
    ncbi = NCBITaxa()
    phylum_names = {}

    for taxid in taxids:
        lineage = ncbi.get_lineage(taxid)
        ranks = ncbi.get_rank(lineage)
        names = ncbi.get_taxid_translator(lineage)
        
        # Find the phylum in the lineage
        phylum_id = [tid for tid in lineage if ranks[tid] == 'phylum']
        
        if phylum_id:
            phylum_name = names[phylum_id[0]]
            phylum_names[taxid] = phylum_name
        else:
            phylum_names[taxid] = "Phylum not found"

    return phylum_names

# main script

with open(input_file, 'r') as infile:
    taxids=[int(line.strip()) for line in infile if line.strip()]

#get phylum_names
phylum_results = get_phylum_names(taxids)

#write result to output file
with open(output_file, 'w') as outfile:
    outfile.write("txid\tPhylum\n")
    for taxid, phylum in phylum_results.items():
        outfile.write("{}\t{}\n".format(taxid,phylum))

print("Results have been written to {}".format(output_file))