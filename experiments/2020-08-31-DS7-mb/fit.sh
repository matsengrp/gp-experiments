set -eux

mkdir -p _output

TREES=_ignore/ds7.rerooted-topologies.last9000.nonsingletons.nwk
SEQS=DS7.n.fasta

# Train via GP
trap "rm -f _output/mmap.dat" EXIT
gpex fit --config config.json $TREES $SEQS

# # Train via SBN-SA and put in sa-sbn-params.csv
# python train-sbn-sa.py
#
# python plot.py
