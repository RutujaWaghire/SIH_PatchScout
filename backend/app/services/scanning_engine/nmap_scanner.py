"""
Real Nmap scanner implementation using python-nmap.
"""
import nmap
import asyncio
from typing import Dict, List, Any
from datetime import datetime


class NmapScanner:
    """Wrapper for Nmap network scanner."""
    
    def __init__(self, target: str, port_range: str = "1-1000", aggressiveness: str = "medium"):
        self.target = target
        self.port_range = port_range
        self.aggressiveness = aggressiveness
        self.nm = nmap.PortScanner()
        
    async def scan(self) -> Dict[str, Any]:
        """
        Execute Nmap scan asynchronously.
        
        Returns:
            Dictionary containing scan results with ports, services, and vulnerabilities.
        """
        # Determine scan arguments based on aggressiveness
        scan_args = self._get_scan_args()
        
        try:
            # Run scan in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.nm.scan(self.target, self.port_range, arguments=scan_args)
            )
            
            # Parse results
            results = self._parse_results()
            return results
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "vulnerabilities": [],
                "ports": [],
            }
    
    def _get_scan_args(self) -> str:
        """Generate Nmap arguments based on aggressiveness level."""
        if self.aggressiveness == "low":
            # Polite scan: slower, less aggressive
            return "-sV -T2 --max-retries 1"
        elif self.aggressiveness == "high":
            # Aggressive scan: fast, thorough
            return "-sV -sC -O -T4 --script vuln"
        else:
            # Medium (default): balanced
            return "-sV -sC -T3"
    
    def _parse_results(self) -> Dict[str, Any]:
        """Parse Nmap scan results into structured format."""
        vulnerabilities = []
        ports = []
        services = []
        
        for host in self.nm.all_hosts():
            host_data = self.nm[host]
            
            # Parse port information
            for proto in host_data.all_protocols():
                port_list = host_data[proto].keys()
                
                for port in port_list:
                    port_info = host_data[proto][port]
                    service_name = port_info.get('name', 'unknown')
                    service_version = port_info.get('version', '')
                    state = port_info.get('state', 'unknown')
                    
                    if state == 'open':
                        ports.append({
                            "port": port,
                            "protocol": proto,
                            "state": state,
                            "service": service_name,
                            "version": service_version,
                        })
                        
                        services.append(service_name)
                        
                        # Check for known vulnerable services
                        vuln = self._check_service_vulnerability(
                            port, service_name, service_version
                        )
                        if vuln:
                            vulnerabilities.append(vuln)
            
            # Check for NSE script results (vulnerability scripts)
            if 'hostscript' in host_data:
                for script in host_data['hostscript']:
                    script_vuln = self._parse_nse_script(script, host)
                    if script_vuln:
                        vulnerabilities.append(script_vuln)
        
        return {
            "success": True,
            "tool": "Nmap",
            "target": self.target,
            "scan_time": datetime.utcnow().isoformat(),
            "ports_found": len(ports),
            "services_found": len(set(services)),
            "vulnerabilities": vulnerabilities,
            "ports": ports,
            "os_fingerprint": self._get_os_fingerprint(),
        }
    
    def _check_service_vulnerability(self, port: int, service: str, version: str) -> Dict[str, Any]:
        """Check if service/version has known vulnerabilities."""
        # Common vulnerable services database
        vulnerable_services = {
            "vsftpd 2.3.4": {
                "cve": "CVE-2011-2523",
                "severity": "critical",
                "cvss": 10.0,
                "title": "vsFTPd 2.3.4 Backdoor Command Execution",
                "description": "vsFTPd version 2.3.4 contains a backdoor which allows remote code execution",
            },
            "ProFTPD 1.3.3c": {
                "cve": "CVE-2010-4221",
                "severity": "critical",
                "cvss": 10.0,
                "title": "ProFTPD 1.3.3c Backdoor Command Execution",
                "description": "ProFTPD 1.3.3c contains a backdoor allowing remote code execution",
            },
            "Apache 2.4.49": {
                "cve": "CVE-2021-41773",
                "severity": "critical",
                "cvss": 9.8,
                "title": "Apache HTTP Server 2.4.49 Path Traversal",
                "description": "Path traversal and remote code execution vulnerability in Apache 2.4.49",
            },
        }
        
        # Check if this service/version is known to be vulnerable
        service_key = f"{service} {version}".strip()
        if service_key in vulnerable_services:
            vuln_data = vulnerable_services[service_key]
            return {
                "cve_id": vuln_data["cve"],
                "title": vuln_data["title"],
                "description": vuln_data["description"],
                "severity": vuln_data["severity"],
                "cvss_score": vuln_data["cvss"],
                "affected_component": f"{service} {version}",
                "port": port,
                "service": service,
                "discovered_by": "Nmap",
                "exploit_status": "available",
                "solution": f"Upgrade {service} to latest secure version",
                "references": [f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={vuln_data['cve']}"],
            }
        
        # Check for outdated SSH
        if service == "ssh" and version:
            try:
                # Extract version number
                if "OpenSSH" in version:
                    version_num = float(version.split()[1].split('p')[0])
                    if version_num < 7.4:
                        return {
                            "cve_id": "CVE-2018-15473",
                            "title": "OpenSSH User Enumeration Vulnerability",
                            "description": f"OpenSSH {version} is vulnerable to user enumeration",
                            "severity": "medium",
                            "cvss_score": 5.3,
                            "affected_component": version,
                            "port": port,
                            "service": service,
                            "discovered_by": "Nmap",
                            "exploit_status": "poc_available",
                            "solution": "Upgrade OpenSSH to version 7.8 or later",
                            "references": ["https://www.cve.org/CVERecord?id=CVE-2018-15473"],
                        }
            except:
                pass
        
        return None
    
    def _parse_nse_script(self, script: Dict, host: str) -> Dict[str, Any]:
        """Parse NSE (Nmap Scripting Engine) vulnerability script results."""
        script_id = script.get('id', '')
        output = script.get('output', '')
        
        # Check if it's a vulnerability script
        if 'vuln' in script_id or 'CVE' in output:
            return {
                "title": f"Vulnerability detected by {script_id}",
                "description": output,
                "severity": "medium",
                "cvss_score": 5.0,
                "affected_component": host,
                "discovered_by": f"Nmap NSE ({script_id})",
                "exploit_status": "manual",
                "solution": "Review NSE script output and apply appropriate patches",
            }
        
        return None
    
    def _get_os_fingerprint(self) -> str:
        """Extract OS fingerprint from Nmap results."""
        for host in self.nm.all_hosts():
            if 'osmatch' in self.nm[host]:
                matches = self.nm[host]['osmatch']
                if matches:
                    return matches[0].get('name', 'Unknown')
        return "Unknown"
