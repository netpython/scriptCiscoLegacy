#!/usr/bin/env python3
from common import *
log=setup("arp_table"); p=parser("Table ARP"); args=p.parse_args()
def job(d): return flatten(d.get("name",d["host"]),run(d,"show ip arp",True))
rows=sum(parallel(devices(args.inventory),job,args.workers),[]); log.info("%s",write_csv("arp_table",rows))

