import argparse
import logging
import subprocess
from tqdm import tqdm
import pandas as pd
import networkx as nx
import numpy as np
import json
import collections

from ..core.go import GO
from ..core.cluster import Cluster

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum level of messages to capture
    format='%(asctime)s - %(levelname)s - %(message)s',  # Specify the format of the log messages
    handlers=[
        logging.StreamHandler()  # Log messages will be output to the console
    ]
)

def clean_GO_map(f):
    seqDb = pd.read_csv(f,sep=',')
    seqDb.columns = ['seq','manual_annot','pfam_list','GO_list']
    seqDb['GO_str'] = seqDb['GO_list']
    seqDb['GO_list'] = seqDb['GO_str'].str.split(';')
    def extract_GO_id_from_list(l):
        if isinstance(l,list):
            return [i.split('|')[0] for i in l]
        else:
            return None
    seqDb['GO_ids'] = seqDb['GO_list'].apply(extract_GO_id_from_list)
    seq2GO = seqDb[['seq','GO_ids']]
    seq2GO.columns = ['seq','GO_ids']
    return seq2GO

def read_network(DSDfile, interactionFile, edge_weight_thresh=0.5, net_name="Network", results_dir='./'):
    '''
    Read in the network and filter edges based on DSD confidence threshold
    '''

    '''
    if not DSDfile:
        logging.info(f'DSD file not provided. Generating DSD adjacency matrix...')        
        command = ['fastDSD', '-c', 'converge', '-t', 0.5, --outfile, f"{results_dir}/dsd_adjacency_matrix interactionFile"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logging.info(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
    '''

    logging.info(f'Reading DSD File: {DSDfile}...')
    dsd_df = pd.read_csv(DSDfile, sep='\t', index_col=0, header=0)
    protein_names = [str(i) for i in dsd_df.index]
    DSD = dsd_df.values

    fullG = nx.read_weighted_edgelist(interactionFile)
    logging.info('Selecting DSD connected component...')
    G = fullG.subgraph(protein_names)
    logging.info('Filtering edges with confidence threshold {}...'.format(edge_weight_thresh))
    wG = nx.Graph()
    for (u,v,d) in tqdm(G.edges.data()):
        if d['weight'] >= edge_weight_thresh:
            wG.add_edge(u,v,weight=d['weight'])
    del G
    G = wG 
    A = nx.to_numpy_array(G, nodelist=protein_names)
    degrees = [i[1] for i in list(G.degree())]

    #if output_stats:
    # print a table of network statistics
    label = ['Nodes','Edges','Degree (Med)','Degree (Avg)','Sparsity']
    value = [len(G.nodes), len(G.edges), np.median(degrees), np.mean(degrees), len(G.edges()) / len(G)**2]
    stats = pd.DataFrame([label,value]).T
    stats.columns = ['',net_name]
    stats = stats.set_index('')
    logging.info(stats)
    # save a histogram of protein degree 
    #display_degree_dist(G, degrees, net_name, results_dir)

    return G, DSD, protein_names

def display_degree_dist(G, degrees, net_name, results_dir):
    '''
    Helper function to read_network that displays the degree distribution of the initial network
    '''
    degreeDist = {}
    for i in degrees:
        n = degreeDist.setdefault(i,0)
        degreeDist[i] = n + 1

    plt.xlabel('Degree')
    plt.ylabel('Proportion of Nodes')  # we already handled the x-label with ax1
    plt.title('Node Degree Distribution')
    plt.scatter(degreeDist.keys(), [i/len(G) for i in degreeDist.values()])
    print('Saving Degree Distribution Plot to: ', results_dir + net_name + '.degree_dist.png')
    plt.savefig(results_dir + net_name + '_degree_dist.png')


def clean_GO_map(f):
    seqDb = pd.read_csv(f,sep=',')
    seqDb.columns = ['seq','manual_annot','pfam_list','GO_list']
    seqDb['GO_str'] = seqDb['GO_list']
    seqDb['GO_list'] = seqDb['GO_str'].str.split(';')
    def extract_GO_id_from_list(l):
        if isinstance(l,list):
            return [i.split('|')[0] for i in l]
        else:
            return None
    seqDb['GO_ids'] = seqDb['GO_list'].apply(extract_GO_id_from_list)
    seq2GO = seqDb[['seq','GO_ids']]
    seq2GO.columns = ['seq','GO_ids']
    return seq2GO


def plot_stuff(TODO):
    pass
    '''
    # plot the distribution of proteins added
    plt.hist(prot_counts.values(), bins=range(1, max(prot_counts.values())+1))
    plt.xlabel('Number of times protein was added')
    plt.ylabel('Number of proteins')
    
    # make y axis log scale
    plt.yscale('log')
    # add count on the top of the histogram bar
    
    plt.title(f'Distribution of proteins added ({net_name})')
    '''


