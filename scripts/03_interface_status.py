#!/usr/bin/env python3
from common import *
log=setup("interface_status"); p=parser("État des interfaces"); args=p.parse_args()
def job(d): return flatten(d.get("name",d["host"]),run(d,"show interfaces status",True))
rows=sum(parallel(devices(args.inventory),job,args.workers),[]); log.info("%s",write_csv("interface_status",rows))

