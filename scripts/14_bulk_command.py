#!/usr/bin/env python3
from common import *
log=setup("bulk_command"); p=parser("Commande show en masse"); p.add_argument("--command",required=True)
args=p.parse_args()
if not args.command.strip().lower().startswith(("show ","ping ","traceroute ")): raise SystemExit("Seules les commandes de diagnostic sont autorisées.")
def job(d): return {"device":d.get("name",d["host"]),"command":args.command,"output":run(d,args.command)}
result=parallel(devices(args.inventory),job,args.workers); log.info("%s",write_json("bulk_command",result))

