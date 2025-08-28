import os, sys 
import pandas as pd 
import networkx as nx 

bracken_folder = sys.argv[1]
out_file = sys.argv[2]

# Function to read Bracken file from the given input bracken folder
def read_bracken(file): 
    df = pd.read_csv(file, sep='\t') 
    return df[['name', 'new_est_reads']] 

# Read all Bracken files in the folder 
bracken_files = [f for f in os.listdir(bracken_folder) if f.endswith('.bracken')] 
samples = {f: read_bracken(os.path.join(bracken_folder, f)) for f in bracken_files} 

# Create a graph 
G = nx.Graph() 

# Add nodes and edges 
for sample, data in samples.items(): 
    for _, row in data.iterrows(): 
        species = row['name'] 
        abundance = row['new_est_reads'] 
        G.add_node(species, type='species') 
        G.add_node(sample, type='sample') 
        G.add_edge(sample, species, weight=abundance) 

# Write to GML file 
nx.write_gml(G, out_file)

print("GML file 'bracken_network.gml' has been created for network analysis.") 
