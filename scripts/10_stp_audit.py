#!/usr/bin/env python3
from common import *
log=setup("stp_audit"); p=parser("Audit spanning-tree"); args=p.parse_args()
def job(d): return {"device":d.get("name",d["host"]),"spanning_tree":run(d,"show spanning-tree root",True)}
result=parallel(devices(args.inventory),job,args.workers); log.info("%s",write_json("stp_audit",result))

