mkdir -p _ignore
mb simplest.mb > _ignore/ds1.log

# rerooting on 15, which is Latimeria_chalumnae or Coelacanth
awk '$1~/tree/ {print $NF}' _ignore/ds1.t | nw_topology - | nw_reroot - 15 | nw_order - | tail -n 9000 > _ignore/ds1.rerooted-topologies.last9000.nwk
sort _ignore/ds1.rerooted-topologies.last9000.nwk | uniq -c | sort -nr | awk '$1 > 1 {print $2}' > _ignore/ds1.rerooted-topologies.last9000.nonsingletons.nwk
