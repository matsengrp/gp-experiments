"""
Training an SBN via SA
"""

import libsbn

inst = libsbn.rooted_instance("charlie")
inst.read_newick_file("_ignore/ds7.rerooted-topologies.last9000.nonsingletons.nwk")
inst.process_loaded_trees()
inst.train_simple_average()
inst.sbn_parameters_to_csv("_output/sa-sbn-params.csv")
