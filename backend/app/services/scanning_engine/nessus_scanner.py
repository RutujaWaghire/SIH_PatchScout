"""
Nessus Scanner Integration (Real Implementation with Tenable.io API)
Connects to Tenable.io or Nessus Professional
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
import os
import time

logger = logging.getLogger(__name__)

# Try to import Tenable SDK
try:
    from tenable.io import TenableIO
    from tenable.nessus import Nessus
    TENABLE_AVAILABLE = True
except ImportError:
    TENABLE_AVAILABLE = False
    logger.warning("tenable-io not installed. Nessus will run in mock mode.")


class NessusScanner:
    """Nessus scanner implementation with fallback to mock"""
    
    def __init__(self):
        self.name = "Nessus"
        self.version = "10.6"
        
        # Tenable.io credentials
        self.tenable_access_key = os.getenv("TENABLE_ACCESS_KEY")
        self.tenable_secret_key = os.getenv("TENABLE_SECRET_KEY")
        
        # Nessus Professional credentials
        self.nessus_url = os.getenv("NESSUS_URL", "https://localhost:8834")
        self.nessus_username = os.getenv("NESSUS_USERNAME")
        self.nessus_password = os.getenv("NESSUS_PASSWORD")
        self.nessus_access_key = os.getenv("NESSUS_ACCESS_KEY")
        self.nessus_secret_key = os.getenv("NESSUS_SECRET_KEY")
        
        self.use_tenable_io = os.getenv("USE_TENABLE_IO", "false").lower() == "true"
    
    async def scan(self, target: str, config: Dict) -> Dict:
        """
        Perform Nessus scan
        Falls back to mock if Tenable SDK not available or configured
        """
        if TENABLE_AVAILABLE and self._is_configured():
            try:
                if self.use_tenable_io:
                    return await self._tenable_io_scan(target, config)
                else:
                    return await self._nessus_professional_scan(target, config)
            except Exception as e:
                logger.error(f"Nessus real scan failed: {e}. Falling back to mock.")
                return await self._mock_scan(target, config)
        else:
            logger.info("Using mock Nessus scan")
            return await self._mock_scan(target, config)
    
    def _is_configured(self) -> bool:
        """Check if Nessus is properly configured"""
        if self.use_tenable_io:
            return bool(self.tenable_access_key and self.tenable_secret_key)
        else:
            return bool(self.nessus_url and (
                (self.nessus_username and self.nessus_password) or
                (self.nessus_access_key and self.nessus_secret_key)
            ))
    
    async def _tenable_io_scan(self, target: str, config: Dict) -> Dict:
        """Scan using Tenable.io cloud platform"""
        logger.info(f"Starting Tenable.io scan on {target}")
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_tenable_io_scan, target, config)
    
    def _sync_tenable_io_scan(self, target: str, config: Dict) -> Dict:
        """Synchronous Tenable.io scan"""
        tio = TenableIO(
            access_key=self.tenable_access_key,
            secret_key=self.tenable_secret_key
        )
        
        # Create scan
        scan = tio.scans.create(
            name=f"PatchScout-{target}-{datetime.utcnow().timestamp()}",
            targets=[target],
            template='basic'  # basic, advanced, discovery, etc.
        )
        
        # Launch scan
        tio.scans.launch(scan['id'])
        
        # Poll for completion
        scan_complete = False
        max_polls = 240  # 20 minutes max
        poll_count = 0
        
        while not scan_complete and poll_count < max_polls:
            scan_status = tio.scans.details(scan['id'])
            status = scan_status['info']['status']
            
            if status in ['completed', 'canceled', 'aborted']:
                scan_complete = True
            else:
                poll_count += 1
                time.sleep(5)
        
        # Get results
        vulnerabilities = []
        if scan_complete:
            results = tio.scans.results(scan['id'])
            
            for vuln in results.get('vulnerabilities', []):
                vulnerabilities.append({
                    "cve_id": vuln.get('plugin_name', 'N/A'),
                    "title": vuln.get('plugin_family', 'Unknown'),
                    "severity": self._severity_to_text(vuln.get('severity', 0)),
                    "cvss_score": vuln.get('cvss_base_score', 0),
                    "description": vuln.get('synopsis', ''),
                    "solution": vuln.get('solution', ''),
                    "port": vuln.get('port', 'unknown'),
                    "service": vuln.get('protocol', 'unknown'),
                    "plugin_id": vuln.get('plugin_id')
                })
        
        # Delete scan (cleanup)
        tio.scans.delete(scan['id'])
        
        logger.info(f"Tenable.io scan complete. Found {len(vulnerabilities)} vulnerabilities.")
        
        return {
            "tool": self.name,
            "version": self.version,
            "target": target,
            "scan_time": datetime.utcnow().isoformat(),
            "vulnerabilities": vulnerabilities,
            "scan_duration": f"{poll_count * 5} seconds",
            "hosts_scanned": 1,
            "mode": "tenable.io"
        }
    
    async def _nessus_professional_scan(self, target: str, config: Dict) -> Dict:
        """Scan using Nessus Professional"""
        logger.info(f"Starting Nessus Professional scan on {target}")
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_nessus_professional_scan, target, config)
    
    def _sync_nessus_professional_scan(self, target: str, config: Dict) -> Dict:
        """Synchronous Nessus Professional scan"""
        # Connect to Nessus
        if self.nessus_access_key and self.nessus_secret_key:
            nessus = Nessus(
                self.nessus_url,
                access_key=self.nessus_access_key,
                secret_key=self.nessus_secret_key,
                ssl_verify=False
            )
        else:
            nessus = Nessus(
                self.nessus_url,
                username=self.nessus_username,
                password=self.nessus_password,
                ssl_verify=False
            )
        
        # Get policies
        policies = nessus.policies.list()
        policy_id = policies['policies'][0]['id'] if policies['policies'] else None
        
        if not policy_id:
            raise Exception("No Nessus policy available")
        
        # Create scan
        scan = nessus.scans.create(
            name=f"PatchScout-{target}-{datetime.utcnow().timestamp()}",
            targets=[target],
            policy_id=policy_id
        )
        
        # Launch scan
        nessus.scans.launch(scan['id'])
        
        # Poll for completion
        scan_complete = False
        max_polls = 240
        poll_count = 0
        
        while not scan_complete and poll_count < max_polls:
            scan_status = nessus.scans.details(scan['id'])
            status = scan_status['info']['status']
            
            if status in ['completed', 'canceled', 'aborted']:
                scan_complete = True
            else:
                poll_count += 1
                time.sleep(5)
        
        # Get results
        vulnerabilities = []
        if scan_complete:
            results = nessus.scans.details(scan['id'])
            
            for vuln in results.get('vulnerabilities', []):
                vulnerabilities.append({
                    "cve_id": vuln.get('plugin_name', 'N/A'),
                    "title": vuln.get('plugin_family', 'Unknown'),
                    "severity": self._severity_to_text(vuln.get('severity', 0)),
                    "cvss_score": vuln.get('cvss_base_score', 0),
                    "description": vuln.get('synopsis', ''),
                    "solution": vuln.get('solution', ''),
                    "port": vuln.get('port', 'unknown'),
                    "service": vuln.get('protocol', 'unknown'),
                    "plugin_id": vuln.get('plugin_id')
                })
        
        # Delete scan
        nessus.scans.delete(scan['id'])
        
        logger.info(f"Nessus Professional scan complete. Found {len(vulnerabilities)} vulnerabilities.")
        
        return {
            "tool": self.name,
            "version": self.version,
            "target": target,
            "scan_time": datetime.utcnow().isoformat(),
            "vulnerabilities": vulnerabilities,
            "scan_duration": f"{poll_count * 5} seconds",
            "hosts_scanned": 1,
            "mode": "nessus-professional"
        }
    
    async def _mock_scan(self, target: str, config: Dict) -> Dict:
        """Mock scan for when Nessus is not available"""
        await asyncio.sleep(5)
        
        return {
            "tool": self.name,
            "version": self.version,
            "target": target,
            "scan_time": datetime.utcnow().isoformat(),
            "vulnerabilities": [
                {
                    "cve_id": "CVE-2024-SSL-001",
                    "title": "SSL/TLS Weak Cipher Suites",
                    "severity": "medium",
                    "cvss_score": 5.3,
                    "description": "Server supports weak SSL/TLS cipher suites",
                    "solution": "Disable weak ciphers and use TLS 1.2+",
                    "port": 443,
                    "service": "https"
                },
                {
                    "cve_id": "CVE-2024-AUTH-002",
                    "title": "Missing Security Headers",
                    "severity": "low",
                    "cvss_score": 3.7,
                    "description": "HTTP security headers not configured",
                    "solution": "Implement HSTS, CSP, X-Frame-Options headers",
                    "port": 80,
                    "service": "http"
                }
            ],
            "scan_duration": "5.0 seconds",
            "hosts_scanned": 1,
            "mode": "mock"
        }
    
    def _severity_to_text(self, severity: int) -> str:
        """Convert Nessus severity number to text"""
        severity_map = {
            0: "info",
            1: "low",
            2: "medium",
            3: "high",
            4: "critical"
        }
        return severity_map.get(severity, "info")
