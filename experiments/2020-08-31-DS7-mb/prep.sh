mkdir -p _ignore
mb simplest.mb > _ignore/ds7.log

# rerooting on 7, which is Didelphis_virginiana
awk '$1~/tree/ {print $NF}' _ignore/ds7.t | nw_topology - | nw_reroot - 7 | nw_order - | tail -n 9000 > _ignore/ds7.rerooted-topologies.last9000.nwk
sort _ignore/ds7.rerooted-topologies.last9000.nwk | uniq -c | sort -nr | awk '$1 > 1 {print $2}' > _ignore/ds7.rerooted-topologies.last9000.nonsingletons.nwk
