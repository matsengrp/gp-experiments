sc --deduplicate-sequences ~/test-libsbn/iqtree/Makona_1610_genomes_2016-06-23.fasta.uniqueseq.phyx Makona_1610_genomes_2016-06-23_unique_sequences.fasta
iqtree -m JC -wbtl -redo -o EBOV___Gueckedou-C05___KJ660348___GIN___Gueckedou___2014-03-19 -s Makona_1610_genomes_2016-06-23_unique_sequences.fasta -bb 10000
nw_reroot Makona_1610_genomes_2016-06-23_unique_sequences.fasta.ufboot EBOV___Gueckedou-C05___KJ660348___GIN___Gueckedou___2014-03-19 > Makona_1610_genomes_2016-06-23_unique_sequences.fasta.ufboot.rerooted
nw_topology *rerooted | nw_order - | sort | uniq -c | awk '{print $2}' > Makona_1610_genomes_2016-06-23_unique_sequences.fasta.ufboot.rerooted.sorted
head -n 100 Makona_1610_genomes_2016-06-23_unique_sequences.fasta.ufboot.rerooted.sorted > Makona_1610_genomes_2016-06-23_unique_sequences.fasta.ufboot.rerooted.sorted.top100
head -n 1000 Makona_1610_genomes_2016-06-23_unique_sequences.fasta.ufboot.rerooted.sorted > Makona_1610_genomes_2016-06-23_unique_sequences.fasta.ufboot.rerooted.sorted.top1000
