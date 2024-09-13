# This code is PhyloFunc package to calculate PhyloFunc distance for human gut microbiome dataset
import pkgutil
import time
import pandas as pd
from Bio import Phylo
import io
# Name internal nodes of phylogenetic tree
def assign_names(tree):
    node_count = 0
    for clade in tree.find_clades(order='postorder'):
        if not clade.name:
            node_count += 1
            clade.name = f"Node{node_count}"
    return tree, node_count
# Recursively collect leaf nodes and their data
def collect_leaf_nodes(clade, composition_table):
    if clade.is_terminal() or clade.name == "None":
        return pd.DataFrame()

    leaf_data = composition_table[composition_table['Genome'].isin(
        [sub_clade.name for sub_clade in clade.get_terminals() if sub_clade.name != "None"]
    )].copy()

    if not leaf_data.empty:
        leaf_data.loc[:, 'Genome'] = clade.name

    return leaf_data

# Recursively collect information about all branches of the tree
def collect_branches(clade, all_branches):
    if clade.is_terminal():
        return
    branches = generate_branches(clade)
    # Ensure that each entry in branches has exactly 4 elements
    all_branches.extend(branches)
    for child_clade in clade.clades:
        collect_branches(child_clade, all_branches)

# Process a phylogenetic tree clade to obtain information about its branches, including the predecessor, successor, and branch length.
def generate_branches(clade):
    branches = []
    for child in clade.clades:
        if child.branch_length is not None:
            branches.append([
                clade.name if clade.name else clade.clades[0].name,
                child.name if child.name else child.clades[0].name,
                child.count_terminals(),
                child.branch_length
            ])
    return branches

# Perform a PhyloFunc distance for one pair of sample
def PhyloFunc_distance(tree_file=None, sample_file=None):

    start_time = time.time()

    # Load the tree and sample data
    if tree_file is None:
        tree_data = pkgutil.get_data(__name__, 'data/bac120_iqtree_v2.0.1.nwk')
        tree = Phylo.read(io.StringIO(tree_data.decode('utf-8')), "newick")
    else:
        tree = Phylo.read(tree_file, "newick")

    if sample_file is None:
        sample_data = pkgutil.get_data(__name__, 'data/Genome-COG-distance.csv')
        sample_data = pd.read_csv(io.StringIO(sample_data.decode('utf-8')), sep=',')
    else:
        sample_data = pd.read_csv(sample_file, sep=',')

    # Assign names to internal nodes
    tree_with_names, node_count = assign_names(tree)

    # Collect branches
    all_branches = []
    collect_branches(tree_with_names.root, all_branches)
    branch_df = pd.DataFrame(all_branches, columns=["Precedent", "Consequent", "Number_of_child_nodes", "Length"]).dropna()

    # Calculate taxon and function composition
    grouped_sum_tax = sample_data.groupby('Genome')[sample_data.columns[2:]].sum()
    total_sum_tax = grouped_sum_tax.sum()
    tax_composition = grouped_sum_tax.div(total_sum_tax, axis=1).reset_index()

    weighted_function_composition = sample_data.groupby(['Genome', 'COG accession'])[sample_data.columns[2:]].sum()
    total_sum_all_func = weighted_function_composition.sum()
    weighted_function_composition = weighted_function_composition.div(total_sum_all_func, axis=1).reset_index()

    # Extend weighted function composition and taxon composition for internal nodes
    clades = [clade for clade in tree_with_names.find_clades() if not clade.is_terminal()]

    extend_weighted_function_composition = pd.concat([
        collect_leaf_nodes(clade, weighted_function_composition).groupby('COG accession')[sample_data.columns[2:]].sum()
        .reset_index().assign(Genome=clade.name)
        for clade in clades
    ], ignore_index=True)

    weighted_function_composition_all = pd.concat([weighted_function_composition, extend_weighted_function_composition], ignore_index=True)

    # Calculate weighted function composition percentage
    weighted_function_composition_percentage = weighted_function_composition_all.groupby(['Genome', 'COG accession'])[sample_data.columns[2:]].sum()
    total_by_genome = weighted_function_composition_all.groupby('Genome')[sample_data.columns[2:]].sum()
    weighted_function_composition_percentage = weighted_function_composition_percentage.div(total_by_genome, level=0).reset_index()

    # Fill in the average function composition percentage for intensity values where each COG is NaN.
    weighted_function_composition_percentage = weighted_function_composition_percentage.apply(lambda x: x.fillna(1 / len(x)) if x.isna().all() else x, axis=1)

    # Extend taxon composition for internal nodes
    extend_taxon_composition = pd.concat([
        collect_leaf_nodes(clade, tax_composition).groupby('Genome')[sample_data.columns[2:]].sum()
        .reset_index().assign(Genome=clade.name)
        for clade in clades
    ], ignore_index=True)

    extend_taxon_composition_merge_all_nodes = pd.concat([tax_composition, extend_taxon_composition], ignore_index=True)

    # Extract specific columns for the pairwise calculation
    Sample1, Sample2 = 2, 3  # Extract the first two samples from the table corresponding to column indices 2 and 3. 
    Sample1_function = weighted_function_composition_percentage.iloc[:, [0, 1, Sample1]]
    Sample1_taxon = extend_taxon_composition_merge_all_nodes.iloc[:, [0, Sample1 - 1]]

    Sample2_function = weighted_function_composition_percentage.iloc[:, Sample2]
    Sample2_taxon = extend_taxon_composition_merge_all_nodes.iloc[:, Sample2 - 1]

    Sample_pair_function = pd.concat([Sample1_function, Sample2_function], axis=1)
    Sample_pair_taxon = pd.concat([Sample1_taxon, Sample2_taxon], axis=1)

    PhyloFunc = 0

    # Calculate branch lengths for fast lookup
    branch_length_map = branch_df.set_index('Consequent')['Length'].to_dict()

    # Loop through each unique Genome to compute distance
    for t in weighted_function_composition_percentage['Genome'].unique():
        weight_taxon = branch_length_map.get(t, 1)

        data_cog_tax = Sample_pair_function[Sample_pair_function["Genome"] == t]
        if data_cog_tax.empty:
            continue

        origin_data_norm = data_cog_tax.iloc[:, 2:].apply(lambda x: x / x.sum(), axis=0).fillna(0)

        # Compute the minimum and maximum sums for the distance calculation
        min_sum = origin_data_norm.min(axis=1).sum()
        max_sum = origin_data_norm.max(axis=1).sum()

        if max_sum == 0:
            Sample_pair = 0
        else:
            Sample_pair = 1 - min_sum / max_sum

        Sample1_abundance = Sample_pair_taxon[Sample_pair_taxon["Genome"] == t].iloc[0, 1]
        Sample2_abundance = Sample_pair_taxon[Sample_pair_taxon["Genome"] == t].iloc[0, 2]

        # Accumulate the weighted PhyloFunc distance
        PhyloFunc += Sample_pair * weight_taxon * Sample1_abundance * Sample2_abundance

    # Output the result
    s1 = sample_data.columns[Sample1]
    s2 = sample_data.columns[Sample2]

    print(f'The optimized PhyloFunc distance between "{s1}" and "{s2}" is {PhyloFunc}.')
    print(f"Finish, time consumed: {time.time() - start_time:.2f} seconds")

