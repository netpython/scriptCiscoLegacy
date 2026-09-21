#!/usr/bin/env python3
"""Sauvegarde les configurations et détecte les dérives entre deux exécutions."""
from __future__ import annotations
import difflib,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from common import devices,parallel,parser,run,stamp,OUTPUT,setup
log=setup("backup_drift");p=parser("Backup et dérive de configuration");p.add_argument("--baseline",default="baselines");p.add_argument("--update-baseline",action="store_true");args=p.parse_args();base=Path(args.baseline);base.mkdir(exist_ok=True)
def normalize(text):return "\n".join(x.rstrip() for x in text.splitlines() if not x.startswith(("Building configuration","Current configuration","Last configuration change")))+"\n"
def audit(d):
 name=d.get("name",d["host"]);cfg=normalize(run(d,"show running-config"));digest=hashlib.sha256(cfg.encode()).hexdigest();target=base/f"{name}.cfg";previous=target.read_text(encoding="utf-8") if target.exists() else "";changed=bool(previous and previous!=cfg)
 diff="\n".join(difflib.unified_diff(previous.splitlines(),cfg.splitlines(),fromfile="baseline",tofile="current",lineterm="")) if changed else ""
 if args.update_baseline or not target.exists():target.write_text(cfg,encoding="utf-8")
 return {"device":name,"host":d["host"],"sha256":digest,"baseline_exists":bool(previous),"changed":changed,"diff_lines":len(diff.splitlines()),"diff":diff}
results=parallel(devices(args.inventory),audit,args.workers);folder=OUTPUT/f"drift_{stamp()}";folder.mkdir()
for r in results:
 if r.get("diff"):(folder/f"{r['device']}.diff").write_text(r.pop("diff"),encoding="utf-8")
(folder/"summary.json").write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding="utf-8");log.info("Rapport: %s",folder)