def get_clusters_from_file(G, post_recipe_clusters_filepath):
    logging.debug(f"Reading clusters from {post_recipe_clusters_filepath}")
    clusters = Cluster.readClusterObjects(post_recipe_clusters_filepath)
    for i in clusters:
        i.set_graph(G)
    return clusters

    
def get_network_from_file(G, protein_names):
    fullNetwork = Cluster(protein_names) 
    fullNetwork.set_graph(G)
    return fullNetwork


def gen_maps(protein_go_map_filepaths):
    dataframes = []
    for file in protein_go_map_filepaths:
        clean_map = clean_GO_map(file)
        dataframes.append(clean_map)
    goMap = pd.concat(dataframes, ignore_index=True)
    return goMap


def get_go_objects(go_db_file):
    GO_OBJECTS = GO.read_GO_obo(go_db_file)
    return GO_OBJECTS


def write_pretty(TODO):
    '''
    summary_output_filename = f'{BASE_DIR}{net_name}_pretty_clusters_summary.txt'
    with (open(summary_output_filename, 'w+')) as f:
        for i in clusters:
            f.write(i.__repr__() + '\n')
        # f.write(json.dumps([i.to_dict() for i in clusters]))
    print(f"pretty summary printed to {summary_output_filename}")
    hash_to_proteins_file = f'{BASE_DIR}{net_name}_hash_to_proteins.json'
    with (open(hash_to_proteins_file, 'w+')) as f:
        for i in clusters:
            f.write(json.dumps({hash(i): i.proteins}) + '\n')
    print(f"cluster info printed to {hash_to_proteins_file}")
    '''
    pass

def create_dict(output_dir):
    import collections
    recipe_json = f"{output_dir}/recipe_clusters.json"
    
    # determine distribution of protein re-addition.
    recipe_prots = {}
    with open(recipe_json) as f:
        recipe_prots = json.load(f)
    
    # create a default dict where the key is a protein and the initial val is 0
    # then for each cluster, increment the count for each protein in the cluster
    prot_counts = collections.defaultdict(int)
    for k in recipe_prots["degree"]["0.75"].keys():
        for prot in recipe_prots["degree"]["0.75"][k]:
            prot_counts[prot] += 1


def filter_results(metric, percent_conec, readdition_threshold, clusters, qualifying_proteins_by_metric):
    # print(f"qualifying: {qualifying_proteins_by_metric.keys()}")
    # write output to clusters
    # for metric in qualifying_proteins_by_metric.keys():
    #     with open(metric + "_" + outfile, "w") as f:

    # IGNORE PROTEINS ADDED MORE THAN 15 TIMES
    prot_counts = collections.defaultdict(int)
    # TODO add error log for metric and percent_conec
    for k in qualifying_proteins_by_metric[metric][percent_conec].keys():
        for prot in qualifying_proteins_by_metric[metric][percent_conec][k]:
            prot_counts[prot] += 1

    addition_proteins = set([k for k in prot_counts.keys() if prot_counts[k] <= readdition_threshold])

    for (cluster, prots) in qualifying_proteins_by_metric[metric][percent_conec].items():
        if len(prots) > 0:
            qualifying_proteins_by_metric[metric][percent_conec][cluster] = [prot for prot in prots if prot in addition_proteins]
    return qualifying_proteins_by_metric


def printstuff():
    print(f"writing to {outfile_prefix}-clusters.json")
    with open(outfile, "w") as f:
        for i in range(0, len(initial_clusters)):
            if (len(initial_clusters[i]) == 0):
                continue

            f.write(initial_clusters[i])
            
            if str(i) in qualifying_proteins_by_metric[metric][percent_conec].keys():
                print(f"{len(qualifying_proteins_by_metric[metric][percent_conec][str(i)])} proteins added to cluster {i} for metric {metric} and percent_conec {percent_conec}")
                f.write(args.sep)
                f.write(",".join(qualifying_proteins_by_metric[metric][percent_conec][str(i)]))
            f.write("\n")


def pretty_print_clusters(clusters, outfile):
    # NOTE: this is added to be able to print the clusters to files for lenore
    with (open(outfile, 'w+')) as f:
        for i in clusters:
            f.write(i.__repr__() + '\n')
        # f.write(json.dumps([i.to_dict() for i in clusters]))
    logging.info(f"Pretty summary saved to {outfile}")

