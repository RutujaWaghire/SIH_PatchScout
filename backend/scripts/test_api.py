"""
Backend Test Script - Verify All API Endpoints
"""
import sys
import time
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

def test_api():
    """Test backend API endpoints"""
    import requests
    from colorama import Fore, Style, init
    init(autoreset=True)
    
    API_BASE = "http://localhost:8000"
    
    print("=" * 70)
    print(f"{Fore.CYAN}🧪 PatchScout API Test Suite{Style.RESET_ALL}")
    print("=" * 70)
    
    tests_passed = 0
    tests_failed = 0
    
    def test_endpoint(method, endpoint, data=None, description=""):
        nonlocal tests_passed, tests_failed
        try:
            url = f"{API_BASE}{endpoint}"
            print(f"\n{Fore.YELLOW}Testing: {description or endpoint}{Style.RESET_ALL}")
            print(f"  → {method} {url}")
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            elif method == "PATCH":
                response = requests.patch(url, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, timeout=10)
            
            if response.status_code < 400:
                print(f"  {Fore.GREEN}✓ PASS{Style.RESET_ALL} - Status: {response.status_code}")
                tests_passed += 1
                return response.json() if response.content else None
            else:
                print(f"  {Fore.RED}✗ FAIL{Style.RESET_ALL} - Status: {response.status_code}")
                print(f"    Error: {response.text[:200]}")
                tests_failed += 1
                return None
        except requests.exceptions.ConnectionError:
            print(f"  {Fore.RED}✗ FAIL{Style.RESET_ALL} - Cannot connect to server")
            print(f"    Make sure backend is running: uvicorn app.main:app --reload")
            tests_failed += 1
            return None
        except Exception as e:
            print(f"  {Fore.RED}✗ FAIL{Style.RESET_ALL} - {str(e)}")
            tests_failed += 1
            return None
    
    # Test 1: Health Check
    print(f"\n{Fore.CYAN}📋 Category: Health Checks{Style.RESET_ALL}")
    test_endpoint("GET", "/health", description="Health check")
    test_endpoint("GET", "/api/health", description="API health check")
    
    # Test 2: Dashboard Stats
    print(f"\n{Fore.CYAN}📊 Category: Dashboard & Reports{Style.RESET_ALL}")
    stats = test_endpoint("GET", "/api/reports/dashboard/stats", description="Dashboard statistics")
    
    # Test 3: List Scans
    print(f"\n{Fore.CYAN}🔍 Category: Scans{Style.RESET_ALL}")
    scans = test_endpoint("GET", "/api/scans/?page=1&page_size=5", description="List scans")
    
    # Test 4: Create Scan
    scan_data = {
        "target": "scanme.nmap.org",
        "scan_config": {
            "selected_tools": ["Nmap"],
            "scan_type": "quick",
            "aggressiveness": "low",
            "port_range": "80,443",
            "include_nse": False,
            "compliance": []
        }
    }
    scan_response = test_endpoint("POST", "/api/scans/", data=scan_data, description="Create new scan")
    
    scan_id = None
    if scan_response and 'id' in scan_response:
        scan_id = scan_response['id']
        print(f"  {Fore.GREEN}Created scan ID: {scan_id}{Style.RESET_ALL}")
        
        # Test 5: Get Scan Details
        time.sleep(2)  # Wait for scan to start
        test_endpoint("GET", f"/api/scans/{scan_id}", description=f"Get scan {scan_id} details")
        
        # Test 6: Get Scan Vulnerabilities
        test_endpoint("GET", f"/api/scans/{scan_id}/vulnerabilities", description=f"Get scan {scan_id} vulnerabilities")
        
        # Test 7: Get Scan Results
        test_endpoint("GET", f"/api/scans/{scan_id}/results", description=f"Get scan {scan_id} results")
    
    # Test 8: List Vulnerabilities
    print(f"\n{Fore.CYAN}🐛 Category: Vulnerabilities{Style.RESET_ALL}")
    vulns = test_endpoint("GET", "/api/vulnerabilities/?page=1&page_size=10", description="List vulnerabilities")
    test_endpoint("GET", "/api/vulnerabilities/stats/summary", description="Vulnerability statistics")
    
    # Test 9: AI Chat
    print(f"\n{Fore.CYAN}🤖 Category: AI Assistant{Style.RESET_ALL}")
    chat_data = {
        "message": "What are my critical vulnerabilities?",
        "rag_mode": True
    }
    test_endpoint("POST", "/api/chat/", data=chat_data, description="Send chat message")
    
    # Test 10: Attack Paths
    if scan_id:
        print(f"\n{Fore.CYAN}🎯 Category: Attack Paths{Style.RESET_ALL}")
        test_endpoint("GET", f"/api/attack-paths/{scan_id}", description=f"Get attack paths for scan {scan_id}")
        test_endpoint("GET", f"/api/attack-paths/{scan_id}/graph", description=f"Get attack graph for scan {scan_id}")
    
    # Test 11: Reports
    if scan_id:
        print(f"\n{Fore.CYAN}📄 Category: Reports{Style.RESET_ALL}")
        test_endpoint("GET", f"/api/reports/{scan_id}/json", description=f"Generate JSON report for scan {scan_id}")
        test_endpoint("GET", f"/api/reports/{scan_id}/summary", description=f"Generate summary for scan {scan_id}")
    
    # Test 12: Cancel Scan
    if scan_id:
        print(f"\n{Fore.CYAN}🛑 Category: Scan Control{Style.RESET_ALL}")
        test_endpoint("POST", f"/api/scans/{scan_id}/cancel", description=f"Cancel scan {scan_id}")
    
    # Results
    print("\n" + "=" * 70)
    total = tests_passed + tests_failed
    pass_rate = (tests_passed / total * 100) if total > 0 else 0
    
    print(f"\n{Fore.CYAN}📊 Test Results:{Style.RESET_ALL}")
    print(f"  Total Tests: {total}")
    print(f"  {Fore.GREEN}Passed: {tests_passed}{Style.RESET_ALL}")
    print(f"  {Fore.RED}Failed: {tests_failed}{Style.RESET_ALL}")
    print(f"  Pass Rate: {pass_rate:.1f}%")
    
    if tests_failed == 0:
        print(f"\n{Fore.GREEN}🎉 ALL TESTS PASSED! Backend is fully functional!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}⚠️  Some tests failed. Check backend logs.{Style.RESET_ALL}")
    
    print("=" * 70)
    
    return tests_failed == 0

if __name__ == "__main__":
    try:
        import requests
        import colorama
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "colorama"])
        import requests
        import colorama
    
    success = test_api()
    sys.exit(0 if success else 1)
