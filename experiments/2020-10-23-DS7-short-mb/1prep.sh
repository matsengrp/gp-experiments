set -e
set -u

mkdir -p _ignore

FINAL_PREFIX=_ignore/ds7.rerooted-topologies.post-burn

rm -f $FINAL_PREFIX.nwk $FINAL_PREFIX.nexus
for i in 1 2;
do
    # rerooting on 7, which is Didelphis_virginiana
    last-percent 75 _ignore/ds7.run${i}.t | awk '$1~/tree/ {print $NF}' | nw_topology - | nw_reroot - 7 | nw_order - >> $FINAL_PREFIX.nwk
done

gpex newick-to-nexus-int-sort $FINAL_PREFIX.nwk $FINAL_PREFIX.nexus
