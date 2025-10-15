import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { AlertTriangle, Shield, TrendingUp, Network } from "lucide-react";

interface AnalyzerProps {
  scanData: any;
}

export const Analyzer = ({ scanData }: AnalyzerProps) => {
  if (!scanData) {
    return (
      <Card className="p-12 text-center glass-effect">
        <Shield className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-xl font-semibold mb-2">No Scan Data Available</h3>
        <p className="text-muted-foreground">
          Run a scan from the Scanner tab to view analysis
        </p>
      </Card>
    );
  }

  const severityCounts = {
    critical: scanData.vulnerabilities.filter((v: any) => v.severity === "critical").length,
    high: scanData.vulnerabilities.filter((v: any) => v.severity === "high").length,
    medium: scanData.vulnerabilities.filter((v: any) => v.severity === "medium").length,
    low: scanData.vulnerabilities.filter((v: any) => v.severity === "low").length,
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical":
        return "gradient-danger";
      case "high":
        return "bg-destructive";
      case "medium":
        return "bg-warning";
      case "low":
        return "bg-primary";
      default:
        return "bg-muted";
    }
  };

  const getSeverityBadgeVariant = (severity: string) => {
    switch (severity) {
      case "critical":
      case "high":
        return "destructive";
      case "medium":
        return "outline";
      default:
        return "secondary";
    }
  };

  return (
    <div className="space-y-6">
      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-6 border-destructive/50">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">Critical</span>
            <AlertTriangle className="h-5 w-5 text-destructive" />
          </div>
          <p className="text-3xl font-bold text-destructive">{severityCounts.critical}</p>
        </Card>
        <Card className="p-6 border-warning/50">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">High</span>
            <TrendingUp className="h-5 w-5 text-warning" />
          </div>
          <p className="text-3xl font-bold text-warning">{severityCounts.high}</p>
        </Card>
        <Card className="p-6 border-primary/50">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">Medium</span>
            <Network className="h-5 w-5 text-primary" />
          </div>
          <p className="text-3xl font-bold text-primary">{severityCounts.medium}</p>
        </Card>
        <Card className="p-6 border-success/50">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">Low</span>
            <Shield className="h-5 w-5 text-success" />
          </div>
          <p className="text-3xl font-bold text-success">{severityCounts.low}</p>
        </Card>
      </div>

      {/* Vulnerability Details */}
      <Card className="p-6 glass-effect">
        <h2 className="text-2xl font-bold mb-6">Vulnerability Analysis</h2>
        <div className="space-y-4">
          {scanData.vulnerabilities.map((vuln: any, index: number) => (
            <Card
              key={index}
              className={`p-5 border-l-4 transition-smooth hover:scale-[1.01] ${
                vuln.severity === "critical"
                  ? "border-l-destructive"
                  : vuln.severity === "high"
                  ? "border-l-warning"
                  : vuln.severity === "medium"
                  ? "border-l-primary"
                  : "border-l-success"
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <Badge variant={getSeverityBadgeVariant(vuln.severity)} className="uppercase">
                      {vuln.severity}
                    </Badge>
                    <code className="text-sm px-2 py-1 rounded bg-muted">{vuln.id}</code>
                    <span className="text-sm font-semibold">CVSS: {vuln.cvss}</span>
                  </div>
                  <h3 className="text-lg font-semibold mb-1">{vuln.title}</h3>
                  <p className="text-sm text-muted-foreground mb-2">{vuln.description}</p>
                  <p className="text-sm">
                    <span className="text-muted-foreground">Affected: </span>
                    <code className="text-xs bg-muted px-2 py-1 rounded">{vuln.affectedComponent}</code>
                  </p>
                </div>
              </div>
              <div className="mt-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-muted-foreground">Risk Score</span>
                  <span className="text-xs font-semibold">{vuln.cvss}/10</span>
                </div>
                <Progress value={(vuln.cvss / 10) * 100} className="h-2" />
              </div>
            </Card>
          ))}
        </div>
      </Card>

      {/* Attack Path Visualization */}
      <Card className="p-6 glass-effect">
        <h2 className="text-2xl font-bold mb-6">Potential Attack Paths</h2>
        <div className="space-y-4">
          <div className="p-4 rounded-lg border border-destructive/30 bg-destructive/5">
            <div className="flex items-center gap-2 mb-3">
              <div className="h-2 w-2 rounded-full bg-destructive animate-pulse" />
              <h4 className="font-semibold">High Risk Attack Chain Detected</h4>
            </div>
            <div className="space-y-2 ml-4">
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-full bg-destructive/20 flex items-center justify-center text-xs font-bold">
                  1
                </div>
                <div className="flex-1">
                  <p className="text-sm">Initial Access via CVE-2024-1234 (RCE)</p>
                  <p className="text-xs text-muted-foreground">Exploit web server vulnerability</p>
                </div>
              </div>
              <div className="ml-4 border-l-2 border-destructive/30 h-6" />
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-full bg-warning/20 flex items-center justify-center text-xs font-bold">
                  2
                </div>
                <div className="flex-1">
                  <p className="text-sm">Privilege Escalation via CVE-2024-5678 (SQL Injection)</p>
                  <p className="text-xs text-muted-foreground">Access authentication database</p>
                </div>
              </div>
              <div className="ml-4 border-l-2 border-warning/30 h-6" />
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center text-xs font-bold">
                  3
                </div>
                <div className="flex-1">
                  <p className="text-sm">Data Exfiltration</p>
                  <p className="text-xs text-muted-foreground">Extract sensitive information</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
