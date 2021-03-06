set -eux

mkdir -p _output

TREES=run.fasta.ufboot.rerooted
SEQS=run.fasta

# Train via GP
trap "rm -f _output/mmap.dat" EXIT
gpex fit --config config.json $TREES $SEQS

# Train via SBN-SA and put in sa-sbn-params.csv
python train-sbn-sa.py $TREES

python plot.py
