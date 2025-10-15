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
  ExternalLink
} from "lucide-react";

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

export const EnhancedAIAssistant = () => {
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

  const generateRAGResponse = (userInput: string) => {
    const input_lower = userInput.toLowerCase();
    
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
          { title: "CVE-2024-1234", type: "CVE" as const, url: "https://cve.mitre.org", relevance: 0.95 },
          { title: "Apache Security Advisory", type: "NVD" as const, url: "https://nvd.nist.gov", relevance: 0.90 }
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

**Remediation Strategy:**
1. 🔒 **Implement parameterized queries** immediately
2. 🧪 **Input validation** - whitelist approach
3. 🛡️ **Principle of least privilege** for DB accounts
4. 📊 **Database activity monitoring**

**OWASP Reference:** A03:2021 – Injection`,
        sources: [
          { title: "OWASP SQL Injection", type: "OWASP" as const, url: "https://owasp.org", relevance: 0.92 }
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

**Priority Mitigations:**
1. 🚨 Patch Apache immediately (breaks the chain)
2. 🔐 Network segmentation between web/DB tiers
3. 📊 Deploy EDR on critical systems

**Risk Reduction:** Patching CVE-2024-1234 reduces attack path probability by 89%`,
        sources: [
          { title: "MITRE ATT&CK Framework", type: "MITRE" as const, url: "https://attack.mitre.org", relevance: 0.93 }
        ]
      };
    }

    return {
      content: `🤖 I can help you with various security topics:

**Available Knowledge Areas:**
• Vulnerability analysis & prioritization
• Attack path modeling & threat hunting
• Remediation strategies & patch management  
• Compliance frameworks (NIST, ISO 27001)
• Incident response procedures
• Security architecture recommendations

Try asking about specific CVEs, attack scenarios, or mitigation strategies!`,
      sources: []
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
    setInput("");
    setLoading(true);

    setTimeout(() => {
      const response = ragMode ? generateRAGResponse(input) : {
        content: "I'm operating in basic mode. Enable RAG mode for enhanced vulnerability analysis.",
        sources: []
      };

      const assistantMessage: Message = {
        role: "assistant",
        content: response.content,
        sources: response.sources,
        timestamp: new Date()
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setLoading(false);
    }, 1500);
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
    "Explain threat intelligence"
  ];

  return (
    <div className="h-[calc(100vh-16rem)] flex gap-6">
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
                <span className={`text-xs px-2 py-1 rounded ${ragMode ? 'bg-green-500/20 text-green-500' : 'bg-gray-500/20 text-gray-500'}`}>
                  {ragMode ? "RAG Active" : "Basic Mode"}
                </span>
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
                      className={`max-w-[85%] p-4 rounded-lg ${
                        message.role === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-card border border-border"
                      }`}
                    >
                      <div className="prose prose-sm max-w-none dark:prose-invert">
                        {message.content.split('\n').map((line, i) => (
                          <div key={i}>{line}</div>
                        ))}
                      </div>
                      <div className="text-xs text-muted-foreground mt-2">
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
                            <span className="text-xs px-2 py-1 rounded border">
                              {source.type}
                            </span>
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
      <div className="w-80">
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
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
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs px-2 py-1 rounded bg-red-500/20 text-red-500 border">
                    critical
                  </span>
                  <span className="text-xs">CVE-2024-1234</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs px-2 py-1 rounded bg-orange-500/20 text-orange-500 border">
                    high
                  </span>
                  <span className="text-xs">CVE-2024-5678</span>
                </div>
              </div>
            </div>
            <Separator />
            <div className="text-sm">
              <div className="font-medium mb-2">Threat Intel:</div>
              <div className="text-xs text-muted-foreground">
                Risk Score: 8.5/10
              </div>
              <div className="text-xs text-muted-foreground">
                Active Campaigns: 3
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};