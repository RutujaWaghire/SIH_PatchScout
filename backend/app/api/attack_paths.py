"""
Attack path analysis API endpoints.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Scan, Vulnerability

router = APIRouter(prefix="/attack-paths", tags=["attack-paths"])


@router.get("/{scan_id}")
def get_attack_paths(scan_id: int, db: Session = Depends(get_db)):
    """
    Generate and retrieve attack paths for a scan.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    vulnerabilities = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
    
    # Generate attack paths based on vulnerabilities
    attack_paths = []
    
    # Path 1: External Reconnaissance -> Exploitation -> Privilege Escalation
    if any(v.port == 80 or v.port == 443 for v in vulnerabilities):
        web_vulns = [v for v in vulnerabilities if v.port in [80, 443]]
        critical_vulns = [v for v in vulnerabilities if v.severity.value == "critical"]
        
        if web_vulns and critical_vulns:
            attack_paths.append({
                "id": "path-1",
                "name": "Web Application Compromise",
                "severity": "critical",
                "steps": [
                    {
                        "id": "recon",
                        "name": "Reconnaissance",
                        "description": f"Attacker scans {scan.target} and identifies open web ports",
                        "mitre_id": "TA0043",
                        "technique": "Active Scanning"
                    },
                    {
                        "id": "exploit",
                        "name": "Initial Access",
                        "description": f"Exploit {web_vulns[0].title} on port {web_vulns[0].port}",
                        "mitre_id": "TA0001",
                        "technique": "Exploit Public-Facing Application",
                        "cve": web_vulns[0].cve_id
                    },
                    {
                        "id": "persistence",
                        "name": "Establish Persistence",
                        "description": "Attacker creates backdoor for continuous access",
                        "mitre_id": "TA0003",
                        "technique": "Web Shell"
                    },
                    {
                        "id": "escalate",
                        "name": "Privilege Escalation",
                        "description": "Elevate privileges to root/administrator",
                        "mitre_id": "TA0004",
                        "technique": "Exploitation for Privilege Escalation"
                    }
                ],
                "impact": "Complete system compromise with root access",
                "likelihood": "High",
                "recommendations": [
                    f"Immediately patch {web_vulns[0].cve_id}",
                    "Implement Web Application Firewall (WAF)",
                    "Enable intrusion detection",
                    "Regular security assessments"
                ]
            })
    
    # Path 2: SSH Brute Force -> Lateral Movement
    ssh_vulns = [v for v in vulnerabilities if v.port == 22 or "ssh" in v.service.lower() if v.service]
    if ssh_vulns:
        attack_paths.append({
            "id": "path-2",
            "name": "SSH Brute Force Attack",
            "severity": "high",
            "steps": [
                {
                    "id": "scan",
                    "name": "Network Scanning",
                    "description": f"Identify SSH service on port 22",
                    "mitre_id": "TA0043",
                    "technique": "Active Scanning"
                },
                {
                    "id": "brute-force",
                    "name": "Credential Access",
                    "description": "Brute force SSH credentials",
                    "mitre_id": "TA0006",
                    "technique": "Brute Force"
                },
                {
                    "id": "lateral",
                    "name": "Lateral Movement",
                    "description": "Move to other systems on network",
                    "mitre_id": "TA0008",
                    "technique": "Remote Services: SSH"
                },
                {
                    "id": "exfiltration",
                    "name": "Data Exfiltration",
                    "description": "Extract sensitive data",
                    "mitre_id": "TA0010",
                    "technique": "Exfiltration Over C2 Channel"
                }
            ],
            "impact": "Unauthorized access to sensitive data",
            "likelihood": "Medium",
            "recommendations": [
                "Implement key-based authentication",
                "Disable password authentication",
                "Use fail2ban or similar tools",
                "Enable multi-factor authentication"
            ]
        })
    
    # Path 3: Database Exploitation
    db_vulns = [v for v in vulnerabilities if any(db in (v.service or "").lower() for db in ["mysql", "postgresql", "mssql", "mongodb"])]
    if db_vulns:
        attack_paths.append({
            "id": "path-3",
            "name": "Database Breach",
            "severity": "critical",
            "steps": [
                {
                    "id": "discover",
                    "name": "Discovery",
                    "description": f"Identify exposed database on port {db_vulns[0].port}",
                    "mitre_id": "TA0043",
                    "technique": "Network Service Discovery"
                },
                {
                    "id": "exploit-db",
                    "name": "Exploitation",
                    "description": "Exploit database vulnerability or weak credentials",
                    "mitre_id": "TA0001",
                    "technique": "Valid Accounts"
                },
                {
                    "id": "collection",
                    "name": "Data Collection",
                    "description": "Extract database contents",
                    "mitre_id": "TA0009",
                    "technique": "Data from Information Repositories"
                },
                {
                    "id": "impact",
                    "name": "Impact",
                    "description": "Data breach, ransomware, or data destruction",
                    "mitre_id": "TA0040",
                    "technique": "Data Encrypted for Impact"
                }
            ],
            "impact": "Massive data breach affecting customer data",
            "likelihood": "High",
            "recommendations": [
                "Never expose databases directly to internet",
                "Use strong authentication",
                "Encrypt data at rest and in transit",
                "Implement database firewall rules"
            ]
        })
    
    # Calculate overall risk
    total_paths = len(attack_paths)
    critical_paths = sum(1 for p in attack_paths if p["severity"] == "critical")
    
    return {
        "scan_id": scan_id,
        "target": scan.target,
        "attack_paths": attack_paths,
        "summary": {
            "total_paths": total_paths,
            "critical_paths": critical_paths,
            "high_paths": sum(1 for p in attack_paths if p["severity"] == "high"),
            "overall_risk": "Critical" if critical_paths > 0 else "High" if total_paths > 0 else "Low"
        },
        "mitre_attack_mapping": {
            "tactics": ["TA0043", "TA0001", "TA0003", "TA0004", "TA0006", "TA0008", "TA0009", "TA0010", "TA0040"],
            "techniques_count": len(attack_paths) * 4
        }
    }


@router.get("/{scan_id}/graph")
def get_attack_graph(scan_id: int, db: Session = Depends(get_db)):
    """
    Get attack graph data for visualization.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    vulnerabilities = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
    
    # Generate graph nodes and edges
    nodes = [
        {"id": "attacker", "label": "Attacker", "type": "threat-actor", "risk": "critical"},
        {"id": "target", "label": scan.target, "type": "asset", "risk": "target"}
    ]
    
    edges = []
    
    # Add vulnerability nodes and edges
    for i, vuln in enumerate(vulnerabilities[:10]):  # Limit to 10 for visualization
        node_id = f"vuln-{vuln.id}"
        nodes.append({
            "id": node_id,
            "label": vuln.title[:30] + "..." if len(vuln.title) > 30 else vuln.title,
            "type": "vulnerability",
            "risk": vuln.severity.value,
            "cve": vuln.cve_id,
            "cvss": vuln.cvss_score
        })
        
        # Edge from attacker to vulnerability
        edges.append({
            "from": "attacker",
            "to": node_id,
            "type": "exploits",
            "label": f"Port {vuln.port}" if vuln.port else "Network"
        })
        
        # Edge from vulnerability to target
        edges.append({
            "from": node_id,
            "to": "target",
            "type": "compromises",
            "label": vuln.exploit_status.value
        })
    
    return {
        "nodes": nodes,
        "edges": edges,
        "layout": "hierarchical"
    }
