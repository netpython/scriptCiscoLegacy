#!/usr/bin/env python3
from common import *
log=setup("vlan_audit"); p=parser("Audit VLAN"); args=p.parse_args()
def job(d): return flatten(d.get("name",d["host"]),run(d,"show vlan brief",True))
rows=sum(parallel(devices(args.inventory),job,args.workers),[]); log.info("%s",write_csv("vlans",rows))

