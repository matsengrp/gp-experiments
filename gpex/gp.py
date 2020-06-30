"""libsbn interface."""

import libsbn


def fit(newick_path, fasta_path):
    inst = libsbn.rooted_instance("")
    inst.read_newick_file(newick_path)
    inst.read_fasta_file(fasta_path)
    inst.print_status()
