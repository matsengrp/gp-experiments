"""libsbn interface."""

import libsbn


def fit(newick_path, fasta_path, tol, max_iter):
    inst = libsbn.gp_instance("_output/mmap.dat")
    inst.read_fasta_file(fasta_path)
    inst.read_newick_file(newick_path)
    inst.make_engine()
    inst.print_status()
    inst.estimate_branch_lengths(tol, max_iter)
    inst.estimate_sbn_parameters(tol, max_iter)
