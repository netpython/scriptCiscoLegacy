# scriptCiscoLegacy

Collection de 15 scripts Python pour administrer et auditer des équipements Cisco IOS / IOS-XE historiques via SSH.

## Fonctions incluses

| # | Script | Fonction |
|---|---|---|
| 01 | `01_inventory.py` | Inventaire modèle, série et version |
| 02 | `02_backup_configs.py` | Sauvegarde running/startup-config |
| 03 | `03_interface_status.py` | État des interfaces en CSV |
| 04 | `04_vlan_audit.py` | Audit VLAN et ports associés |
| 05 | `05_trunk_audit.py` | Audit des trunks 802.1Q |
| 06 | `06_cdp_neighbors.py` | Cartographie CDP |
| 07 | `07_lldp_neighbors.py` | Cartographie LLDP |
| 08 | `08_mac_table.py` | Export table MAC |
| 09 | `09_arp_table.py` | Export table ARP |
| 10 | `10_stp_audit.py` | Vérification STP/root bridge |
| 11 | `11_port_security.py` | Audit port-security |
| 12 | `12_errdisabled_ports.py` | Détection ports err-disabled |
| 13 | `13_config_compliance.py` | Contrôles de conformité regex |
| 14 | `14_bulk_command.py` | Exécution d'une commande show |
| 15 | `15_config_deployer.py` | Déploiement contrôlé de configuration |

## Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp inventory.example.yml inventory.yml
export CISCO_USERNAME='admin'
export CISCO_PASSWORD='mot-de-passe'
export CISCO_SECRET='enable-secret'
```

## Utilisation

```bash
python scripts/01_inventory.py -i inventory.yml
python scripts/02_backup_configs.py -i inventory.yml
python scripts/14_bulk_command.py -i inventory.yml --command "show ip interface brief"
python scripts/15_config_deployer.py -i inventory.yml --config configs/example.txt --dry-run
```

Les résultats sont placés dans `outputs/` et les journaux dans `logs/`. Les identifiants ne doivent jamais être enregistrés dans Git.

## Sécurité

- Tester d'abord en laboratoire.
- Utiliser `--dry-run` avant tout déploiement.
- Limiter les comptes SSH aux privilèges nécessaires.
- Sauvegarder les configurations avant une modification.

## Compatibilité

Python 3.11, Netmiko 4.x, Cisco IOS et IOS-XE accessibles en SSH. Certains parseurs TextFSM peuvent dépendre de la version de commande retournée par l'équipement.

## Licence

MIT.

