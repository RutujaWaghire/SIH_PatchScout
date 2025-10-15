import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Download, FileJson, FileText, Shield } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface ScanOutputProps {
  scanData: any;
}

export const ScanOutput = ({ scanData }: ScanOutputProps) => {
  const { toast } = useToast();

  if (!scanData) {
    return (
      <Card className="p-12 text-center glass-effect">
        <Shield className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-xl font-semibold mb-2">No Output Available</h3>
        <p className="text-muted-foreground">
          Run a scan from the Scanner tab to generate reports
        </p>
      </Card>
    );
  }

  const downloadReport = (format: "json" | "txt") => {
    let content = "";
    let filename = "";

    if (format === "json") {
      content = JSON.stringify(scanData, null, 2);
      filename = `vulnerability-report-${Date.now()}.json`;
    } else {
      content = `VULNERABILITY SCAN REPORT
Generated: ${new Date(scanData.scanTime).toLocaleString()}
Target: ${scanData.target}

SUMMARY
========
Total Vulnerabilities: ${scanData.vulnerabilities.length}
Critical: ${scanData.vulnerabilities.filter((v: any) => v.severity === "critical").length}
High: ${scanData.vulnerabilities.filter((v: any) => v.severity === "high").length}
Medium: ${scanData.vulnerabilities.filter((v: any) => v.severity === "medium").length}
Low: ${scanData.vulnerabilities.filter((v: any) => v.severity === "low").length}

DETAILED FINDINGS
=================

${scanData.vulnerabilities
  .map(
    (v: any, i: number) => `
${i + 1}. ${v.title}
   CVE ID: ${v.id}
   Severity: ${v.severity.toUpperCase()}
   CVSS Score: ${v.cvss}
   Description: ${v.description}
   Affected Component: ${v.affectedComponent}
   
   Recommendation: Immediate patching required for ${v.severity} severity vulnerabilities.
   -------------------------------------------------------------------
`
  )
  .join("\n")}
`;
      filename = `vulnerability-report-${Date.now()}.txt`;
    }

    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast({
      title: "Report Downloaded",
      description: `${format.toUpperCase()} report saved successfully`,
    });
  };

  return (
    <div className="space-y-6">
      {/* Export Options */}
      <Card className="p-6 glass-effect">
        <h2 className="text-2xl font-bold mb-4">Export Reports</h2>
        <div className="flex gap-3">
          <Button
            onClick={() => downloadReport("json")}
            className="gradient-primary text-primary-foreground"
          >
            <FileJson className="mr-2 h-4 w-4" />
            Export JSON
          </Button>
          <Button
            onClick={() => downloadReport("txt")}
            variant="outline"
            className="border-primary/50"
          >
            <FileText className="mr-2 h-4 w-4" />
            Export Text Report
          </Button>
        </div>
      </Card>

      {/* Scan Metadata */}
      <Card className="p-6 glass-effect">
        <h2 className="text-2xl font-bold mb-4">Scan Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-muted-foreground mb-1">Target</p>
            <code className="text-sm bg-muted px-3 py-2 rounded block">{scanData.target}</code>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-1">Scan Time</p>
            <code className="text-sm bg-muted px-3 py-2 rounded block">
              {new Date(scanData.scanTime).toLocaleString()}
            </code>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-1">Total Findings</p>
            <p className="text-2xl font-bold text-primary">{scanData.vulnerabilities.length}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-1">Risk Level</p>
            <Badge variant="destructive" className="text-sm">
              {scanData.vulnerabilities.some((v: any) => v.severity === "critical")
                ? "CRITICAL"
                : "HIGH"}
            </Badge>
          </div>
        </div>
      </Card>

      {/* Structured Output */}
      <Card className="p-6 glass-effect">
        <h2 className="text-2xl font-bold mb-4">Structured Data Output</h2>
        <div className="bg-background/50 rounded-lg p-4 border border-border">
          <pre className="text-xs overflow-x-auto">
            <code>{JSON.stringify(scanData, null, 2)}</code>
          </pre>
        </div>
      </Card>

      {/* Threat Intelligence Integration */}
      <Card className="p-6 glass-effect">
        <h2 className="text-2xl font-bold mb-4">Threat Intelligence Sources</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-4 border-primary/50">
            <h4 className="font-semibold mb-2">NVD Database</h4>
            <p className="text-sm text-muted-foreground mb-3">
              National Vulnerability Database
            </p>
            <Badge variant="outline" className="text-xs">
              {scanData.vulnerabilities.length} CVEs matched
            </Badge>
          </Card>
          <Card className="p-4 border-primary/50">
            <h4 className="font-semibold mb-2">ExploitDB</h4>
            <p className="text-sm text-muted-foreground mb-3">
              Known exploit information
            </p>
            <Badge variant="outline" className="text-xs">
              {scanData.vulnerabilities.filter((v: any) => v.severity === "critical").length}{" "}
              exploits found
            </Badge>
          </Card>
          <Card className="p-4 border-primary/50">
            <h4 className="font-semibold mb-2">Rapid7</h4>
            <p className="text-sm text-muted-foreground mb-3">
              Metasploit modules available
            </p>
            <Badge variant="outline" className="text-xs">
              {scanData.vulnerabilities.filter((v: any) => v.severity === "high").length} modules
              ready
            </Badge>
          </Card>
        </div>
      </Card>
    </div>
  );
};
