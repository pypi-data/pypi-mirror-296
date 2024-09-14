### Steps for running ReCIPE

##### Install ReCIPE

`pip install recipe-cluster`

##### Download Gene Ontology Data Base

[Download gene ontology](https://geneontology.org/docs/download-ontology/)

#### Generate DSD file

[fastDSD](https://github.com/samsledje/fastDSD) is recommended. It can be used simply by running command:

`fastDSD -c --converge -t 0.5 --outfile dscript_distances network-filepath.csv`

#### Generate Cluster File (if necessary)

ReCIPE accepts both CSV and JSON formats for cluster files.

- **CSV format**: Each line in the CSV represents a cluster of proteins, with each cluster containing a comma-separated list of protein identifiers.
  
- **JSON format**: Each key represents a unique cluster ID. The value associated with each key is an object containing a `members` array, which lists the protein identifiers for that cluster.
  

#### Run ReCIPE

##### Reconnect Clusters

This method analyses cluster, network and DSD files to determine the which proteins qualify to be introduced to clusters in order to create overlapping clusters.

```
usage: recipe-cluster reconnect [-h] -cfp CLUSTER_FILEPATH [-cfl CLUSTERS_LABELED] -nfp
                        NETWORK_FILEPATH --outfile-prefix OUTFILE_PREFIX
                        [--modify-clusters MODIFY_CLUSTERS] [--lb LB] [--ub UB] [--lr LR]
                        [--connectivity-threshold CONNECTIVITY_THRESHOLD] [--metric METRIC]
                        [--max_proteins MAX_PROTEINS]

options:
  -h, --help            show this help message and exit
  -cfp CLUSTER_FILEPATH, --cluster-filepath CLUSTER_FILEPATH
                        Cluster filepath
  -cfl CLUSTERS_LABELED, --clusters-labeled CLUSTERS_LABELED
                        If a CSV file of clusters is passed, clusters have labels. Default:
                        False
  -nfp NETWORK_FILEPATH, --network-filepath NETWORK_FILEPATH
                        Network filepath
  --outfile-prefix OUTFILE_PREFIX
                        Output file prefix
  --modify-clusters MODIFY_CLUSTERS
                        Format of the output file. default is false, meaning the dict
                        (which maps added proteins to clusters, and retains all param
                        options) is printed. if set to true, the modified clusters are
                        printed. Default: False
  --lb LB               Lower bound (inclusive) for cluster size. Default: 3
  --ub UB               Upper bound (exclusive) for cluster size. Default: 100
  --lr LR               Linear ratio (if not using sqrt). Default = None
  --connectivity-threshold CONNECTIVITY_THRESHOLD, -cthresh CONNECTIVITY_THRESHOLD
                        Connectivity threshold to add proteins until. Default = -1.0
                        (yields connectivity thresholds [0.1, 0.25, 0.5, 0.75, 1.0]) (if
                        only a single option is desired, 0.75 is recommended)
  --metric METRIC, -wm METRIC
                        Which metric(s) to use to rank proteins to be added back. Default:
                        all. Options: all, degree, components_connected, score
  --max_proteins MAX_PROTEINS
                        Max number of proteins to add to a cluster. Default = 20
```

##### Parse Results

The `parse` command parses through the results of reconnecting the clusters and generates a JSON file. Each key in the JSON file represents a unique cluster ID. The value associated with each key is an object containing a `members` array, which lists the protein identifiers for that cluster and a `GO_terms` dictionary with the keys being all the GO terms associated with the members of the cluster and the value being the count of the GO term.

```
usage: recipe-cluster parse [-h] -cfp CLUSTER_FILEPATH --recipe-results RECIPE_RESULTS --dsd-file
                    DSD_FILE -nfp NETWORK_FILEPATH --protein-go-filepaths
                    PROTEIN_GO_FILEPATHS [PROTEIN_GO_FILEPATHS ...]
                    [--connectivity-threshold CONNECTIVITY_THRESHOLD] [-t THRESHOLD]
                    [--metric {degree,components_connected,score}]
                    [--output-prefix OUTPUT_PREFIX]
                    [--readdition-threshold READDITION_THRESHOLD] [--go-db-file GO_DB_FILE]

options:
  -h, --help            show this help message and exit
  -cfp CLUSTER_FILEPATH, --cluster-filepath CLUSTER_FILEPATH
                        Cluster filepath
  --recipe-results RECIPE_RESULTS
                        ReCIPE results filepath generated from `reconnect` command
  --dsd-file DSD_FILE   Path to the DSD file adjacency matrix
  -nfp NETWORK_FILEPATH, --network-filepath NETWORK_FILEPATH
                        Network filepath
  --protein-go-filepaths PROTEIN_GO_FILEPATHS [PROTEIN_GO_FILEPATHS ...]
                        Takes in a CSV file file formatted as follows: `<ID (required)>,
                        <manual_annotation>, <name>, <GO_list>`. The <GO_list> column
                        contains ';' separated GO annotations.
  --connectivity-threshold CONNECTIVITY_THRESHOLD, -cthresh CONNECTIVITY_THRESHOLD
                        Connectivity threshold to add proteins until.
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold for PPIs' confidence score
  --metric {degree,components_connected,score}, -wm {degree,components_connected,score}
                        Which metric to use to rank proteins to be added back. Default:
                        degree. Options: degree, components_connected, score
  --output-prefix OUTPUT_PREFIX
                        Prefix with which to save results
  --readdition-threshold READDITION_THRESHOLD
                        Filter out proteins added more times than cutoff
  --go-db-file GO_DB_FILE
                        Path to the GO database file
```

##### (Optional) Single Command Reconnect and Parse

There is an option, the `cook` command, to run both `reconnect` and `parse` using the same command.

```
usage: recipe-cluster cook [-h] -cfp CLUSTER_FILEPATH [-cfl CLUSTERS_LABELED] -nfp NETWORK_FILEPATH
                   --dsd-file DSD_FILE --protein-go-filepaths PROTEIN_GO_FILEPATHS
                   [PROTEIN_GO_FILEPATHS ...] [--go-db-file GO_DB_FILE]
                   [--output-prefix OUTPUT_PREFIX] [-t THRESHOLD]
                   [--connectivity-threshold CONNECTIVITY_THRESHOLD] [--lr LR]
                   [--metric {degree,components_connected,score}] [--lb LB] [--ub UB]
                   [--max-proteins MAX_PROTEINS]
                   [--readdition-threshold READDITION_THRESHOLD]

options:
  -h, --help            show this help message and exit
  -cfp CLUSTER_FILEPATH, --cluster-filepath CLUSTER_FILEPATH
                        Cluster filepath
  -cfl CLUSTERS_LABELED, --clusters-labeled CLUSTERS_LABELED
                        If a CSV file of clusters is passed, clusters have labels. Default:
                        False
  -nfp NETWORK_FILEPATH, --network-filepath NETWORK_FILEPATH
                        Network filepath
  --dsd-file DSD_FILE   Path to the DSD file adjacency matrix
  --protein-go-filepaths PROTEIN_GO_FILEPATHS [PROTEIN_GO_FILEPATHS ...]
                        Takes in a CSV file file formatted as follows: `<ID (required)>,
                        <manual_annotation>, <name>, <GO_list>`. The <GO_list> column
                        contains ';' separated GO annotations.
  --go-db-file GO_DB_FILE
                        Path to the GO database file
  --output-prefix OUTPUT_PREFIX
                        Prefix with which to save results
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold for PPIs' confidence score
  --connectivity-threshold CONNECTIVITY_THRESHOLD, -cthresh CONNECTIVITY_THRESHOLD
                        Connectivity threshold to add proteins until.
  --lr LR               Linear ratio (if not using sqrt). Default = None
  --metric {degree,components_connected,score}, -wm {degree,components_connected,score}
                        Which metric to use to rank proteins to be added back. Default:
                        degree. Options: degree, components_connected, score
  --lb LB               Lower bound (inclusive) for cluster size. Default: 3
  --ub UB               Upper bound (exclusive) for cluster size. Default: 100
  --max-proteins MAX_PROTEINS
                        Max number of proteins to add to a cluster. Default = 20
  --readdition-threshold READDITION_THRESHOLD
                        Filter out proteins added more times than cutoff
```

In addition to command line access. The methods in this package can be accessed programmatically with the same arguments as follows:
```
import recipe-cluster as recipe

recipe.reconnect(...)
recipe.parse(...)
recipe.cook(...)
```