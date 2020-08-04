set -eux

mkdir -p _output

TREES=ds4.rerooted-topologies.last9000.nonsingletons.nwk
SEQS=DS4.n.fasta

trap "rm -f _output/mmap.dat" EXIT
gpex fit --config config.json $TREES $SEQS
