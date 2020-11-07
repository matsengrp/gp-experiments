"""our libsbn interface."""

import libsbn
import pandas as pd
import gpex.tree


def fit(newick_path, fasta_path, out_csv_path, tol, max_iter):
    inst = libsbn.gp_instance("_output/mmap.dat")
    inst.read_fasta_file(fasta_path)
    gpex.tree.read_tree_file(inst, newick_path)
    inst.make_engine()
    inst.print_status()
    inst.estimate_branch_lengths(tol, max_iter)
    inst.estimate_sbn_parameters()
    inst.sbn_parameters_to_csv(out_csv_path)


def rooted_instance_of_trees(tree_path):
    inst = libsbn.rooted_instance("")
    inst.read_nexus_file(tree_path)
    inst.process_loaded_trees()
    return inst


def treeprobs(tree_path, sbn_parameter_csv_path):
    inst = rooted_instance_of_trees(tree_path)
    inst.read_sbn_parameters_from_csv(sbn_parameter_csv_path)
    return pd.DataFrame({"probability": inst.calculate_sbn_probabilities()})