# Calculate PhyloFunc distance matrix for all samples
def PhyloFunc_matrix(tree_file=None, sample_file=None):

    start_time = time.time()

    # Load the tree
    if tree_file is None:
        tree_data = pkgutil.get_data(__name__, 'data/bac120_iqtree_v2.0.1.nwk')
        tree = Phylo.read(io.StringIO(tree_data.decode('utf-8')), "newick")
    else:
        tree = Phylo.read(tree_file, "newick")

    # Load the sample data
    if sample_file is None:
        sample_data = pkgutil.get_data(__name__, 'data/Genome-COG-matrix.csv')
        sample_data = pd.read_csv(io.StringIO(sample_data.decode('utf-8')), sep=',')
    else:
        sample_data = pd.read_csv(sample_file, sep=',')

    # Assign names to internal nodes
    tree_with_names, node_count = assign_names(tree)

    # Collect branches
    all_branches = []
    collect_branches(tree_with_names.root, all_branches)

    # Create branch DataFrame with correct data and column names
    branch_df = pd.DataFrame(all_branches,
                             columns=["Precedent", "Consequent", "Number_of_child_nodes", "Length"]).dropna()

    # Calculate taxon composition
    Genome = 'Genome'
    Intensity = sample_data.columns[2:]

    # Calculate Taxon composition
    grouped_sum_tax = sample_data.groupby(Genome)[Intensity].sum()
    total_sum_tax = grouped_sum_tax.sum()
    tax_composition = grouped_sum_tax.div(total_sum_tax, axis=1).reset_index()

    # Calculate Weighted function composition
    weighted_function_composition = sample_data.groupby(['Genome', 'COG accession'])[Intensity].sum()
    total_sum_all_func = weighted_function_composition.sum()
    weighted_function_composition = weighted_function_composition.div(total_sum_all_func, axis=1).reset_index()

    # Extend weighted function composition for internal nodes
    clades = [clade for clade in tree_with_names.find_clades() if not clade.is_terminal()]
    extend_weighted_function_composition = pd.concat([
        collect_leaf_nodes(clade, weighted_function_composition).groupby('COG accession')[Intensity].sum()
        .reset_index().assign(Genome=clade.name)
        for clade in clades
    ])

    weighted_function_composition_all = pd.concat([weighted_function_composition, extend_weighted_function_composition],
                                                  ignore_index=True)

    # Calculate weighted function composition percentage
    weighted_function_composition_percentage = weighted_function_composition_all.groupby(['Genome', 'COG accession'])[
        Intensity].sum()
    total_by_genome = weighted_function_composition_all.groupby('Genome')[Intensity].sum()
    weighted_function_composition_percentage = weighted_function_composition_percentage.div(total_by_genome,
                                                                                            level=0).reset_index()

    # Fill in NaNs
    weighted_function_composition_percentage = weighted_function_composition_percentage.apply(
        lambda x: x.fillna(1 / len(x)) if x.isna().all() else x, axis=1
    )

    # Extend taxon composition for internal nodes
    extend_taxon_composition = pd.concat([
        collect_leaf_nodes(clade, tax_composition).groupby('Genome')[Intensity].sum()
        .reset_index().assign(Genome=clade.name)
        for clade in clades
    ])

    extend_taxon_composition_merge_all_nodes = pd.concat([tax_composition, extend_taxon_composition], ignore_index=True)

    # Calculate PhyloFunc distances for each sample pair
    column_pairs = list(zip(Intensity, range(2, len(Intensity) + 2)))
    columns = [col for col, idx in column_pairs]
    Sample_pair_matrix_norm = pd.DataFrame(index=columns, columns=columns, dtype=float)
    Sample_pair_matrix_norm.fillna(0, inplace=True)

    for i, (Sample1_col, a_idx) in enumerate(column_pairs):
        Sample1_function = weighted_function_composition_percentage.iloc[:, [0, 1, a_idx]]
        Sample1_taxon = extend_taxon_composition_merge_all_nodes.iloc[:, [0, a_idx - 1]]

        for j, (Sample2_col, b_idx) in enumerate(column_pairs[i + 1:], start=i + 1):
            Sample2_function = weighted_function_composition_percentage.iloc[:, b_idx]
            Sample2_taxon = extend_taxon_composition_merge_all_nodes.iloc[:, b_idx - 1]

            Sample_pair_function = pd.concat([Sample1_function, Sample2_function], axis=1)
            Sample_pair_taxon = pd.concat([Sample1_taxon, Sample2_taxon], axis=1)
            PhyloFunc = 0

            for t in weighted_function_composition_percentage['Genome'].unique():
                if t == f'Node{node_count}':  # set the weight of root dynamically
                    weight_taxon = 1
                else:
                    weight_taxon = branch_df.loc[branch_df['Consequent'] == t, 'Length'].values[0]

                data_cog_tax = Sample_pair_function[Sample_pair_function["Genome"] == t]
                if data_cog_tax.empty:
                    continue

                # Normalization using the helper function
                origin_data_norm = data_cog_tax.iloc[:, 2:].apply(lambda x: x / x.sum(), axis=0).fillna(0)

                # Calculate minimum and maximum sums
                min_sum = origin_data_norm.apply(lambda x: min(x), axis=1).sum()
                max_sum = origin_data_norm.apply(lambda x: max(x), axis=1).sum()

                if max_sum == 0:
                    Sample_pair = 0
                else:
                    Sample_pair = 1 - min_sum / max_sum

                Sample1_abundance = Sample_pair_taxon[Sample_pair_taxon["Genome"] == t].iloc[0, 1]
                Sample2_abundance = Sample_pair_taxon[Sample_pair_taxon["Genome"] == t].iloc[0, 2]
                PhyloFunc += Sample_pair * weight_taxon * Sample1_abundance * Sample2_abundance

            Sample_pair_matrix_norm.iat[i, j] = PhyloFunc
            Sample_pair_matrix_norm.iat[j, i] = PhyloFunc

            print(f'The PhyloFunc distance between "{Sample1_col}" and "{Sample2_col}" is {PhyloFunc}.')

    print(f"Finish, time consumed: {time.time() - start_time:.2f} seconds")

    return Sample_pair_matrix_norm


