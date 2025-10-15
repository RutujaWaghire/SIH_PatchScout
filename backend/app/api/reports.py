"""
Reports generation API endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.database import get_db
from app.models import Scan, Vulnerability, ScanResult

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{scan_id}/json")
def generate_json_report(scan_id: int, db: Session = Depends(get_db)):
    """
    Generate comprehensive JSON report for a scan.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    vulnerabilities = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
    scan_results = db.query(ScanResult).filter(ScanResult.scan_id == scan_id).all()
    
    report = {
        "report_metadata": {
            "generated_at": datetime.utcnow().isoformat(),
            "report_type": "vulnerability_scan",
            "patchscout_version": "1.0.0"
        },
        "scan_information": {
            "scan_id": scan.id,
            "target": scan.target,
            "scan_type": scan.scan_type.value,
            "status": scan.status.value,
            "started_at": scan.started_at.isoformat() if scan.started_at else None,
            "completed_at": scan.completed_at.isoformat() if scan.completed_at else None,
            "duration_seconds": scan.duration_seconds,
            "tools_used": scan.selected_tools,
            "aggressiveness": scan.aggressiveness,
            "port_range": scan.port_range
        },
        "executive_summary": {
            "total_vulnerabilities": scan.total_vulnerabilities,
            "severity_breakdown": {
                "critical": scan.critical_count,
                "high": scan.high_count,
                "medium": scan.medium_count,
                "low": scan.low_count
            },
            "risk_score": (scan.critical_count * 10 + scan.high_count * 7 + 
                          scan.medium_count * 4 + scan.low_count * 1) / max(scan.total_vulnerabilities, 1),
            "open_ports": scan.open_ports_count,
            "services_detected": scan.services_detected,
            "os_fingerprint": scan.os_fingerprint
        },
        "vulnerabilities": [
            {
                "id": v.id,
                "cve_id": v.cve_id,
                "title": v.title,
                "description": v.description,
                "severity": v.severity.value,
                "cvss_score": v.cvss_score,
                "cvss_vector": v.cvss_vector,
                "affected_component": v.affected_component,
                "affected_version": v.affected_version,
                "port": v.port,
                "service": v.service,
                "discovered_by": v.discovered_by,
                "exploit_status": v.exploit_status.value,
                "solution": v.solution,
                "recommendation": v.recommendation,
                "references": v.references,
                "mitre_attack_ids": v.mitre_attack_ids,
                "cwe_ids": v.cwe_ids,
                "tags": v.tags
            }
            for v in vulnerabilities
        ],
        "tool_results": [
            {
                "tool_name": sr.tool_name,
                "status": sr.status.value,
                "duration_seconds": sr.duration_seconds,
                "vulnerabilities_found": sr.vulnerabilities_found,
                "ports_scanned": sr.ports_scanned,
                "started_at": sr.started_at.isoformat() if sr.started_at else None,
                "completed_at": sr.completed_at.isoformat() if sr.completed_at else None
            }
            for sr in scan_results
        ],
        "recommendations": [
            {
                "priority": "Critical",
                "action": f"Immediately patch {scan.critical_count} critical vulnerabilities",
                "impact": "Prevents immediate exploitation",
                "effort": "High"
            },
            {
                "priority": "High",
                "action": f"Address {scan.high_count} high-severity vulnerabilities within 7 days",
                "impact": "Reduces attack surface",
                "effort": "Medium"
            },
            {
                "priority": "Medium",
                "action": "Implement continuous security monitoring",
                "impact": "Early threat detection",
                "effort": "Low"
            },
            {
                "priority": "Low",
                "action": "Regular vulnerability scans (weekly/monthly)",
                "impact": "Proactive security posture",
                "effort": "Low"
            }
        ]
    }
    
    return JSONResponse(content=report)


