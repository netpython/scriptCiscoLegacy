#!/usr/bin/env python3
"""Analyse capacité, erreurs, ports inutilisés et cohérence des descriptions."""
from __future__ import annotations
import re,sys
from pathlib import Path
from openpyxl import Workbook
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from common import devices,parallel,parser,run,stamp,OUTPUT,setup
log=setup("interface_capacity");args=parser("Audit capacité interfaces").parse_args()
def audit(d):
 name=d.get("name",d["host"]);status=run(d,"show interfaces status",True);errors=run(d,"show interfaces counters errors",True);rows=[]
 if not isinstance(status,list):return [{"device":name,"error":"TextFSM indisponible","raw":str(status)}]
 errmap={str(x.get("port") or x.get("interface")):x for x in errors} if isinstance(errors,list) else {}
 for x in status:
  port=str(x.get("port") or x.get("interface") or "");state=str(x.get("status","")).lower();desc=x.get("name") or x.get("description") or "";e=errmap.get(port,{})
  total=sum(int(e.get(k) or 0) for k in e if k not in {"port","interface"} and str(e.get(k) or "0").isdigit())
  finding="ERRORS" if total else "UP_NO_DESCRIPTION" if state=="connected" and not desc else "UNUSED_ENABLED" if state in {"notconnect","disabled"} else "OK"
  rows.append({"device":name,"port":port,"status":state,"description":desc,"vlan":x.get("vlan"),"duplex":x.get("duplex"),"speed":x.get("speed"),"error_total":total,"finding":finding})
 return rows
groups=parallel(devices(args.inventory),audit,args.workers);rows=[x for g in groups for x in (g if isinstance(g,list) else [g])];wb=Workbook();ws=wb.active;ws.title="Interfaces";headers=sorted({k for r in rows for k in r});ws.append(headers)
for r in rows:ws.append([r.get(h,"") for h in headers])
ws.freeze_panes="A2";ws.auto_filter.ref=ws.dimensions;path=OUTPUT/f"interface_capacity_{stamp()}.xlsx";wb.save(path);log.info("Rapport: %s",path)

