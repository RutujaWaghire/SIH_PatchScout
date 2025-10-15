"""
Pydantic schemas for scan operations.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ScanConfigSchema(BaseModel):
    """Schema for scan configuration."""
    selected_tools: List[str] = Field(default_factory=lambda: ["Nmap", "OpenVAS", "Nessus", "Nikto", "Nuclei"])
    scan_type: str = Field(default="comprehensive")
    aggressiveness: str = Field(default="medium")
    port_range: str = Field(default="1-65535")
    exclude_ports: Optional[str] = None
    include_nse: bool = True
    compliance: List[str] = Field(default_factory=list)


class ScanCreateSchema(BaseModel):
    """Schema for creating a new scan."""
    target: str = Field(..., description="Target URL, IP, or domain")
    scan_config: ScanConfigSchema = Field(default_factory=ScanConfigSchema)


class ScanResponseSchema(BaseModel):
    """Schema for scan response."""
    id: int
    target: str
    scan_type: str
    status: str
    selected_tools: List[str]
    summary: dict
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class ScanListResponseSchema(BaseModel):
    """Schema for list of scans."""
    scans: List[ScanResponseSchema]
    total: int
    page: int
    page_size: int
