"""Some basic testing and demo code for the libsbn module.

If you want to see the results of the print statements, use `pytest -s`.
"""

import libsbn

inst = libsbn.rooted_instance("charlie")
inst.read_newick_file("ds4.rerooted-topologies.last9000.nonsingletons.nwk")
inst.process_loaded_trees()
inst.train_simple_average()
with open("_output/sa-sbn-params.csv", "w") as out:
    for pcsp, value in inst.pretty_indexed_sbn_parameters():
        out.write(",".join([pcsp, str(value)]) + "\n")
