#!/usr/bin/env python3
from common import *
log=setup("inventory"); p=parser("Inventaire Cisco IOS")
args=p.parse_args(); devs=devices(args.inventory)
def job(d):
    facts=run(d,"show version",True); inv=run(d,"show inventory",True)
    return {"device":d.get("name",d["host"]),"host":d["host"],"version":facts,"inventory":inv}
result=parallel(devs,job,args.workers); path=write_json("inventory",result); log.info("Export: %s",path)

