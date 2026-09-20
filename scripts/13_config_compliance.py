#!/usr/bin/env python3
import re
from common import *
log=setup("config_compliance"); p=parser("Conformité configuration"); args=p.parse_args()
RULES={"ssh_v2":r"(?m)^ip ssh version 2$","no_http":r"(?m)^no ip http server$","timestamps":r"(?m)^service timestamps log datetime"}
def job(d):
    cfg=run(d,"show running-config"); row={"device":d.get("name",d["host"])}
    row.update({name:"PASS" if re.search(rx,cfg) else "FAIL" for name,rx in RULES.items()}); return row
rows=parallel(devices(args.inventory),job,args.workers); log.info("%s",write_csv("compliance",rows))

