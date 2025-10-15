"""
CVE data model for storing vulnerability intelligence from NVD and other sources.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON, Boolean
from sqlalchemy import Index

from app.database import Base


class CVEData(Base):
    """Model for CVE intelligence data."""
    __tablename__ = "cve_data"

    id = Column(Integer, primary_key=True, index=True)
    
    # CVE identification
    cve_id = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    
    # CVSS scoring
    cvss_v3_score = Column(Float, nullable=True)
    cvss_v3_vector = Column(String, nullable=True)
    cvss_v2_score = Column(Float, nullable=True)
    cvss_v2_vector = Column(String, nullable=True)
    severity = Column(String, nullable=True, index=True)
    
    # CWE and categorization
    cwe_ids = Column(JSON, default=list)
    vulnerability_types = Column(JSON, default=list)  # e.g., ['SQL Injection', 'XSS']
    
    # Publication dates
    published_date = Column(DateTime, nullable=True)
    last_modified_date = Column(DateTime, nullable=True)
    
    # Affected products
    affected_vendors = Column(JSON, default=list)
    affected_products = Column(JSON, default=list)
    affected_versions = Column(JSON, default=list)
    
    # Exploit information
    exploit_available = Column(Boolean, default=False)
    exploit_maturity = Column(String, nullable=True)  # unproven, poc, functional, high
    exploit_references = Column(JSON, default=list)
    
    # References and resources
    references = Column(JSON, default=list)  # List of reference URLs
    nvd_url = Column(String, nullable=True)
    mitre_url = Column(String, nullable=True)
    
    # MITRE ATT&CK mapping
    mitre_attack_techniques = Column(JSON, default=list)
    mitre_attack_tactics = Column(JSON, default=list)
    
    # Threat intelligence
    trending = Column(Boolean, default=False)
    actively_exploited = Column(Boolean, default=False)
    ransomware_used = Column(Boolean, default=False)
    apt_groups = Column(JSON, default=list)  # APT groups exploiting this CVE
    
    # Remediation
    patch_available = Column(Boolean, default=False)
    vendor_advisories = Column(JSON, default=list)
    mitigation_strategies = Column(Text, nullable=True)
    
    # Additional metadata
    epss_score = Column(Float, nullable=True)  # Exploit Prediction Scoring System
    epss_percentile = Column(Float, nullable=True)
    kev_listed = Column(Boolean, default=False)  # CISA Known Exploited Vulnerabilities
    
    # Source tracking
    data_source = Column(String, default="NVD")  # NVD, ExploitDB, MITRE, etc.
    last_synced = Column(DateTime, default=datetime.utcnow)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Composite index for common queries
    __table_args__ = (
        Index('ix_cve_severity_exploit', 'severity', 'exploit_available'),
        Index('ix_cve_trending_exploited', 'trending', 'actively_exploited'),
    )

    def __repr__(self):
        return f"<CVEData(cve_id={self.cve_id}, severity={self.severity})>"

    def to_dict(self):
        """Convert CVE data to dictionary."""
        return {
            "id": self.id,
            "cve_id": self.cve_id,
            "title": self.title,
            "description": self.description,
            "cvss_v3_score": self.cvss_v3_score,
            "cvss_v3_vector": self.cvss_v3_vector,
            "severity": self.severity,
            "cwe_ids": self.cwe_ids,
            "vulnerability_types": self.vulnerability_types,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "last_modified_date": self.last_modified_date.isoformat() if self.last_modified_date else None,
            "affected_vendors": self.affected_vendors,
            "affected_products": self.affected_products,
            "exploit_available": self.exploit_available,
            "exploit_maturity": self.exploit_maturity,
            "references": self.references,
            "mitre_attack_techniques": self.mitre_attack_techniques,
            "trending": self.trending,
            "actively_exploited": self.actively_exploited,
            "patch_available": self.patch_available,
            "epss_score": self.epss_score,
            "kev_listed": self.kev_listed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
