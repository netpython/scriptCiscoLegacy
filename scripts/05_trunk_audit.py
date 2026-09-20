#!/usr/bin/env python3
from common import *
log=setup("trunk_audit"); p=parser("Audit trunks"); args=p.parse_args()
def job(d): return flatten(d.get("name",d["host"]),run(d,"show interfaces trunk",True))
rows=sum(parallel(devices(args.inventory),job,args.workers),[]); log.info("%s",write_csv("trunks",rows))

