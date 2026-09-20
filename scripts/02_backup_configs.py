#!/usr/bin/env python3
from common import *
log=setup("backup_configs"); p=parser("Sauvegarde des configurations"); args=p.parse_args(); devs=devices(args.inventory)
def job(d):
    name=d.get("name",d["host"]); folder=OUTPUT/f"backup_{stamp()}"; folder.mkdir(exist_ok=True)
    for kind in ("running-config","startup-config"):
        (folder/f"{name}_{kind}.cfg").write_text(run(d,f"show {kind}"),encoding="utf-8")
    return {"device":name,"status":"saved","folder":str(folder)}
result=parallel(devs,job,args.workers); log.info("%s",write_json("backup_summary",result))

