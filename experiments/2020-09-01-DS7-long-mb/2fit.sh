set -eux

mkdir -p _output

TREES=_ignore/ds7.rerooted-topologies.post-burn.nexus
SEQS=DS7.n.fasta

# Train via GP
trap "rm -f _output/mmap.dat" EXIT
gpex fit --config config.json $TREES $SEQS

# Train via SBN-SA and put in sa-sbn-params.csv
gpex simpleaverage $TREES _output/sa-sbn-params.csv
