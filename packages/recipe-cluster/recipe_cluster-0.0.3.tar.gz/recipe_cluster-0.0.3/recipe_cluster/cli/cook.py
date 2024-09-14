import argparse
from .parse import parse
from .reconnect import reconnect

def cook(cluster_filepath,
         network_filepath,
         dsd_file,
         protein_go_filepaths,
         go_db_file,
         cluster_outfile,
         pretty_summary_outfile=None,
         hub_protein_outfile=None,
         clusters_labeled=False,
         threshold=0.5,
         cthresh=0.75,
         lr=None,
         metric="degree",
         lb=3,
         ub=100,
         max_proteins=20,
         readdition_threshold=15
        ):
    qualifying_proteins_by_metric = reconnect(cluster_filepath, network_filepath, hub_protein_outfile, lb, ub, lr, cthresh, metric, max_proteins, clusters_labeled)
    parse(cluster_filepath, network_filepath, dsd_file, protein_go_filepaths, go_db_file, cluster_outfile, qualifying_proteins_by_metric, pretty_summary_outfile, threshold, cthresh, metric, readdition_threshold)

    
def main(args=None):
    if args is None:
        args = get_args().parse_args()
    
    cook(args.cluster_filepath, args.network_filepath, args.dsd_file, args.protein_go_filepaths, args.go_db_file, args.cluster_outfile, args.pretty_summary_outfile, args.hub_protein_outfile, args.clusters_labeled, args.threshold, args.connectivity_threshold, args.lr, args.metric, args.lb, args.ub, args.max_proteins, args.readdition_threshold)

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
    parser.add_argument (
        "-cfl", "--clusters-labeled", 
        required=False,
        help = "If a CSV file of clusters is passed, clusters have labels. Default: False",
        type = bool,
        default = False
    )
    parser.add_argument(
        "-nfp", "--network-filepath", 
        help = "Network filepath", 
        required=True,
        type = str
    )
    parser.add_argument('--dsd-file', default=None, help='Path to the DSD file adjacency matrix', required = True, type = str)
    parser.add_argument(
        '--protein-go-filepaths',
        type=str,
        nargs='+',
        required = True,
        help="Takes in a CSV file file formatted as follows: `<ID (required)>, <manual_annotation>, <name>, <GO_list>`. The <GO_list> column contains ';' separated GO annotations."
    )
    parser.add_argument("--go-db-file", type=str, help="Path to the GO database file", required=False, default="go.obo")
    parser.add_argument("--hub-protein-outfile", help = "File path for JSON cluster results", type = str, required=False, default="./recipe-clusters.json")
    parser.add_argument("--cluster_outfile", help = "Filepath to save final cluster JSON file.", type = str, required=False, default="./recipe-clusters.json")
    parser.add_argument("--pretty_summary_outfile", help = "Filepath to save pretty printed TXT summary of reconnexted clusters.", type = str, required=False, default=None)
    parser.add_argument("-t", "--threshold", required=False, help = "Threshold for PPIs' confidence score", default=0.5, type=float)
    parser.add_argument(
        "--connectivity-threshold", "-cthresh",
        required=False,
        help = 'Connectivity threshold to add proteins until.',
        default = 0.75,
        type=float
    )
    parser.add_argument(
        "--lr", 
        required=False,
        help = "Linear ratio (if not using sqrt). Default = None", 
        type = float,
        default = None,  
    )
    parser.add_argument(
        "--metric", "-wm",
        required=False,
        help = "Which metric to use to rank proteins to be added back. Default: degree. Options: degree, components_connected, score",
        choices=['degree', 'components_connected', 'score'],
        type = str,
        default = "degree"
    )
    parser.add_argument( 
        "--lb", 
        required=False,
        help = "Lower bound (inclusive) for cluster size. Default: 3", 
        type = int,
        default = 3,
    )
    parser.add_argument(
        "--ub", 
        required=False,
        help = "Upper bound (exclusive) for cluster size. Default: 100", 
        type = int,
        default=100,
    )
    parser.add_argument(
        "--max-proteins", 
        required=False,
        help = "Max number of proteins to add to a cluster. Default = 20", 
        type=int,
        default = 20
    )
    parser.add_argument(
        '--readdition-threshold',
        default=15,
        type=int,
        help='Filter out proteins added more times than cutoff'
    )    
    return parser

if __name__ == "__main__":
    parser = get_args()
    main(parser.parse_args())

