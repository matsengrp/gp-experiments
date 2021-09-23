import libsbn

def simple_average(newick_path, fasta_path):
    inst = libsbn.rooted_instance("_output/mmap.dat")
    inst.read_fasta_file(fasta_path)
    inst.read_newick_file(newick_path)
    inst.process_loaded_trees()
    inst.print_status()
    inst.train_simple_average()
    inst.sbn_parameters_to_csv("_output/sbn-parameters.csv")
    return inst
