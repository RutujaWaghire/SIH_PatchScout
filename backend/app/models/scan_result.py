"""
Scan result database model for storing detailed tool-specific outputs.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float, Enum
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class ToolStatus(str, enum.Enum):
    """Enumeration for individual tool scan status."""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


class ScanResult(Base):
    """Model for individual tool scan results."""
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False, index=True)
    
    # Tool information
    tool_name = Column(String, nullable=False, index=True)  # Nmap, OpenVAS, etc.
    tool_version = Column(String, nullable=True)
    status = Column(Enum(ToolStatus), default=ToolStatus.IDLE)
    
    # Execution details
    command = Column(Text, nullable=True)  # Command executed
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    
    # Results
    raw_output = Column(Text, nullable=True)  # Raw tool output
    parsed_output = Column(JSON, nullable=True)  # Structured parsed data
    error_message = Column(Text, nullable=True)
    exit_code = Column(Integer, nullable=True)
    
    # Statistics
    vulnerabilities_found = Column(Integer, default=0)
    ports_scanned = Column(Integer, nullable=True)
    hosts_scanned = Column(Integer, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    scan = relationship("Scan", back_populates="scan_results")

    def __repr__(self):
        return f"<ScanResult(id={self.id}, tool={self.tool_name}, status={self.status})>"

    def to_dict(self):
        """Convert scan result to dictionary."""
        return {
            "id": self.id,
            "scan_id": self.scan_id,
            "tool_name": self.tool_name,
            "tool_version": self.tool_version,
            "status": self.status.value if self.status else None,
            "command": self.command,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "vulnerabilities_found": self.vulnerabilities_found,
            "ports_scanned": self.ports_scanned,
            "error_message": self.error_message,
            "exit_code": self.exit_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
