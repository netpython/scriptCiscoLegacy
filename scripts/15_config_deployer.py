#!/usr/bin/env python3
from pathlib import Path
from netmiko import ConnectHandler
from common import *
log=setup("config_deployer"); p=parser("Déploiement contrôlé"); p.add_argument("--config",required=True); p.add_argument("--dry-run",action="store_true"); p.add_argument("--save",action="store_true")
args=p.parse_args(); commands=[x.strip() for x in Path(args.config).read_text(encoding="utf-8").splitlines() if x.strip() and not x.lstrip().startswith("!")]
def job(d):
    name=d.get("name",d["host"])
    if args.dry_run: return {"device":name,"status":"DRY-RUN","commands":commands}
    params={k:v for k,v in d.items() if k!="name"}
    with ConnectHandler(**params) as c:
        if d.get("secret"): c.enable()
        output=c.send_config_set(commands)
        if args.save: output+="\n"+c.save_config()
    return {"device":name,"status":"APPLIED","output":output}
result=parallel(devices(args.inventory),job,args.workers); log.info("%s",write_json("deployment",result))

