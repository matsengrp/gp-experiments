set -eux

TREES=Makona_1610_genomes_2016-06-23_unique_sequences.fasta.ufboot.rerooted.sorted.top1000
SEQS=Makona_1610_genomes_2016-06-23_unique_sequences.fasta

mkdir -p _ignore
test -f _ignore/$TREES || gunzip -c $TREES.gz > _ignore/$TREES
test -f _ignore/$SEQS || gunzip -c $SEQS.gz > _ignore/$SEQS

mkdir -p _output
gpex fit --config config.json _ignore/$TREES _ignore/$SEQS _output/gp-sbn-parameters.csv
