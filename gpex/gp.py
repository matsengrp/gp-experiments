"""libsbn interface."""

import libsbn


def fit(newick_path, fasta_path):
    inst = libsbn.gp_instance("_output/mmap.dat")
    inst.read_fasta_file(fasta_path)
    inst.read_newick_file(newick_path)
    inst.make_engine()
    inst.print_status()
    inst.estimate_branch_lengths(1e-2, 10)
    inst.estimate_sbn_parameters(1e-2, 10)
