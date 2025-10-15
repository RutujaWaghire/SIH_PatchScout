"""
OpenVAS Scanner Integration (Real Implementation with GVM)
Uses python-gvm to connect to actual OpenVAS/GVM instances
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
import os

logger = logging.getLogger(__name__)

# Try to import GVM libraries
try:
    from gvm.connections import UnixSocketConnection, TLSConnection
    from gvm.protocols.gmp import Gmp
    from gvm.transforms import EtreeCheckCommandTransform
    GVM_AVAILABLE = True
except ImportError:
    GVM_AVAILABLE = False
    logger.warning("python-gvm not installed. OpenVAS will run in mock mode.")


class OpenVASScanner:
    """OpenVAS/GVM scanner implementation with fallback to mock"""
    
    def __init__(self):
        self.name = "OpenVAS"
        self.version = "22.4"
        self.gvm_host = os.getenv("GVM_HOST", "localhost")
        self.gvm_port = int(os.getenv("GVM_PORT", "9390"))
        self.gvm_username = os.getenv("GVM_USERNAME", "admin")
        self.gvm_password = os.getenv("GVM_PASSWORD", "admin")
        self.use_socket = os.getenv("GVM_USE_SOCKET", "false").lower() == "true"
        self.socket_path = os.getenv("GVM_SOCKET_PATH", "/var/run/gvmd.sock")
    
    async def scan(self, target: str, config: Dict) -> Dict:
        """
        Perform OpenVAS scan
        Falls back to mock if GVM not available or configured
        """
        if GVM_AVAILABLE and self._is_configured():
            try:
                return await self._real_scan(target, config)
            except Exception as e:
                logger.error(f"OpenVAS real scan failed: {e}. Falling back to mock.")
                return await self._mock_scan(target, config)
        else:
            logger.info("Using mock OpenVAS scan")
            return await self._mock_scan(target, config)
    
    def _is_configured(self) -> bool:
        """Check if OpenVAS is properly configured"""
        if self.use_socket:
            return os.path.exists(self.socket_path)
        return bool(self.gvm_host and self.gvm_username and self.gvm_password)
    
    async def _real_scan(self, target: str, config: Dict) -> Dict:
        """
        Real OpenVAS scan using python-gvm
        """
        logger.info(f"Starting real OpenVAS scan on {target}")
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_scan, target, config)
    
    def _sync_scan(self, target: str, config: Dict) -> Dict:
        """Synchronous GVM scan"""
        transform = EtreeCheckCommandTransform()
        
        # Connect to GVM
        if self.use_socket:
            connection = UnixSocketConnection(path=self.socket_path)
        else:
            connection = TLSConnection(hostname=self.gvm_host, port=self.gvm_port)
        
        vulnerabilities = []
        
        with Gmp(connection=connection, transform=transform) as gmp:
            # Authenticate
            gmp.authenticate(self.gvm_username, self.gvm_password)
            
            # Create target
            target_response = gmp.create_target(
                name=f"PatchScout-{target}-{datetime.utcnow().timestamp()}",
                hosts=[target]
            )
            target_id = target_response.get('id')
            
            # Get scan config (Full and fast by default)
            config_id = 'daba56c8-73ec-11df-a475-002264764cea'  # Full and fast
            
            # Create task
            task_response = gmp.create_task(
                name=f"PatchScout-Task-{datetime.utcnow().timestamp()}",
                config_id=config_id,
                target_id=target_id,
                scanner_id='08b69003-5fc2-4037-a479-93b440211c73'  # Default scanner
            )
            task_id = task_response.get('id')
            
            # Start scan
            gmp.start_task(task_id)
            
            # Poll for completion
            scan_complete = False
            max_polls = 120  # 10 minutes max
            poll_count = 0
            
            while not scan_complete and poll_count < max_polls:
                task_status = gmp.get_task(task_id)
                status = task_status.xpath('task/status/text()')[0]
                
                if status in ['Done', 'Stopped', 'Interrupted']:
                    scan_complete = True
                else:
                    poll_count += 1
                    import time
                    time.sleep(5)
            
            # Get results
            results = gmp.get_results(task_id=task_id)
            
            # Parse vulnerabilities
            for result in results.xpath('result'):
                severity = float(result.xpath('severity/text()')[0] or 0)
                if severity > 0:
                    vuln = {
                        "cve_id": result.xpath('nvt/@oid')[0] if result.xpath('nvt/@oid') else None,
                        "title": result.xpath('nvt/name/text()')[0] if result.xpath('nvt/name/text()') else "Unknown",
                        "severity": self._cvss_to_severity(severity),
                        "cvss_score": severity,
                        "description": result.xpath('description/text()')[0] if result.xpath('description/text()') else "",
                        "solution": result.xpath('nvt/solution/text()')[0] if result.xpath('nvt/solution/text()') else "",
                        "port": result.xpath('port/text()')[0] if result.xpath('port/text()') else "unknown",
                        "service": result.xpath('port/text()')[0].split('/')[1] if result.xpath('port/text()') and '/' in result.xpath('port/text()')[0] else "unknown"
                    }
                    vulnerabilities.append(vuln)
            
            # Cleanup
            gmp.delete_task(task_id, ultimate=True)
            gmp.delete_target(target_id, ultimate=True)
        
        logger.info(f"OpenVAS scan complete. Found {len(vulnerabilities)} vulnerabilities.")
        
        return {
            "tool": self.name,
            "version": self.version,
            "target": target,
            "scan_time": datetime.utcnow().isoformat(),
            "vulnerabilities": vulnerabilities,
            "scan_duration": f"{poll_count * 5} seconds",
            "hosts_scanned": 1,
            "mode": "real"
        }
    
    async def _mock_scan(self, target: str, config: Dict) -> Dict:
        """Mock scan for when OpenVAS is not available"""
        await asyncio.sleep(3)
        
        return {
            "tool": self.name,
            "version": self.version,
            "target": target,
            "scan_time": datetime.utcnow().isoformat(),
            "vulnerabilities": [
                {
                    "cve_id": "CVE-2024-SQL-001",
                    "title": "SQL Injection in Login Form",
                    "severity": "high",
                    "cvss_score": 8.1,
                    "description": "Unvalidated SQL query in authentication module",
                    "solution": "Implement parameterized queries",
                    "port": 3306,
                    "service": "mysql"
                },
                {
                    "cve_id": "CVE-2024-XSS-002",
                    "title": "Reflected XSS in Search",
                    "severity": "medium",
                    "cvss_score": 5.4,
                    "description": "User input not sanitized in search functionality",
                    "solution": "Implement input validation and output encoding",
                    "port": 80,
                    "service": "http"
                }
            ],
            "scan_duration": "3.2 seconds",
            "hosts_scanned": 1,
            "mode": "mock"
        }
    
    def _cvss_to_severity(self, cvss_score: float) -> str:
        """Convert CVSS score to severity level"""
        if cvss_score >= 9.0:
            return "critical"
        elif cvss_score >= 7.0:
            return "high"
        elif cvss_score >= 4.0:
            return "medium"
        elif cvss_score > 0:
            return "low"
        return "info"
