mkdir -p _ignore
mb simplest.mb > _ignore/ds4.log

# rerooting on 8, which is Chytridium_confervae
awk '$1~/tree/ {print $NF}' _ignore/ds4.t | nw_topology - | nw_reroot - 8 | nw_order - | tail -n 9000 > _ignore/ds4.rerooted-topologies.last9000.nwk
sort _ignore/ds4.rerooted-topologies.last9000.nwk | uniq -c | sort -nr | awk '$1 > 1 {print $2}' > _ignore/ds4.rerooted-topologies.last9000.nonsingletons.nwk
