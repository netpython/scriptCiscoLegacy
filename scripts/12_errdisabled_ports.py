#!/usr/bin/env python3
from common import *
log=setup("errdisabled"); p=parser("Ports err-disabled"); args=p.parse_args()
def job(d):
    raw=run(d,"show interfaces status | include err-disabled")
    return [{"device":d.get("name",d["host"]),"line":line} for line in raw.splitlines() if line.strip()]
rows=sum(parallel(devices(args.inventory),job,args.workers),[]); log.info("%s",write_csv("errdisabled",rows))