@router.get("/{scan_id}/summary")
def generate_summary_report(scan_id: int, db: Session = Depends(get_db)):
    """
    Generate executive summary report.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    vulnerabilities = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
    
    # Group by severity
    critical_vulns = [v for v in vulnerabilities if v.severity.value == "critical"]
    high_vulns = [v for v in vulnerabilities if v.severity.value == "high"]
    
    # Calculate risk
    risk_score = (len(critical_vulns) * 10 + len(high_vulns) * 7) / max(len(vulnerabilities), 1)
    
    return {
        "scan_id": scan.id,
        "target": scan.target,
        "scan_date": scan.started_at.isoformat() if scan.started_at else None,
        "summary": {
            "total_vulnerabilities": len(vulnerabilities),
            "critical": len(critical_vulns),
            "high": len(high_vulns),
            "risk_score": round(risk_score, 2),
            "risk_level": "Critical" if risk_score > 7 else "High" if risk_score > 4 else "Medium" if risk_score > 2 else "Low"
        },
        "top_vulnerabilities": [
            {
                "title": v.title,
                "severity": v.severity.value,
                "cvss": v.cvss_score,
                "cve": v.cve_id,
                "solution": v.solution
            }
            for v in sorted(vulnerabilities, key=lambda x: x.cvss_score or 0, reverse=True)[:5]
        ],
        "compliance_status": {
            "pci_dss": "Non-Compliant" if risk_score > 5 else "Partially Compliant",
            "nist": "Non-Compliant" if risk_score > 6 else "Partially Compliant",
            "iso_27001": "Non-Compliant" if risk_score > 5 else "Partially Compliant"
        },
        "next_steps": [
            "Patch critical vulnerabilities immediately",
            "Implement WAF for web applications",
            "Enable intrusion detection systems",
            "Conduct penetration testing",
            "Schedule regular security assessments"
        ]
    }


@router.get("/{scan_id}/csv")
def generate_csv_report(scan_id: int, db: Session = Depends(get_db)):
    """
    Generate CSV export of vulnerabilities.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    vulnerabilities = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
    
    # Generate CSV content
    csv_content = "ID,CVE,Title,Severity,CVSS,Port,Service,Component,Exploit Status,Solution\n"
    
    for v in vulnerabilities:
        csv_content += f'"{v.id}","{v.cve_id or "N/A"}","{v.title}","{v.severity.value}","{v.cvss_score or "N/A"}","{v.port or "N/A"}","{v.service or "N/A"}","{v.affected_component or "N/A"}","{v.exploit_status.value}","{(v.solution or "")[:100]}"\n'
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=patchscout_scan_{scan_id}_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        }
    )


@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get aggregated statistics for dashboard.
    """
    from app.models import SeverityLevel, ScanStatus
    
    total_scans = db.query(Scan).count()
    active_scans = db.query(Scan).filter(Scan.status == ScanStatus.RUNNING).count()
    completed_scans = db.query(Scan).filter(Scan.status == ScanStatus.COMPLETED).count()
    
    total_vulns = db.query(Vulnerability).count()
    critical_vulns = db.query(Vulnerability).filter(Vulnerability.severity == SeverityLevel.CRITICAL).count()
    high_vulns = db.query(Vulnerability).filter(Vulnerability.severity == SeverityLevel.HIGH).count()
    medium_vulns = db.query(Vulnerability).filter(Vulnerability.severity == SeverityLevel.MEDIUM).count()
    low_vulns = db.query(Vulnerability).filter(Vulnerability.severity == SeverityLevel.LOW).count()
    
    # Recent scans
    recent_scans = db.query(Scan).order_by(Scan.created_at.desc()).limit(5).all()
    
    return {
        "scans": {
            "total": total_scans,
            "active": active_scans,
            "completed": completed_scans,
            "failed": db.query(Scan).filter(Scan.status == ScanStatus.FAILED).count()
        },
        "vulnerabilities": {
            "total": total_vulns,
            "critical": critical_vulns,
            "high": high_vulns,
            "medium": medium_vulns,
            "low": low_vulns
        },
        "risk_score": (critical_vulns * 10 + high_vulns * 7 + medium_vulns * 4 + low_vulns * 1) / max(total_vulns, 1),
        "recent_scans": [
            {
                "id": s.id,
                "target": s.target,
                "status": s.status.value,
                "vulnerabilities": s.total_vulnerabilities,
                "created_at": s.created_at.isoformat()
            }
            for s in recent_scans
        ]
    }
