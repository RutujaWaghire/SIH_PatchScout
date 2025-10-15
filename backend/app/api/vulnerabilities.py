"""
Vulnerabilities API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import Vulnerability, Scan
from app.schemas.vulnerability import (
    VulnerabilityResponseSchema,
    VulnerabilityListResponseSchema,
    VulnerabilityFilterSchema
)

router = APIRouter(prefix="/vulnerabilities", tags=["vulnerabilities"])


@router.get("/", response_model=VulnerabilityListResponseSchema)
def list_vulnerabilities(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    severity: Optional[str] = None,
    scan_id: Optional[int] = None,
    cve_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    List all vulnerabilities with filtering and pagination.
    """
    query = db.query(Vulnerability)
    
    # Apply filters
    if severity:
        query = query.filter(Vulnerability.severity == severity)
    if scan_id:
        query = query.filter(Vulnerability.scan_id == scan_id)
    if cve_id:
        query = query.filter(Vulnerability.cve_id.contains(cve_id))
    
    total = query.count()
    vulnerabilities = query.order_by(desc(Vulnerability.discovered_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "vulnerabilities": [v.to_dict() for v in vulnerabilities],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{vuln_id}", response_model=VulnerabilityResponseSchema)
def get_vulnerability(vuln_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific vulnerability.
    """
    vulnerability = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    return vulnerability.to_dict()


@router.patch("/{vuln_id}/false-positive")
def mark_false_positive(vuln_id: int, is_false_positive: bool, db: Session = Depends(get_db)):
    """
    Mark a vulnerability as false positive or true positive.
    """
    vulnerability = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    vulnerability.false_positive = is_false_positive
    db.commit()
    
    return {"message": "Updated successfully", "vulnerability": vulnerability.to_dict()}


@router.patch("/{vuln_id}/verify")
def verify_vulnerability(vuln_id: int, verified: bool, db: Session = Depends(get_db)):
    """
    Mark a vulnerability as verified or unverified.
    """
    vulnerability = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    vulnerability.verified = verified
    db.commit()
    
    return {"message": "Updated successfully", "vulnerability": vulnerability.to_dict()}


@router.get("/stats/summary")
def get_vulnerability_summary(db: Session = Depends(get_db)):
    """
    Get vulnerability statistics summary.
    """
    from app.models import SeverityLevel
    
    total = db.query(Vulnerability).count()
    critical = db.query(Vulnerability).filter(Vulnerability.severity == SeverityLevel.CRITICAL).count()
    high = db.query(Vulnerability).filter(Vulnerability.severity == SeverityLevel.HIGH).count()
    medium = db.query(Vulnerability).filter(Vulnerability.severity == SeverityLevel.MEDIUM).count()
    low = db.query(Vulnerability).filter(Vulnerability.severity == SeverityLevel.LOW).count()
    
    return {
        "total": total,
        "by_severity": {
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
        },
        "risk_score": (critical * 10 + high * 7 + medium * 4 + low * 1) / max(total, 1)
    }
