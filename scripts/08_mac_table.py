#!/usr/bin/env python3
from common import *
log=setup("mac_table"); p=parser("Table MAC"); args=p.parse_args()
def job(d): return flatten(d.get("name",d["host"]),run(d,"show mac address-table",True))
rows=sum(parallel(devices(args.inventory),job,args.workers),[]); log.info("%s",write_csv("mac_table",rows))

