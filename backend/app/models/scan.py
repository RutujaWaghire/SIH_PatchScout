"""
Scan database model for storing scan configurations and metadata.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum, Float
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class ScanStatus(str, enum.Enum):
    """Enumeration for scan status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScanType(str, enum.Enum):
    """Enumeration for scan types."""
    QUICK = "quick"
    COMPREHENSIVE = "comprehensive"
    STEALTH = "stealth"
    CUSTOM = "custom"


class Scan(Base):
    """Model for vulnerability scans."""
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, nullable=False, index=True)
    scan_type = Column(Enum(ScanType), default=ScanType.COMPREHENSIVE)
    status = Column(Enum(ScanStatus), default=ScanStatus.PENDING, index=True)
    
    # Scan configuration
    selected_tools = Column(JSON, default=list)  # List of tool names
    aggressiveness = Column(String, default="medium")  # low, medium, high
    port_range = Column(String, default="1-65535")
    exclude_ports = Column(String, nullable=True)
    include_nse = Column(JSON, default=True)
    compliance_frameworks = Column(JSON, default=list)
    
    # Results summary
    total_vulnerabilities = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    
    # Network findings
    open_ports_count = Column(Integer, default=0)
    services_detected = Column(Integer, default=0)
    os_fingerprint = Column(String, nullable=True)
    
    # Metadata
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    estimated_time_minutes = Column(Integer, default=0)
    
    # User and tracking
    user_id = Column(String, nullable=True, index=True)
    scan_config_hash = Column(String, nullable=True)  # For deduplication
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vulnerabilities = relationship("Vulnerability", back_populates="scan", cascade="all, delete-orphan")
    scan_results = relationship("ScanResult", back_populates="scan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scan(id={self.id}, target={self.target}, status={self.status})>"

    def to_dict(self):
        """Convert scan to dictionary."""
        # Calculate progress based on completed scan results
        progress = 0
        current_tool = None
        
        if self.status == ScanStatus.COMPLETED:
            progress = 100
        elif self.status == ScanStatus.RUNNING:
            # Check scan_results to determine progress
            completed_tools = len([r for r in self.scan_results if r.status.value == "complete"])
            total_tools = len(self.selected_tools) if self.selected_tools else 1
            progress = int((completed_tools / total_tools) * 100) if total_tools > 0 else 0
            
            # Find currently running tool
            running_results = [r for r in self.scan_results if r.status.value == "running"]
            if running_results:
                current_tool = running_results[0].tool_name
        
        return {
            "id": self.id,
            "target": self.target,
            "scan_type": self.scan_type.value if self.scan_type else None,
            "status": self.status.value if self.status else None,
            "progress": progress,
            "current_tool": current_tool,
            "selected_tools": self.selected_tools,
            "aggressiveness": self.aggressiveness,
            "port_range": self.port_range,
            "vulnerabilities_count": self.total_vulnerabilities,
            "critical_count": self.critical_count,
            "high_count": self.high_count,
            "medium_count": self.medium_count,
            "low_count": self.low_count,
            "open_ports_count": self.open_ports_count,
            "services_detected": self.services_detected,
            "os_fingerprint": self.os_fingerprint,
            "summary": {
                "total_vulnerabilities": self.total_vulnerabilities,
                "critical": self.critical_count,
                "high": self.high_count,
                "medium": self.medium_count,
                "low": self.low_count,
                "open_ports": self.open_ports_count,
                "services": self.services_detected,
            },
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
