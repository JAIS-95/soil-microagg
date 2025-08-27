from Bio import Entrez
import time
import requests
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

def get_genbank_assembly_id(taxid):
    Entrez.email = "m.jaiswal@northeastern.edu"  # Replace with your email
    
    try:
        # Search for assembly records with the given taxid
        handle = Entrez.esearch(db="assembly", term="txid{}[Organism:exp] AND latest[filter]".format(taxid), retmax=1)
        record = Entrez.read(handle)
        
        if record["IdList"]:
            # Get the first assembly ID (assuming it's the most relevant)
            assembly_id = record["IdList"][0]
            
            # Fetch the assembly summary
            summary = Entrez.esummary(db="assembly", id=assembly_id, report="full")
            summary_record = Entrez.read(summary)['DocumentSummarySet']['DocumentSummary'][0]
            
            # Extract the GenBank assembly accession
            genbank_accession = summary_record.get('AssemblyAccession', 'Not available')
            
            return genbank_accession
        else:
            return "No assembly found for taxid {}".format(taxid)
    
    except Exception as e:
        return "Error for taxid {}: {}".format(taxid, str(e))

def get_genome_size(assembly_id, txid):
    url = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/{}/dataset_report".format(assembly_id)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
                
        # Extract relevant information
        if data:
            assembly_info = data['reports'][0]
            #accession = assembly_info['assembly']['assembly_accession']
            organism_name = assembly_info['organism']['organism_name']
            genome_size = assembly_info['assembly_stats']['total_sequence_length']
            return "{}\t{}\t{}\t{}".format(txid,assembly_id,organism_name,genome_size)
        else:
            return "{}\t{}\tNA\tnot_found".format(txid,assembly_id)
    
    except requests.exceptions.RequestException as e:
        return "{}\tError: {}".format(assembly_id,str(e))

# Main script

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    outfile.write("txid\tGCF_Id\tSpecies\tGenome_size\n")
    for line in infile:
        txid = line.strip()
        assembly_id = get_genbank_assembly_id(txid)
        result = get_genome_size(assembly_id, txid)
        outfile.write(result + '\n')

        time.sleep(1)  # To avoid overloading NCBI's servers

print("Results have been written to {}".format(output_file))