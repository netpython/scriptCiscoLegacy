#!/usr/bin/env python3
from common import *
log=setup("lldp_neighbors"); p=parser("Voisins LLDP"); args=p.parse_args()
def job(d): return flatten(d.get("name",d["host"]),run(d,"show lldp neighbors detail",True))
rows=sum(parallel(devices(args.inventory),job,args.workers),[]); log.info("%s",write_csv("lldp_neighbors",rows))