def print_reconnected_clusters(clusters, outfile):
    out_dict = {}
    for i in clusters:
        out_dict[hash(i)] = {}
        out_dict[hash(i)]["members"] = i.proteins
        out_dict[hash(i)]["GO_terms"] = i.GO_terms
    with (open(outfile, 'w+')) as f:
        json.dump(out_dict, f)
    '''
    with (open(outfile, 'w+')) as f:
        for i in clusters:
            f.write(json.dumps({hash(i): i.proteins}) + '\n')
    '''
    logging.info(f"Clusters saved to {outfile}")
            
def parse(cluster_filepath,
         network_filepath,
         dsd_file,
         protein_go_filepaths,
         go_db_file,
         cluster_outfile,
         qualifying_proteins_by_metric,
         pretty_summary_outfile = None,
         threshold=0.5,
         cthresh=0.75,
         metric="degree",
         readdition_threshold=15
        ):
    G, DSD, protein_names = read_network(dsd_file, network_filepath, threshold, "Network")
    clusters = get_clusters_from_file(G, cluster_filepath)
    fullNetwork = get_network_from_file(G, protein_names)
    goMap = gen_maps(protein_go_filepaths)
    qualifying_proteins_by_metric = filter_results(metric, cthresh, readdition_threshold, clusters, qualifying_proteins_by_metric)

    logging.info('Adding GO Annotations...')
    GO_OBJECTS = get_go_objects(go_db_file)
    for clust in tqdm(clusters):
        clust.add_GO_terms(goMap,GO_OBJECTS)
    clusters.sort(key=lambda x: len(x), reverse=True)
    fullNetwork.add_GO_terms(goMap,GO_OBJECTS)
    if pretty_summary_outfile:
        pretty_print_clusters(clusters, pretty_summary_outfile)
    print_reconnected_clusters(clusters, cluster_outfile)


def get_args(parser=None):
    """
    """
    if parser is None:
        parser = argparse.ArgumentParser()
    parser.add_argument(
        "-cfp", "--cluster-filepath", 
        required=True,
        help = "Cluster filepath", 
        type = str
    )
    parser.add_argument(
        "--recipe-results", 
        required=True,
        help = "ReCIPE results filepath generated from `reconnect` command", 
        type = str
    )
    parser.add_argument('--dsd-file', default=None, help='Path to the DSD file adjacency matrix', required = True, type = str)
    parser.add_argument(
        "-nfp", "--network-filepath", 
        help = "Network filepath", 
        required=True,
        type = str
    )
    parser.add_argument(
        '--protein-go-filepaths',
        type=str,
        nargs='+',
        required = True,
        help="Takes in a CSV file file formatted as follows: `<ID (required)>, <manual_annotation>, <name>, <GO_list>`. The <GO_list> column contains ';' separated GO annotations."
    )
    parser.add_argument(
        "--connectivity-threshold", "-cthresh",
        required=False,
        help = 'Connectivity threshold to add proteins until.',
        default = 0.75,
        type=float
    )
    parser.add_argument("-t", "--threshold", required=False, help = "Threshold for PPIs' confidence score", default=0.5, type=float)
    # parser.add_argument('--lr', help='The second parameter')
    # parser.add_argument('--max-proteins', help='Maximum number of proteins to reconnect')
    parser.add_argument(
        "--metric", "-wm",
        required=False,
        help = "Which metric to use to rank proteins to be added back. Default: degree. Options: degree, components_connected, score",
        choices=['degree', 'components_connected', 'score'],
        type = str,
        default = "degree"
    )
    # parser.add_argument('--output', help='File path to output reconnected components')
    parser.add_argument("--cluster_outfile", help = "Filepath to save final cluster JSON file.", type = str, required=False, default="./recipe-clusters.json")
    parser.add_argument("--pretty_summary_outfile", help = "Filepath to save pretty printed TXT summary of reconnexted clusters.", type = str, required=False, default=None)
    parser.add_argument(
        '--readdition-threshold',
        default=15,
        type=int,
        help='Filter out proteins added more times than cutoff'
    )
    parser.add_argument("--go-db-file", type=str, help="Path to the GO database file", required=False, default="go.obo")

    return parser


def main(args=None):
    if args is None:
        args = get_args().parse_args()

    qualifying_proteins_by_metric = {}
    with open(args.recipe_results, "rb") as f:
        qualifying_proteins_by_metric = json.load(f)
    
    parse(args.cluster_filepath, args.network_filepath, args.dsd_file, args.protein_go_filepaths, args.go_db_file, args.cluster_outfile, qualifying_proteins_by_metric, args.pretty_summary_outfile, args.threshold, str(args.connectivity_threshold), args.metric, args.readdition_threshold)

if __name__ == "__main__":
    parser = get_args()
    main(parser.parse_args())
