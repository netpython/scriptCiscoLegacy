#!/usr/bin/env python3
from common import *
log=setup("port_security"); p=parser("Audit port-security"); args=p.parse_args()
def job(d): return flatten(d.get("name",d["host"]),run(d,"show port-security",True))
rows=sum(parallel(devices(args.inventory),job,args.workers),[]); log.info("%s",write_csv("port_security",rows))

