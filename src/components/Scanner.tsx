import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { 
  Play, 
  Loader2, 
  CheckCircle2, 
  AlertTriangle, 
  Settings,
  Network,
  Shield,
  Globe,
  Search,
  Zap,
  Clock,
  Database
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { api } from "@/lib/api";

const SCAN_TOOLS = [
  { 
    name: "Nmap", 
    description: "Network Discovery & Port Scanning", 
    status: "idle",
    type: "network",
    icon: Network,
    capabilities: ["Port Scanning", "Service Detection", "OS Fingerprinting", "NSE Scripts"],
    avgTime: "2-5 min"
  },
  { 
    name: "OpenVAS", 
    description: "Comprehensive Vulnerability Assessment", 
    status: "idle",
    type: "vulnerability",
    icon: Shield,
    capabilities: ["CVE Detection", "Compliance Checks", "Config Assessment", "Network Security"],
    avgTime: "10-20 min"
  },
  { 
    name: "Nessus", 
    description: "Professional Vulnerability Scanner", 
    status: "idle",
    type: "compliance",
    icon: Database,
    capabilities: ["Deep Vulnerability Analysis", "Compliance Auditing", "Malware Detection", "Asset Discovery"],
    avgTime: "15-30 min"
  },
  { 
    name: "Nikto", 
    description: "Web Server Security Scanner", 
    status: "idle",
    type: "web",
    icon: Globe,
    capabilities: ["Web Vulnerabilities", "CGI Scanning", "Server Misconfigurations", "Dangerous Files"],
    avgTime: "3-8 min"
  },
  { 
    name: "Nuclei", 
    description: "Fast Template-based Scanner", 
    status: "idle",
    type: "template",
    icon: Zap,
    capabilities: ["Template Engine", "Custom CVE Checks", "Subdomain Takeover", "Technology Detection"],
    avgTime: "1-3 min"
  },
];

interface ScannerProps {
  onScanComplete: (data: any) => void;
}

interface ScanConfig {
  selectedTools: string[];
  scanType: 'quick' | 'comprehensive' | 'stealth' | 'custom';
  aggressiveness: 'low' | 'medium' | 'high';
  portRange: string;
  excludePorts: string;
  includeNSE: boolean;
  compliance: string[];
}

export const Scanner = ({ onScanComplete }: ScannerProps) => {
  const [target, setTarget] = useState("");
  const [scanning, setScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [tools, setTools] = useState(SCAN_TOOLS);
  const [currentTool, setCurrentTool] = useState("");
  const [estimatedTime, setEstimatedTime] = useState(0);
  const [scanConfig, setScanConfig] = useState<ScanConfig>({
    selectedTools: SCAN_TOOLS.map(t => t.name),
    scanType: 'comprehensive',
    aggressiveness: 'medium',
    portRange: '1-65535',
    excludePorts: '',
    includeNSE: true,
    compliance: ['PCI DSS', 'NIST']
  });
  const { toast } = useToast();

  const validateTarget = (target: string) => {
    const urlRegex = /^https?:\/\/.+/;
    const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/;
    
    return urlRegex.test(target) || ipRegex.test(target) || domainRegex.test(target);
  };

  const calculateEstimatedTime = () => {
    const timeMapping = {
      'Nmap': 4,
      'OpenVAS': 15,
      'Nessus': 22,
      'Nikto': 5,
      'Nuclei': 2
    };
    
    const selectedTime = scanConfig.selectedTools.reduce((total, tool) => {
      return total + (timeMapping[tool as keyof typeof timeMapping] || 0);
    }, 0);

    const multiplier = scanConfig.scanType === 'quick' ? 0.5 : 
                     scanConfig.scanType === 'comprehensive' ? 1.2 : 1;
    
    return Math.round(selectedTime * multiplier);
  };

  const startScan = async () => {
    if (!target) {
      toast({
        title: "Target Required",
        description: "Please enter a target URL, IP address, or domain",
        variant: "destructive",
      });
      return;
    }

    if (!validateTarget(target)) {
      toast({
        title: "Invalid Target",
        description: "Please enter a valid URL, IP address, or domain name",
        variant: "destructive",
      });
      return;
    }

    if (scanConfig.selectedTools.length === 0) {
      toast({
        title: "No Tools Selected",
        description: "Please select at least one scanning tool",
        variant: "destructive",
      });
      return;
    }

    try {
      setScanning(true);
      setProgress(0);
      const selectedTools = tools.filter(t => scanConfig.selectedTools.includes(t.name));
      const totalTime = calculateEstimatedTime();
      setEstimatedTime(totalTime);

      // Reset tool status
      setTools(SCAN_TOOLS.map(tool => ({ ...tool, status: "idle" })));

      toast({
        title: "Scan Started",
        description: `Initiating scan on ${target} with ${selectedTools.length} tools`,
      });

      // Create scan via API
      console.log("Creating scan with target:", target);
      console.log("Scan config:", scanConfig);
      
      let scanResponse;
      try {
        scanResponse = await api.createScan({
          target,
          scan_config: {
            selected_tools: scanConfig.selectedTools,
            scan_type: scanConfig.scanType,
            aggressiveness: scanConfig.aggressiveness,
            port_range: scanConfig.portRange,
            exclude_ports: scanConfig.excludePorts,
            include_nse: scanConfig.includeNSE,
            compliance: scanConfig.compliance,
          },
        });
        console.log("Scan created successfully:", scanResponse);
      } catch (createError: any) {
        console.error("Failed to create scan:", createError);
        throw new Error(`Failed to create scan: ${createError.message || 'Unknown error'}`);
      }

      if (!scanResponse || !scanResponse.id) {
        throw new Error("Invalid scan response - missing scan ID");
      }

      const scanId = scanResponse.id;
      console.log("Monitoring scan ID:", scanId);
      
      // Poll for scan status
      let scanComplete = false;
      let pollCount = 0;
      const maxPolls = 60; // 5 minutes max (5 seconds interval)
      
      while (!scanComplete && pollCount < maxPolls) {
        await new Promise((resolve) => setTimeout(resolve, 5000)); // Poll every 5 seconds
        
        let scanStatus;
        try {
          scanStatus = await api.getScan(scanId);
          console.log("Scan status update:", scanStatus);
        } catch (statusError) {
          console.error("Failed to get scan status:", statusError);
          continue; // Try again next poll
        }

        // Safely update progress
        const progress = scanStatus?.progress ?? 0;
        const currentTool = scanStatus?.current_tool || null;
        
        setProgress(progress);
        if (currentTool) {
          setCurrentTool(currentTool);
        }
        
        // Update tool statuses based on scan progress
        if (currentTool) {
          setTools((prev) =>
            prev.map((t) => {
              if (t.name === currentTool) {
                return { ...t, status: "running" };
              }
              const toolIndex = selectedTools.findIndex(st => st.name === t.name);
              const currentIndex = selectedTools.findIndex(st => st.name === currentTool);
              if (toolIndex < currentIndex) {
                return { ...t, status: "complete" };
              }
              return t;
            })
          );
        }
        
        if (scanStatus?.status === "completed") {
          scanComplete = true;
          setProgress(100);
          
          // Fetch scan results
          let vulnerabilities = [];
          try {
            const vulnResponse = await api.getScanVulnerabilities(scanId);
            vulnerabilities = vulnResponse?.vulnerabilities || vulnResponse || [];
            console.log("Fetched vulnerabilities:", vulnerabilities);
          } catch (vulnError) {
            console.error("Failed to fetch vulnerabilities:", vulnError);
            // Continue anyway with empty vulnerabilities
          }
          
          // Safely extract summary data
          const summary = scanStatus?.summary || {};
          const totalVulnerabilities = scanStatus?.vulnerabilities_count ?? summary?.total_vulnerabilities ?? 0;
          const critical = scanStatus?.critical_count ?? summary?.critical ?? 0;
          const high = scanStatus?.high_count ?? summary?.high ?? 0;
          const medium = scanStatus?.medium_count ?? summary?.medium ?? 0;
          const low = scanStatus?.low_count ?? summary?.low ?? 0;
          const ports = scanStatus?.open_ports_count ?? summary?.open_ports ?? 0;
          const services = scanStatus?.services_detected ?? summary?.services ?? 0;
          
          // Format results for UI
          const results = {
            id: scanId,
            target,
            scanTime: scanStatus?.started_at || new Date().toISOString(),
            duration: scanStatus?.completed_at && scanStatus?.started_at
              ? `${Math.round((new Date(scanStatus.completed_at).getTime() - new Date(scanStatus.started_at).getTime()) / 60000)} minutes`
              : "Unknown",
            scanConfig,
            summary: {
              totalVulnerabilities,
              critical,
              high,
              medium,
              low,
              ports,
              services
            },
            vulnerabilities,
            networkFindings: {
              openPorts: scanStatus?.open_ports || [],
              osFingerprint: scanStatus?.os_fingerprint || "Unknown",
              uptime: scanStatus?.uptime || "Unknown"
            },
            complianceResults: scanStatus?.compliance_results || {}
          };
          
          console.log("Formatted scan results:", results);
          onScanComplete(results);
          
          toast({
            title: "Scan Complete!",
            description: `Found ${totalVulnerabilities} vulnerabilities`,
          });
        } else if (scanStatus?.status === "failed") {
          throw new Error(scanStatus?.error_message || "Scan failed");
        } else if (scanStatus?.status === "cancelled") {
          throw new Error("Scan was cancelled");
        }
        
        pollCount++;
      }
      
      if (pollCount >= maxPolls) {
        toast({
          title: "Scan Timeout",
          description: "Scan is taking longer than expected. Check the analyzer for partial results.",
          variant: "destructive",
        });
      }
      
      // Mark all tools as complete
      setTools((prev) =>
        prev.map((t) =>
          selectedTools.some(st => st.name === t.name) ? { ...t, status: "complete" } : t
        )
      );
      
    } catch (error: any) {
      console.error("Scan error:", error);
      toast({
        title: "Scan Failed",
        description: error.message || "Failed to complete scan. Check backend connection.",
        variant: "destructive",
      });
      
      // Reset tool statuses on error
      setTools(SCAN_TOOLS);
    } finally {
      setScanning(false);
      setCurrentTool("");
      
      // Reset after delay
      setTimeout(() => {
        setProgress(0);
      }, 3000);
    }
  };



  const toggleTool = (toolName: string) => {
    setScanConfig(prev => ({
      ...prev,
      selectedTools: prev.selectedTools.includes(toolName)
        ? prev.selectedTools.filter(t => t !== toolName)
        : [...prev.selectedTools, toolName]
    }));
  };

  return (
    <div className="space-y-6 relative">
      {/* Loading Overlay - Prevents black screen during initialization */}
      {scanning && progress === 0 && (
        <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center">
          <Card className="w-96 border-primary/50 shadow-2xl">
            <CardContent className="pt-6">
              <div className="text-center space-y-4">
                <div className="flex justify-center">
                  <Loader2 className="h-12 w-12 animate-spin text-primary" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold">Initializing Scan</h3>
                  <p className="text-sm text-muted-foreground mt-2">
                    Setting up security scan for {target}...
                  </p>
                  <p className="text-xs text-muted-foreground mt-2">
                    Please wait while we configure the scanning tools
                  </p>
                </div>
                <Progress value={0} className="h-2" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Target Configuration */}
      <Card className="glass-effect border-primary/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5" />
            Target Configuration
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-3">
            <Input
              placeholder="https://example.com, 192.168.1.1, or example.com"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              disabled={scanning}
              className="flex-1 bg-background/50 border-border"
            />
            <Button
              onClick={startScan}
              disabled={scanning || !target}
              className="gradient-primary text-primary-foreground min-w-32"
            >
              {scanning ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Scanning
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  Start Scan
                </>
              )}
            </Button>
          </div>

          {scanning && (
            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span>Scanning with {currentTool}...</span>
                <span>{Math.round(progress)}% Complete</span>
              </div>
              <Progress value={progress} className="h-2" />
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Clock className="h-4 w-4" />
                Estimated time remaining: {Math.round((100 - progress) / 100 * estimatedTime)} minutes
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Scan Configuration */}
      <Tabs defaultValue="tools" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="tools">Scanning Tools</TabsTrigger>
          <TabsTrigger value="settings">Scan Settings</TabsTrigger>
          <TabsTrigger value="advanced">Advanced Options</TabsTrigger>
        </TabsList>

        <TabsContent value="tools" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {tools.map((tool) => {
              const IconComponent = tool.icon;
              const isSelected = scanConfig.selectedTools.includes(tool.name);
              
              return (
                <Card
                  key={tool.name}
                  className={`cursor-pointer transition-all duration-300 ${
                    tool.status === "running"
                      ? "border-primary glow-primary"
                      : tool.status === "complete"
                      ? "border-success"
                      : isSelected
                      ? "border-primary/50 bg-primary/5"
                      : "border-border hover:border-primary/30"
                  }`}
                  onClick={() => !scanning && toggleTool(tool.name)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <div className={`p-2 rounded-lg ${isSelected ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
                          <IconComponent className="h-4 w-4" />
                        </div>
                        <div>
                          <h3 className="font-semibold flex items-center gap-2">
                            {tool.name}
                            {isSelected && <Checkbox checked disabled className="h-3 w-3" />}
                          </h3>
                          <p className="text-xs text-muted-foreground">{tool.avgTime}</p>
                        </div>
                      </div>
                      {tool.status === "running" && (
                        <Loader2 className="h-5 w-5 text-primary animate-spin" />
                      )}
                      {tool.status === "complete" && (
                        <CheckCircle2 className="h-5 w-5 text-success" />
                      )}
                    </div>
                    
                    <p className="text-sm text-muted-foreground mb-3">{tool.description}</p>
                    
                    <div className="space-y-2">
                      <div className="text-xs font-medium">Capabilities:</div>
                      <div className="flex flex-wrap gap-1">
                        {tool.capabilities.map((cap, i) => (
                          <span key={i} className="text-xs px-2 py-1 rounded bg-muted">
                            {cap}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    <div className="mt-3">
                      <span className={`text-xs px-2 py-1 rounded ${
                        tool.status === "idle"
                          ? isSelected ? "bg-primary/20 text-primary" : "bg-muted text-muted-foreground"
                          : tool.status === "running"
                          ? "bg-primary text-primary-foreground"
                          : "bg-success/20 text-success"
                      }`}>
                        {tool.status === "idle"
                          ? isSelected ? "Selected" : "Click to select"
                          : tool.status === "running"
                          ? "Scanning..."
                          : "Complete"}
                      </span>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        <TabsContent value="settings" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="glass-effect">
              <CardHeader>
                <CardTitle>Scan Profile</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Scan Type</label>
                  <Select value={scanConfig.scanType} onValueChange={(value: any) => setScanConfig(prev => ({ ...prev, scanType: value }))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="quick">Quick Scan (Fast, Basic)</SelectItem>
                      <SelectItem value="comprehensive">Comprehensive (Recommended)</SelectItem>
                      <SelectItem value="stealth">Stealth (Slow, Undetectable)</SelectItem>
                      <SelectItem value="custom">Custom Configuration</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-sm font-medium">Aggressiveness Level</label>
                  <Select value={scanConfig.aggressiveness} onValueChange={(value: any) => setScanConfig(prev => ({ ...prev, aggressiveness: value }))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low (Safe, Minimal Impact)</SelectItem>
                      <SelectItem value="medium">Medium (Balanced)</SelectItem>
                      <SelectItem value="high">High (Thorough, May Trigger IDS)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            <Card className="glass-effect">
              <CardHeader>
                <CardTitle>Network Configuration</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Port Range</label>
                  <Input
                    value={scanConfig.portRange}
                    onChange={(e) => setScanConfig(prev => ({ ...prev, portRange: e.target.value }))}
                    placeholder="1-65535, 80,443,8080"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Exclude Ports</label>
                  <Input
                    value={scanConfig.excludePorts}
                    onChange={(e) => setScanConfig(prev => ({ ...prev, excludePorts: e.target.value }))}
                    placeholder="21,25,135"
                  />
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="nse"
                    checked={scanConfig.includeNSE}
                    onCheckedChange={(checked) => setScanConfig(prev => ({ ...prev, includeNSE: !!checked }))}
                  />
                  <label htmlFor="nse" className="text-sm">Include Nmap NSE Scripts</label>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="advanced" className="space-y-4">
          <Card className="glass-effect">
            <CardHeader>
              <CardTitle>Compliance & Reporting</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Compliance Frameworks</label>
                <div className="grid grid-cols-2 gap-2">
                  {['PCI DSS', 'NIST', 'ISO 27001', 'HIPAA', 'SOX', 'GDPR'].map((framework) => (
                    <div key={framework} className="flex items-center space-x-2">
                      <Checkbox
                        id={framework}
                        checked={scanConfig.compliance.includes(framework)}
                        onCheckedChange={(checked) => {
                          setScanConfig(prev => ({
                            ...prev,
                            compliance: checked
                              ? [...prev.compliance, framework]
                              : prev.compliance.filter(c => c !== framework)
                          }));
                        }}
                      />
                      <label htmlFor={framework} className="text-sm">{framework}</label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t">
                <h4 className="text-sm font-medium mb-2">Estimated Scan Time</h4>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  <span>{calculateEstimatedTime()} minutes with current configuration</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};
