"""
API endpoints for scan operations.
"""
import asyncio
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import Scan, ScanStatus, ScanType, Vulnerability, ScanResult
from app.schemas.scan import (
    ScanCreateSchema,
    ScanResponseSchema,
    ScanListResponseSchema,
)
from app.services.scanning_engine.orchestrator import ScanOrchestrator

router = APIRouter(prefix="/scans", tags=["scans"])


@router.post("/", response_model=ScanResponseSchema, status_code=201)
async def create_scan(
    scan_data: ScanCreateSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Create and start a new vulnerability scan.
    """
    try:
        # Create scan record
        scan = Scan(
            target=scan_data.target,
            scan_type=ScanType(scan_data.scan_config.scan_type),
            status=ScanStatus.PENDING,
            selected_tools=scan_data.scan_config.selected_tools,
            aggressiveness=scan_data.scan_config.aggressiveness,
            port_range=scan_data.scan_config.port_range,
            exclude_ports=scan_data.scan_config.exclude_ports,
            include_nse=scan_data.scan_config.include_nse,
            compliance_frameworks=scan_data.scan_config.compliance,
        )
        
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        # Start scan in background
        background_tasks.add_task(run_scan, scan.id, db)
        
        return scan.to_dict()
    except Exception as e:
        db.rollback()
        print(f"Error creating scan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create scan: {str(e)}")


async def run_scan(scan_id: int, db_session: Session):
    """Background task to execute the scan."""
    # Create a new database session for the background task
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return
        
        try:
            # Update status to running
            scan.status = ScanStatus.RUNNING
            scan.started_at = datetime.utcnow()
            db.commit()
            
            # Initialize orchestrator
            orchestrator = ScanOrchestrator(scan, db)
            
            # Run scan
            await orchestrator.execute()
            
            # Refresh scan object
            db.refresh(scan)
            
            # Update scan with results
            scan.status = ScanStatus.COMPLETED
            scan.completed_at = datetime.utcnow()
            if scan.started_at:
                scan.duration_seconds = (scan.completed_at - scan.started_at).total_seconds()
            
            # Count vulnerabilities
            vuln_counts = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
            scan.total_vulnerabilities = len(vuln_counts)
            scan.critical_count = sum(1 for v in vuln_counts if v.severity.value == "critical")
            scan.high_count = sum(1 for v in vuln_counts if v.severity.value == "high")
            scan.medium_count = sum(1 for v in vuln_counts if v.severity.value == "medium")
            scan.low_count = sum(1 for v in vuln_counts if v.severity.value == "low")
            
            db.commit()
            print(f"✅ Scan {scan_id} completed successfully")
            
        except Exception as e:
            scan.status = ScanStatus.FAILED
            db.commit()
            print(f"❌ Scan {scan_id} failed: {str(e)}")
            import traceback
            traceback.print_exc()
    finally:
        db.close()


@router.get("/", response_model=ScanListResponseSchema)
def list_scans(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    List all scans with pagination and filtering.
    """
    query = db.query(Scan)
    
    if status:
        query = query.filter(Scan.status == status)
    
    total = query.count()
    scans = query.order_by(desc(Scan.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "scans": [scan.to_dict() for scan in scans],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{scan_id}", response_model=ScanResponseSchema)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific scan.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return scan.to_dict()


@router.delete("/{scan_id}", status_code=204)
def delete_scan(scan_id: int, db: Session = Depends(get_db)):
    """
    Delete a scan and all associated data.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    db.delete(scan)
    db.commit()
    return None


@router.post("/{scan_id}/cancel", response_model=ScanResponseSchema)
def cancel_scan(scan_id: int, db: Session = Depends(get_db)):
    """
    Cancel a running scan.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    if scan.status != ScanStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Scan is not running")
    
    scan.status = ScanStatus.CANCELLED
    db.commit()
    
    return scan.to_dict()


@router.get("/{scan_id}/vulnerabilities")
def get_scan_vulnerabilities(
    scan_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all vulnerabilities discovered in a scan.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    vulnerabilities = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
    
    return {
        "scan_id": scan_id,
        "vulnerabilities": [v.to_dict() for v in vulnerabilities],
        "total": len(vulnerabilities),
    }


@router.get("/{scan_id}/results")
def get_scan_tool_results(
    scan_id: int,
    db: Session = Depends(get_db),
):
    """
    Get detailed tool-by-tool results for a scan.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    results = db.query(ScanResult).filter(ScanResult.scan_id == scan_id).all()
    
    return {
        "scan_id": scan_id,
        "results": [r.to_dict() for r in results],
        "total": len(results),
    }
