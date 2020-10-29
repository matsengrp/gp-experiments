set -e
set -u

mkdir -p _ignore

last_percent() (
  percent=${1?}; shift
  ret=0
  for file do
    lines=$(wc -l < "$file") &&
      tail -n "$((lines * percent / 100))" < "$file" || ret=$?
  done
  exit "$ret"
)

FINAL_TREES=_ignore/ds7.rerooted-topologies.post-burn.nwk

rm -f $FINAL_TREES
for i in 1 2;
do
    # rerooting on 7, which is Didelphis_virginiana
    last_percent 75 _ignore/ds7.run${i}.t | awk '$1~/tree/ {print $NF}' | nw_topology - | nw_reroot - 7 | nw_order - >> $FINAL_TREES
done

../newick_to_nexus_int_sort.py _ignore/ds7.rerooted-topologies.post-burn.nwk _ignore/ds7.rerooted-topologies.post-burn.nexus
