"""
Database Initialization Script for PatchScout
Creates all database tables and optionally seeds with sample data
"""
import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import engine, Base
from app.models import Scan, Vulnerability, ScanResult, CVEData
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

def init_db():
    """Initialize database tables"""
    print("🔧 Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def seed_sample_data():
    """Seed database with sample data for testing"""
    print("\n🌱 Seeding sample data...")
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_scans = db.query(Scan).count()
        if existing_scans > 0:
            print(f"⚠️  Database already contains {existing_scans} scans. Skipping seed.")
            return
        
        # Create sample scan
        sample_scan = Scan(
            target="scanme.nmap.org",
            status="completed",
            selected_tools=["Nmap"],
            scan_type="quick",
            aggressiveness="medium",
            port_range="1-1000",
            include_nse=True,
            compliance_frameworks=[],
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            progress=100,
            vulnerabilities_count=3,
            critical_count=1,
            high_count=1,
            medium_count=1,
            low_count=0,
            open_ports_count=3,
            services_detected=3,
            os_fingerprint="Linux 2.6.X|3.X",
        )
        db.add(sample_scan)
        db.commit()
        db.refresh(sample_scan)
        
        print(f"✅ Created sample scan (ID: {sample_scan.id})")
        
        # Create sample vulnerabilities
        vulnerabilities = [
            Vulnerability(
                scan_id=sample_scan.id,
                cve_id="CVE-2024-1234",
                title="Sample Remote Code Execution Vulnerability",
                description="This is a sample vulnerability for testing purposes",
                severity="critical",
                cvss_score=9.8,
                cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                affected_component="Sample Service",
                affected_version="1.0.0",
                port=80,
                service="http",
                protocol="tcp",
                exploit_available=True,
                exploit_maturity="functional",
                solution="Upgrade to version 1.0.1 or later",
                references=["https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-1234"],
                mitre_attack_ids=["T1190"],
                cwe_ids=["CWE-94"],
                tags=["rce", "critical", "network"],
            ),
            Vulnerability(
                scan_id=sample_scan.id,
                cve_id="CVE-2024-5678",
                title="Sample SQL Injection Vulnerability",
                description="SQL injection in authentication module",
                severity="high",
                cvss_score=7.5,
                cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
                affected_component="Database Module",
                affected_version="2.1.0",
                port=3306,
                service="mysql",
                protocol="tcp",
                exploit_available=True,
                exploit_maturity="proof-of-concept",
                solution="Implement parameterized queries",
                references=["https://owasp.org/www-community/attacks/SQL_Injection"],
                mitre_attack_ids=["T1190"],
                cwe_ids=["CWE-89"],
                tags=["sql injection", "database", "high"],
            ),
            Vulnerability(
                scan_id=sample_scan.id,
                cve_id="CVE-2024-9012",
                title="Sample Cross-Site Scripting (XSS) Vulnerability",
                description="Reflected XSS in search parameter",
                severity="medium",
                cvss_score=5.4,
                cvss_vector="CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N",
                affected_component="Web Application",
                affected_version="1.2.0",
                port=443,
                service="https",
                protocol="tcp",
                exploit_available=False,
                solution="Implement input sanitization and CSP headers",
                references=["https://owasp.org/www-community/attacks/xss/"],
                mitre_attack_ids=["T1189"],
                cwe_ids=["CWE-79"],
                tags=["xss", "web", "medium"],
            ),
        ]
        
        for vuln in vulnerabilities:
            db.add(vuln)
        
        db.commit()
        print(f"✅ Created {len(vulnerabilities)} sample vulnerabilities")
        
        # Create sample scan result
        scan_result = ScanResult(
            scan_id=sample_scan.id,
            tool_name="Nmap",
            tool_version="7.94",
            status="complete",
            command_executed="nmap -sV -T3 scanme.nmap.org",
            raw_output="Sample Nmap output...",
            parsed_output={
                "hosts": 1,
                "ports": 3,
                "services": ["http", "https", "ssh"]
            },
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            duration_seconds=45,
            exit_code=0,
            vulnerabilities_found=3,
        )
        db.add(scan_result)
        db.commit()
        
        print(f"✅ Created sample scan result")
        
        # Create sample CVE data
        cve_data = CVEData(
            cve_id="CVE-2024-1234",
            description="Sample CVE for testing",
            published_date=datetime.utcnow(),
            last_modified_date=datetime.utcnow(),
            cvss_v3_score=9.8,
            cvss_v3_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            cvss_v2_score=10.0,
            cvss_v2_vector="AV:N/AC:L/Au:N/C:C/I:C/A:C",
            severity="critical",
            cwe_ids=["CWE-94"],
            affected_vendors=["Sample Vendor"],
            affected_products=["Sample Product"],
            affected_versions=["1.0.0"],
            exploit_available=True,
            exploit_maturity="functional",
            exploit_references=["https://exploit-db.com/exploits/12345"],
            mitre_attack_techniques=["T1190"],
            mitre_attack_tactics=["TA0001"],
            threat_intel_trending=True,
            threat_intel_actively_exploited=True,
            epss_score=0.85,
            kev_listed=True,
            last_synced=datetime.utcnow(),
        )
        db.add(cve_data)
        db.commit()
        
        print(f"✅ Created sample CVE data")
        print(f"\n🎉 Sample data seeding complete!")
        print(f"   - Scan ID: {sample_scan.id}")
        print(f"   - Vulnerabilities: {len(vulnerabilities)}")
        print(f"   - Target: {sample_scan.target}")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function"""
    print("=" * 60)
    print("PatchScout Database Initialization")
    print("=" * 60)
    
    # Initialize database
    if not init_db():
        print("\n❌ Database initialization failed!")
        sys.exit(1)
    
    # Ask if user wants to seed sample data
    print("\n" + "=" * 60)
    response = input("Would you like to seed sample data? (y/n): ").strip().lower()
    
    if response == 'y':
        seed_sample_data()
    else:
        print("⏭️  Skipping sample data seeding")
    
    print("\n" + "=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Start the backend: uvicorn app.main:app --reload")
    print("   2. Start the frontend: npm run dev")
    print("   3. Visit http://localhost:8080")
    print("\n🔗 API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
