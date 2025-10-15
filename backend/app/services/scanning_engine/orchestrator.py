"""
Scan orchestrator - coordinates multiple security scanners.
"""
import asyncio
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models import Scan, Vulnerability, ScanResult, SeverityLevel, ExploitStatus, ToolStatus
from app.services.scanning_engine.nmap_scanner import NmapScanner


class ScanOrchestrator:
    """Orchestrates multiple security scanning tools."""
    
    def __init__(self, scan: Scan, db: Session):
        self.scan = scan
        self.db = db
        self.results = []
        
    async def execute(self):
        """Execute all selected scanning tools."""
        tasks = []
        
        for tool_name in self.scan.selected_tools:
            if tool_name == "Nmap":
                tasks.append(self._run_nmap())
            elif tool_name == "OpenVAS":
                tasks.append(self._run_openvas())
            elif tool_name == "Nessus":
                tasks.append(self._run_nessus())
            elif tool_name == "Nikto":
                tasks.append(self._run_nikto())
            elif tool_name == "Nuclei":
                tasks.append(self._run_nuclei())
        
        # Run all scans concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                print(f"Scan task failed: {result}")
            elif result:
                self._save_results(result)
    
    async def _run_nmap(self) -> Dict[str, Any]:
        """Run Nmap scan."""
        # Create scan result record
        scan_result = ScanResult(
            scan_id=self.scan.id,
            tool_name="Nmap",
            status=ToolStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        self.db.add(scan_result)
        self.db.commit()
        
        try:
            # Initialize and run Nmap scanner
            scanner = NmapScanner(
                target=self.scan.target,
                port_range=self.scan.port_range,
                aggressiveness=self.scan.aggressiveness
            )
            
            result = await scanner.scan()
            
            # Update scan result
            scan_result.status = ToolStatus.COMPLETE
            scan_result.completed_at = datetime.utcnow()
            scan_result.duration_seconds = (scan_result.completed_at - scan_result.started_at).total_seconds()
            scan_result.parsed_output = result
            scan_result.vulnerabilities_found = len(result.get('vulnerabilities', []))
            scan_result.ports_scanned = result.get('ports_found', 0)
            
            # Update scan metadata
            self.scan.open_ports_count = result.get('ports_found', 0)
            self.scan.services_detected = result.get('services_found', 0)
            self.scan.os_fingerprint = result.get('os_fingerprint', 'Unknown')
            
            self.db.commit()
            
            return result
            
        except Exception as e:
            scan_result.status = ToolStatus.FAILED
            scan_result.error_message = str(e)
            scan_result.completed_at = datetime.utcnow()
            self.db.commit()
            raise
    
    async def _run_openvas(self) -> Dict[str, Any]:
        """Run OpenVAS scan (mock implementation)."""
        scan_result = ScanResult(
            scan_id=self.scan.id,
            tool_name="OpenVAS",
            status=ToolStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        self.db.add(scan_result)
        self.db.commit()
        
        # Simulate scan duration
        await asyncio.sleep(3)
        
        # Mock vulnerabilities
        result = {
            "success": True,
            "tool": "OpenVAS",
            "target": self.scan.target,
            "vulnerabilities": [
                {
                    "cve_id": "CVE-2024-3456",
                    "title": "SQL Injection in Web Application",
                    "description": "SQL injection vulnerability allows unauthorized database access",
                    "severity": "high",
                    "cvss_score": 8.6,
                    "affected_component": "Web Application",
                    "discovered_by": "OpenVAS",
                    "exploit_status": "poc_available",
                    "solution": "Implement parameterized queries and input validation",
                    "references": ["https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-3456"],
                }
            ]
        }
        
        scan_result.status = ToolStatus.COMPLETE
        scan_result.completed_at = datetime.utcnow()
        scan_result.duration_seconds = (scan_result.completed_at - scan_result.started_at).total_seconds()
        scan_result.parsed_output = result
        scan_result.vulnerabilities_found = len(result['vulnerabilities'])
        self.db.commit()
        
        return result
    
    async def _run_nessus(self) -> Dict[str, Any]:
        """Run Nessus scan (mock implementation)."""
        scan_result = ScanResult(
            scan_id=self.scan.id,
            tool_name="Nessus",
            status=ToolStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        self.db.add(scan_result)
        self.db.commit()
        
        await asyncio.sleep(2)
        
        result = {
            "success": True,
            "tool": "Nessus",
            "target": self.scan.target,
            "vulnerabilities": [
                {
                    "cve_id": "CVE-2024-7890",
                    "title": "Outdated SSL/TLS Configuration",
                    "description": "Server supports outdated SSL/TLS protocols",
                    "severity": "medium",
                    "cvss_score": 5.9,
                    "affected_component": "SSL/TLS Service",
                    "port": 443,
                    "service": "https",
                    "discovered_by": "Nessus",
                    "exploit_status": "manual",
                    "solution": "Disable SSLv3 and TLS 1.0/1.1, enable TLS 1.2/1.3 only",
                    "references": ["https://www.nessus.org/plugins/"],
                }
            ]
        }
        
        scan_result.status = ToolStatus.COMPLETE
        scan_result.completed_at = datetime.utcnow()
        scan_result.duration_seconds = (scan_result.completed_at - scan_result.started_at).total_seconds()
        scan_result.parsed_output = result
        scan_result.vulnerabilities_found = len(result['vulnerabilities'])
        self.db.commit()
        
        return result
    
    async def _run_nikto(self) -> Dict[str, Any]:
        """Run Nikto scan (mock implementation)."""
        scan_result = ScanResult(
            scan_id=self.scan.id,
            tool_name="Nikto",
            status=ToolStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        self.db.add(scan_result)
        self.db.commit()
        
        await asyncio.sleep(2)
        
        result = {
            "success": True,
            "tool": "Nikto",
            "target": self.scan.target,
            "vulnerabilities": [
                {
                    "title": "Exposed Admin Panel",
                    "description": "Admin panel accessible without authentication at /admin",
                    "severity": "high",
                    "cvss_score": 7.5,
                    "affected_component": "Web Server",
                    "port": 80,
                    "service": "http",
                    "discovered_by": "Nikto",
                    "exploit_status": "manual",
                    "solution": "Implement authentication for admin panel",
                    "references": ["https://cirt.net/Nikto2"],
                }
            ]
        }
        
        scan_result.status = ToolStatus.COMPLETE
        scan_result.completed_at = datetime.utcnow()
        scan_result.duration_seconds = (scan_result.completed_at - scan_result.started_at).total_seconds()
        scan_result.parsed_output = result
        scan_result.vulnerabilities_found = len(result['vulnerabilities'])
        self.db.commit()
        
        return result
    
    async def _run_nuclei(self) -> Dict[str, Any]:
        """Run Nuclei scan (mock implementation)."""
        scan_result = ScanResult(
            scan_id=self.scan.id,
            tool_name="Nuclei",
            status=ToolStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        self.db.add(scan_result)
        self.db.commit()
        
        await asyncio.sleep(1)
        
        result = {
            "success": True,
            "tool": "Nuclei",
            "target": self.scan.target,
            "vulnerabilities": [
                {
                    "title": "Missing Security Headers",
                    "description": "Critical security headers are missing: X-Frame-Options, Content-Security-Policy",
                    "severity": "low",
                    "cvss_score": 3.7,
                    "affected_component": "Web Server",
                    "discovered_by": "Nuclei",
                    "exploit_status": "manual",
                    "solution": "Add security headers to web server configuration",
                    "references": ["https://owasp.org/www-project-secure-headers/"],
                    "tags": ["misconfiguration", "security-headers"],
                }
            ]
        }
        
        scan_result.status = ToolStatus.COMPLETE
        scan_result.completed_at = datetime.utcnow()
        scan_result.duration_seconds = (scan_result.completed_at - scan_result.started_at).total_seconds()
        scan_result.parsed_output = result
        scan_result.vulnerabilities_found = len(result['vulnerabilities'])
        self.db.commit()
        
        return result
    
    def _save_results(self, result: Dict[str, Any]):
        """Save vulnerabilities to database."""
        if not result.get('success'):
            return
        
        vulnerabilities = result.get('vulnerabilities', [])
        
        for vuln_data in vulnerabilities:
            # Map severity string to enum
            severity_map = {
                'critical': SeverityLevel.CRITICAL,
                'high': SeverityLevel.HIGH,
                'medium': SeverityLevel.MEDIUM,
                'low': SeverityLevel.LOW,
                'info': SeverityLevel.INFO,
            }
            
            # Map exploit status
            exploit_map = {
                'available': ExploitStatus.AVAILABLE,
                'poc_available': ExploitStatus.POC_AVAILABLE,
                'manual': ExploitStatus.MANUAL,
                'not_available': ExploitStatus.NOT_AVAILABLE,
            }
            
            vulnerability = Vulnerability(
                scan_id=self.scan.id,
                cve_id=vuln_data.get('cve_id'),
                vulnerability_id=vuln_data.get('cve_id') or f"{vuln_data.get('discovered_by')}-{datetime.utcnow().timestamp()}",
                title=vuln_data.get('title', 'Unknown Vulnerability'),
                description=vuln_data.get('description', ''),
                severity=severity_map.get(vuln_data.get('severity', 'medium'), SeverityLevel.MEDIUM),
                cvss_score=vuln_data.get('cvss_score'),
                cvss_vector=vuln_data.get('cvss_vector'),
                affected_component=vuln_data.get('affected_component'),
                affected_version=vuln_data.get('affected_version'),
                port=vuln_data.get('port'),
                service=vuln_data.get('service'),
                discovered_by=vuln_data.get('discovered_by', 'Unknown'),
                exploit_status=exploit_map.get(vuln_data.get('exploit_status', 'not_available'), ExploitStatus.NOT_AVAILABLE),
                solution=vuln_data.get('solution'),
                references=vuln_data.get('references', []),
                tags=vuln_data.get('tags', []),
                evidence=vuln_data.get('evidence'),
            )
            
            self.db.add(vulnerability)
        
        self.db.commit()
