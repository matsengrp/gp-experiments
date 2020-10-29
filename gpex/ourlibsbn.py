"""our libsbn interface."""

import libsbn
import gpex.tree


def fit(newick_path, fasta_path, tol, max_iter, bl_only):
    inst = libsbn.gp_instance("_output/mmap.dat")
    inst.read_fasta_file(fasta_path)
    gpex.tree.read_tree_file(inst, newick_path)
    inst.make_engine()
    inst.print_status()
    inst.estimate_branch_lengths(tol, max_iter)
    if not bl_only:
        inst.estimate_sbn_parameters()
        inst.sbn_parameters_to_csv("_output/gp-sbn-parameters.csv")


def simpleaverage(tree_path, out_csv_path):
    inst = libsbn.rooted_instance("")
    inst.read_nexus_file(tree_path)
    inst.process_loaded_trees()
    inst.train_simple_average()
    inst.sbn_parameters_to_csv(out_csv_path)
