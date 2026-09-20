#!/usr/bin/env python3
from common import *
log=setup("cdp_neighbors"); p=parser("Voisins CDP"); args=p.parse_args()
def job(d): return flatten(d.get("name",d["host"]),run(d,"show cdp neighbors detail",True))
rows=sum(parallel(devices(args.inventory),job,args.workers),[]); log.info("%s",write_csv("cdp_neighbors",rows))

