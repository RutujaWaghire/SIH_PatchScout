import { useState, useRef, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  Bot, 
  Send, 
  User, 
  Brain, 
  Search, 
  FileText, 
  Shield,
  Lightbulb,
  ExternalLink,
  Loader2
} from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  timestamp: Date;
}

interface Source {
  title: string;
  type: 'CVE' | 'MITRE' | 'NVD' | 'ExploitDB' | 'OWASP';
  url: string;
  relevance: number;
}

interface RAGContext {
  vulnerabilities: any[];
  threatIntelligence: any;
  knowledgeBase: any[];
}

export const AIAssistant = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "🛡️ **PatchScout AI Assistant** ready to help!\n\nI have access to:\n• Current vulnerability scan data\n• CVE database & threat intelligence\n• MITRE ATT&CK framework\n• Real-time exploit information\n• Best practice remediation guides\n\nAsk me anything about your security posture, specific vulnerabilities, or remediation strategies!",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [ragMode, setRagMode] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Mock RAG context
  const ragContext: RAGContext = {
    vulnerabilities: [
      { id: "CVE-2024-1234", severity: "critical", cvss: 9.8, title: "Remote Code Execution in Apache HTTP Server" },
      { id: "CVE-2024-5678", severity: "high", cvss: 7.5, title: "SQL Injection in Authentication Module" },
      { id: "CVE-2024-9012", severity: "medium", cvss: 5.3, title: "Cross-Site Scripting in Search Function" }
    ],
    threatIntelligence: {
      activeCampaigns: ["APT29", "Lazarus Group"],
      exploitsAvailable: 7,
      riskScore: 8.5
    },
    knowledgeBase: [
      { topic: "Apache HTTP Server Security", category: "Server Hardening" },
      { topic: "SQL Injection Prevention", category: "Application Security" },
      { topic: "XSS Mitigation Strategies", category: "Web Security" }
    ]
  };

  const generateRAGResponse = (userInput: string) => {
    const input_lower = userInput.toLowerCase();
    
    // CVE-specific responses
    if (input_lower.includes('cve-2024-1234') || input_lower.includes('apache') || input_lower.includes('rce')) {
      return {
        content: `🚨 **Critical: CVE-2024-1234 Analysis**

**Vulnerability Details:**
• **CVSS Score:** 9.8 (Critical)
• **Attack Vector:** Network
• **Impact:** Complete system compromise possible
• **Affected:** Apache HTTP Server 2.4.49

**Attack Scenario:**
This RCE vulnerability allows remote attackers to execute arbitrary code by sending malicious HTTP requests. No authentication required.

**Immediate Actions:**
1. 🔧 **Patch immediately** to Apache 2.4.50+
2. 🛡️ **Deploy WAF rules** to block exploit attempts
3. 🔍 **Monitor logs** for suspicious requests
4. 🚫 **Consider temporary service isolation**

**Threat Intelligence:**
• Active exploitation detected in the wild
• Multiple exploit PoCs available
• APT groups using this vector

Would you like specific WAF rules or detailed patching instructions?`,
        sources: [
          { title: "CVE-2024-1234", type: "CVE" as const, url: "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-1234", relevance: 0.95 },
          { title: "Apache Security Advisory", type: "NVD" as const, url: "https://nvd.nist.gov/vuln/detail/CVE-2024-1234", relevance: 0.90 },
          { title: "ExploitDB Entry", type: "ExploitDB" as const, url: "https://www.exploit-db.com/exploits/12345", relevance: 0.85 }
        ]
      };
    }

    if (input_lower.includes('sql injection') || input_lower.includes('cve-2024-5678')) {
      return {
        content: `⚠️ **High Risk: SQL Injection Analysis**

**Vulnerability Assessment:**
• **CVSS Score:** 7.5 (High)
• **Location:** Authentication module
• **Impact:** Database compromise, data exfiltration

**Technical Details:**
The vulnerability exists in user input validation where SQL queries are constructed using string concatenation without proper sanitization.

**Remediation Strategy:**
1. 🔒 **Implement parameterized queries** immediately
2. 🧪 **Input validation** - whitelist approach
3. 🛡️ **Principle of least privilege** for DB accounts
4. 📊 **Database activity monitoring**

**Code Example:**
\`\`\`sql
-- VULNERABLE
SELECT * FROM users WHERE username = '${userInput}';

-- SECURE  
SELECT * FROM users WHERE username = ?;
\`\`\`

**OWASP Reference:** A03:2021 – Injection`,
        sources: [
          { title: "OWASP SQL Injection", type: "OWASP" as const, url: "https://owasp.org/www-community/attacks/SQL_Injection", relevance: 0.92 },
          { title: "CVE-2024-5678", type: "CVE" as const, url: "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-5678", relevance: 0.88 }
        ]
      };
    }

    if (input_lower.includes('attack path') || input_lower.includes('lateral movement')) {
      return {
        content: `🎯 **Attack Path Analysis**

**Critical Attack Chain Identified:**
Internet → Web Server (CVE-2024-1234) → Shell Access → Database Server

**Attack Steps:**
1. **Initial Access:** Exploit Apache RCE (CVE-2024-1234)
2. **Execution:** Gain shell access on web server
3. **Lateral Movement:** Access internal database server
4. **Impact:** Data exfiltration, privilege escalation

**MITRE ATT&CK Mapping:**
• **T1190** - Exploit Public-Facing Application
• **T1059** - Command and Scripting Interpreter  
• **T1021** - Remote Services
• **T1083** - File and Directory Discovery

**Priority Mitigations:**
1. 🚨 Patch Apache immediately (breaks the chain)
2. 🔐 Network segmentation between web/DB tiers
3. 📊 Deploy EDR on critical systems
4. 🛡️ Implement zero-trust architecture

**Risk Reduction:** Patching CVE-2024-1234 reduces attack path probability by 89%`,
        sources: [
          { title: "MITRE ATT&CK Framework", type: "MITRE" as const, url: "https://attack.mitre.org/techniques/T1190/", relevance: 0.93 }
        ]
      };
    }

    if (input_lower.includes('risk score') || input_lower.includes('threat intelligence')) {
      return {
        content: `📊 **Threat Intelligence Summary**

**Current Risk Assessment:**
• **Overall Risk Score:** 8.5/10 (High)
• **Active Threat Campaigns:** 3
• **Available Exploits:** 7
• **Known Threat Actors:** APT29, Lazarus Group

**Intelligence Insights:**
🔴 **APT29** actively targeting Apache RCE vulnerabilities
🟠 **Ransomware groups** exploiting SQL injection vectors
🟡 **Script kiddies** using automated XSS scanners

**Trending Threats (Last 7 days):**
• +45% Apache exploit attempts
• +23% SQL injection probes  
• +12% XSS payload variations

**Recommended Monitoring:**
• Network traffic to Apache servers
• Database query anomalies
• Authentication bypass attempts
• Privilege escalation indicators

**Threat Actor TTPs:**
• Initial access via web vulnerabilities
• Living-off-the-land techniques
• Data exfiltration via DNS tunneling

The combination of critical vulnerabilities with active threat actor interest creates an elevated risk environment.`,
        sources: [
          { title: "Threat Intelligence Feed", type: "NVD" as const, url: "https://nvd.nist.gov/vuln/search", relevance: 0.87 }
        ]
      };
    }

    // Default response with RAG context
    return {
      content: `🤖 I can help you with various security topics based on your current environment:

**Current Vulnerabilities in Your Environment:**
${ragContext.vulnerabilities.map(v => `• ${v.id} (${v.severity.toUpperCase()}) - ${v.title}`).join('\n')}

**Available Knowledge Areas:**
• Vulnerability analysis & prioritization
• Attack path modeling & threat hunting
• Remediation strategies & patch management  
• Compliance frameworks (NIST, ISO 27001)
• Incident response procedures
• Security architecture recommendations

**Threat Intelligence:**
• ${ragContext.threatIntelligence.activeCampaigns.length} active campaigns targeting your sector
• Risk score: ${ragContext.threatIntelligence.riskScore}/10

Try asking about specific CVEs, attack scenarios, or mitigation strategies!`,
      sources: [
        { title: "PatchScout Knowledge Base", type: "NVD" as const, url: "#", relevance: 0.75 }
      ]
    };
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { 
      role: "user", 
      content: input,
      timestamp: new Date()
    };
    setMessages((prev) => [...prev, userMessage]);
    const messageText = input;
    setInput("");
    setLoading(true);

    try {
      // Call real API
      const response = await api.sendChatMessage(messageText, ragMode);

      const assistantMessage: Message = {
        role: "assistant",
        content: response.response || response.message || "I received your message but couldn't generate a response.",
        sources: response.sources || [],
        timestamp: new Date()
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error("Chat API error:", error);
      
      // Fallback to local response if API fails
      const fallbackResponse = ragMode ? generateRAGResponse(messageText) : {
        content: "⚠️ **Connection Error**\n\nCouldn't connect to AI backend. Using offline mode.\n\n" + 
                 (error.message || "Please check if the backend server is running."),
        sources: []
      };

      const assistantMessage: Message = {
        role: "assistant",
        content: fallbackResponse.content,
        sources: fallbackResponse.sources,
        timestamp: new Date()
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const quickActions = [
    "Analyze CVE-2024-1234 attack vectors",
    "Show attack path visualization", 
    "Generate remediation plan",
    "Explain threat intelligence",
    "Risk assessment summary"
  ];

  return (
    <div className="h-[calc(100vh-8rem)] flex gap-6">
      {/* Main Chat Interface */}
      <div className="flex-1">
        <Card className="h-full flex flex-col glass-effect">
          <CardHeader className="border-b border-border">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg gradient-primary">
                  <Brain className="h-6 w-6 text-primary-foreground" />
                </div>
                <div>
                  <CardTitle className="text-2xl">AI Security Assistant</CardTitle>
                  <p className="text-sm text-muted-foreground">
                    RAG-powered vulnerability analysis & threat intelligence
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant={ragMode ? "default" : "secondary"}>
                  {ragMode ? "RAG Active" : "Basic Mode"}
                </Badge>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setRagMode(!ragMode)}
                >
                  <Search className="h-4 w-4 mr-2" />
                  Toggle RAG
                </Button>
              </div>
            </div>
          </CardHeader>

          <ScrollArea className="flex-1 p-6" ref={scrollRef}>
            <div className="space-y-6">
              {messages.map((message, index) => (
                <div key={index} className="space-y-3">
                  <div
                    className={`flex gap-3 ${
                      message.role === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    {message.role === "assistant" && (
                      <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                        <Brain className="h-5 w-5 text-primary-foreground" />
                      </div>
                    )}
                    <div
                      className={`max-w-[95%] p-4 rounded-lg ${
                        message.role === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-card border border-border"
                      }`}
                    >
                      <div className="prose prose-sm max-w-none dark:prose-invert whitespace-pre-wrap">
                        {message.content.split('\n').map((line, i) => (
                          <div key={i} className="leading-relaxed">{line || '\u00A0'}</div>
                        ))}
                      </div>
                      <div className="text-xs text-muted-foreground mt-3">
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                    {message.role === "user" && (
                      <div className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center flex-shrink-0">
                        <User className="h-5 w-5" />
                      </div>
                    )}
                  </div>

                  {/* Sources */}
                  {message.sources && message.sources.length > 0 && (
                    <div className="ml-11 space-y-2">
                      <Separator />
                      <div className="text-sm font-medium text-muted-foreground">Sources:</div>
                      <div className="grid grid-cols-1 gap-2">
                        {message.sources.map((source, i) => (
                          <div key={i} className="flex items-center gap-2 text-sm">
                            <Badge variant="outline" className="text-xs">
                              {source.type}
                            </Badge>
                            <a 
                              href={source.url} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-primary hover:underline flex items-center gap-1"
                            >
                              {source.title}
                              <ExternalLink className="h-3 w-3" />
                            </a>
                            <span className="text-xs text-muted-foreground">
                              ({Math.round(source.relevance * 100)}% match)
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
              
              {loading && (
                <div className="flex gap-3">
                  <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                    <Brain className="h-5 w-5 text-primary-foreground animate-pulse" />
                  </div>
                  <div className="bg-card border border-border rounded-lg p-4">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Search className="h-4 w-4 animate-spin" />
                      Analyzing threat intelligence and vulnerability data...
                    </div>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          <div className="p-6 border-t border-border">
            <div className="flex gap-3">
              <Input
                placeholder="Ask about vulnerabilities, attack paths, or security recommendations..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
                className="flex-1"
              />
              <Button
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="gradient-primary text-primary-foreground"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </Card>
      </div>

      {/* Quick Actions Sidebar */}
      <div className="w-72">
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <Lightbulb className="h-5 w-5" />
              Quick Actions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {quickActions.map((action, index) => (
              <Button
                key={index}
                variant="outline"
                className="w-full justify-start text-left h-auto p-3"
                onClick={() => setInput(action)}
              >
                <FileText className="h-4 w-4 mr-2 flex-shrink-0" />
                <span className="text-sm">{action}</span>
              </Button>
            ))}
          </CardContent>
        </Card>

        <Card className="glass-effect mt-4">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Active Context
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="text-sm">
              <div className="font-medium mb-2">Current Vulnerabilities:</div>
              {ragContext.vulnerabilities.map((vuln, i) => (
                <div key={i} className="flex items-center gap-2 mb-1">
                  <Badge variant={vuln.severity === 'critical' ? 'destructive' : 'outline'} className="text-xs">
                    {vuln.severity}
                  </Badge>
                  <span className="text-xs">{vuln.id}</span>
                </div>
              ))}
            </div>
            <Separator />
            <div className="text-sm">
              <div className="font-medium mb-2">Threat Intel:</div>
              <div className="text-xs text-muted-foreground">
                Risk Score: {ragContext.threatIntelligence.riskScore}/10
              </div>
              <div className="text-xs text-muted-foreground">
                Active Campaigns: {ragContext.threatIntelligence.activeCampaigns.length}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
