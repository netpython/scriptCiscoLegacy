#!/usr/bin/env python3
"""Construit la topologie CDP/LLDP et signale les équipements sans redondance."""
from __future__ import annotations
import json,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from common import devices,parallel,parser,run,write_csv,write_json,setup
log=setup("topology_redundancy");args=parser("Audit topologie et redondance").parse_args()
def audit(d):
 name=d.get("name",d["host"]);cdp=run(d,"show cdp neighbors detail",True);lldp=run(d,"show lldp neighbors detail",True);links=[]
 for proto,data in (("CDP",cdp),("LLDP",lldp)):
  if not isinstance(data,list):continue
  for x in data:links.append({"source":name,"local_port":x.get("local_port") or x.get("local_interface"),"neighbor":x.get("destination_host") or x.get("neighbor") or x.get("system_name"),"remote_port":x.get("remote_port") or x.get("neighbor_interface"),"protocol":proto,"platform":x.get("platform","")})
 return links
groups=parallel(devices(args.inventory),audit,args.workers);links=[x for g in groups for x in (g if isinstance(g,list) else [])];degree=defaultdict(set)
for x in links:degree[x["source"]].add(x["neighbor"])
findings=[{"device":d.get("name",d["host"]),"unique_neighbors":len(degree[d.get("name",d["host"])]),"result":"WARNING_SINGLE_PATH" if len(degree[d.get("name",d["host"])])<2 else "OK"} for d in devices(args.inventory)]
log.info("Liens: %s",write_csv("topology_links",links));log.info("Redondance: %s",write_csv("topology_redundancy",findings));write_json("topology_graph",{"nodes":sorted(degree),"links":links})

