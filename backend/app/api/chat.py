"""
AI Chat assistant API endpoints with RAG support.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import (
    ChatRequestSchema,
    ChatResponseSchema,
    ChatHistorySchema,
    ChatSource
)
from app.models import Vulnerability, CVEData, Scan

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponseSchema)
async def chat(request: ChatRequestSchema, db: Session = Depends(get_db)):
    """
    AI chat assistant with RAG (Retrieval-Augmented Generation) support.
    """
    from datetime import datetime
    
    message = request.message.lower()
    sources = []
    
    # Simple keyword-based response system (placeholder for real AI)
    if "cve" in message or "vulnerability" in message:
        # Search for relevant vulnerabilities
        vulns = db.query(Vulnerability).filter(
            Vulnerability.title.ilike(f"%{message}%")
        ).limit(5).all()
        
        if vulns:
            response = f"I found {len(vulns)} vulnerabilities related to your query:\n\n"
            for v in vulns:
                response += f"• **{v.title}** ({v.severity.value.upper()})\n"
                response += f"  CVE: {v.cve_id or 'N/A'} | CVSS: {v.cvss_score or 'N/A'}\n"
                response += f"  {v.description[:100]}...\n\n"
                
                sources.append(ChatSource(
                    type="CVE" if v.cve_id else "Vulnerability",
                    title=v.title,
                    url=f"http://localhost:8000/api/vulnerabilities/{v.id}",
                    relevance=0.85
                ))
        else:
            response = "I couldn't find specific vulnerabilities matching your query. Could you provide more details?"
    
    elif "scan" in message or "target" in message:
        scans = db.query(Scan).order_by(Scan.created_at.desc()).limit(3).all()
        if scans:
            response = f"Here are your recent scans:\n\n"
            for s in scans:
                response += f"• **{s.target}** - {s.status.value}\n"
                response += f"  Found {s.total_vulnerabilities} vulnerabilities\n"
                response += f"  Critical: {s.critical_count}, High: {s.high_count}\n\n"
                
                sources.append(ChatSource(
                    type="Scan",
                    title=f"Scan: {s.target}",
                    url=f"http://localhost:8000/api/scans/{s.id}",
                    relevance=0.9
                ))
        else:
            response = "You don't have any scans yet. Would you like to start a new scan?"
    
    elif "sql injection" in message or "sqli" in message:
        response = """**SQL Injection** is one of the most critical web vulnerabilities (OWASP Top 10 #3).

**What it is:**
Attackers inject malicious SQL code into input fields to manipulate database queries.

**Risk:**
- Unauthorized data access
- Data modification/deletion
- Complete database compromise
- Authentication bypass

**Prevention:**
1. Use parameterized queries (prepared statements)
2. Input validation and sanitization
3. Least privilege database accounts
4. Web Application Firewall (WAF)
5. Regular security testing

**Example Attack:**
```sql
' OR '1'='1' --
```

Would you like me to scan your application for SQL injection vulnerabilities?"""
        
        sources.append(ChatSource(
            type="OWASP",
            title="SQL Injection Prevention Cheat Sheet",
            url="https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html",
            relevance=0.95
        ))
    
    elif "xss" in message or "cross-site scripting" in message:
        response = """**Cross-Site Scripting (XSS)** allows attackers to inject malicious scripts into web pages.

**Types:**
1. **Reflected XSS**: Malicious script in URL/input
2. **Stored XSS**: Script stored in database
3. **DOM-based XSS**: Client-side code vulnerability

**Impact:**
- Session hijacking
- Credential theft
- Defacement
- Malware distribution

**Prevention:**
1. Output encoding/escaping
2. Content Security Policy (CSP)
3. HTTPOnly cookies
4. Input validation
5. Use modern frameworks with XSS protection"""
        
        sources.append(ChatSource(
            type="OWASP",
            title="XSS Prevention Cheat Sheet",
            url="https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html",
            relevance=0.95
        ))
    
    elif "nmap" in message or "port scan" in message:
        response = """**Nmap** (Network Mapper) is a powerful network scanning tool.

**Key Features:**
- Port scanning
- Service version detection
- OS fingerprinting
- NSE (Nmap Scripting Engine)
- Vulnerability detection

**Common Scan Types:**
- `-sV`: Service version detection
- `-sC`: Default scripts
- `-O`: OS detection
- `-p-`: All ports
- `--script vuln`: Vulnerability scanning

**Usage in PatchScout:**
We use python-nmap to perform comprehensive network scans and identify:
- Open ports and services
- Vulnerable service versions
- Misconfigurations
- Known CVEs

Would you like to run a scan?"""
        
        sources.append(ChatSource(
            type="Documentation",
            title="Nmap Reference Guide",
            url="https://nmap.org/book/man.html",
            relevance=0.9
        ))
    
    elif "remediation" in message or "fix" in message or "patch" in message:
        # Get recent critical vulnerabilities
        critical_vulns = db.query(Vulnerability).filter(
            Vulnerability.severity == "critical"
        ).limit(3).all()
        
        if critical_vulns:
            response = "**Priority Remediation Steps:**\n\n"
            for i, v in enumerate(critical_vulns, 1):
                response += f"{i}. **{v.title}**\n"
                response += f"   Solution: {v.solution or 'Apply vendor patches immediately'}\n"
                response += f"   Component: {v.affected_component}\n\n"
        else:
            response = "No critical vulnerabilities found. Great job! Keep monitoring for new threats."
    
    elif "risk" in message or "score" in message:
        total_vulns = db.query(Vulnerability).count()
        critical = db.query(Vulnerability).filter(Vulnerability.severity == "critical").count()
        high = db.query(Vulnerability).filter(Vulnerability.severity == "high").count()
        
        risk_score = (critical * 10 + high * 7) / max(total_vulns, 1)
        
        response = f"""**Current Risk Assessment:**

Total Vulnerabilities: {total_vulns}
Critical: {critical}
High: {high}
Risk Score: {risk_score:.1f}/10

**Risk Level:** {"🔴 CRITICAL" if risk_score > 7 else "🟡 MEDIUM" if risk_score > 4 else "🟢 LOW"}

**Recommendations:**
1. Prioritize critical vulnerabilities
2. Apply security patches
3. Conduct regular scans
4. Implement security monitoring"""
    
    else:
        response = """I'm your AI security assistant. I can help you with:

• **Vulnerability Analysis** - Ask about CVEs, exploits, or specific vulnerabilities
• **Scan Management** - Check scan status, results, and history
• **Security Guidance** - Learn about SQL injection, XSS, and other attacks
• **Risk Assessment** - Get risk scores and remediation priorities
• **Tool Information** - Learn about Nmap, OpenVAS, and scanning techniques

Try asking:
- "Show me critical vulnerabilities"
- "What is SQL injection?"
- "How do I fix CVE-2024-1234?"
- "What's my current risk score?"
- "Tell me about my recent scans"

What would you like to know?"""
    
    return ChatResponseSchema(
        message=response,
        sources=sources,
        rag_context_used=request.rag_mode and len(sources) > 0,
        timestamp=datetime.utcnow()
    )


@router.get("/history/{scan_id}", response_model=ChatHistorySchema)
def get_chat_history(scan_id: int, db: Session = Depends(get_db)):
    """
    Get chat history for a specific scan context.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # In a real implementation, store and retrieve chat history
    return ChatHistorySchema(
        messages=[],
        scan_id=scan_id
    )
