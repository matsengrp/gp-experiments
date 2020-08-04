set -eux

mkdir -p _output

TREES=ds4.rerooted-topologies.last9000.nonsingletons.nwk
SEQS=DS4.n.fasta

# Train via GP
trap "rm -f _output/mmap.dat" EXIT
gpex fit --config config.json $TREES $SEQS
# TODO: output the results as a CSV

# Train via SBN-SA and put in sa-sbn-params.csv
python train-sbn-sa.py

# TODO: compare CSVs
