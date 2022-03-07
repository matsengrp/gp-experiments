"""bito interface."""

import bito


def fit(newick_path, fasta_path, tol, max_iter, bl_only):
    inst = bito.gp_instance("_output/mmap.dat")
    inst.read_fasta_file(fasta_path)
    inst.read_newick_file(newick_path)
    inst.make_engine()
    inst.print_status()
    inst.estimate_branch_lengths(tol, max_iter)
    if not bl_only:
        inst.estimate_sbn_parameters()
        inst.sbn_parameters_to_csv("_output/gp-sbn-parameters.csv")
