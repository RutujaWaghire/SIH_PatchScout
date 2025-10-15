import { useEffect, useRef, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { 
  Network, 
  Zap, 
  Shield, 
  AlertTriangle, 
  Target,
  Route,
  Database,
  Server,
  Globe
} from "lucide-react";

interface AttackPathProps {
  scanData: any;
}

interface Node {
  id: string;
  label: string;
  type: 'asset' | 'vulnerability' | 'exploit' | 'target';
  severity?: string;
  cvss?: number;
  x?: number;
  y?: number;
}

interface Edge {
  from: string;
  to: string;
  label?: string;
  type: 'exploits' | 'leads_to' | 'requires';
}

export const AttackPath = ({ scanData }: AttackPathProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [selectedPath, setSelectedPath] = useState("critical");
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  // Mock attack path data
  const attackPaths = {
    critical: {
      nodes: [
        { id: "internet", label: "Internet", type: "asset", x: 50, y: 300 },
        { id: "web-server", label: "Web Server\n(Apache 2.4.49)", type: "asset", x: 200, y: 300 },
        { id: "cve-2024-1234", label: "CVE-2024-1234\nRCE Vulnerability", type: "vulnerability", severity: "critical", cvss: 9.8, x: 350, y: 200 },
        { id: "shell-access", label: "Shell Access", type: "exploit", x: 500, y: 200 },
        { id: "db-server", label: "Database Server", type: "asset", x: 650, y: 300 },
        { id: "privilege-esc", label: "Privilege Escalation", type: "exploit", x: 500, y: 400 },
        { id: "admin-access", label: "Admin Access", type: "target", x: 800, y: 300 }
      ] as Node[],
      edges: [
        { from: "internet", to: "web-server", label: "HTTP Request", type: "leads_to" },
        { from: "web-server", to: "cve-2024-1234", label: "Exploits", type: "exploits" },
        { from: "cve-2024-1234", to: "shell-access", label: "Gains", type: "leads_to" },
        { from: "shell-access", to: "db-server", label: "Lateral Movement", type: "leads_to" },
        { from: "shell-access", to: "privilege-esc", label: "Attempts", type: "leads_to" },
        { from: "privilege-esc", to: "admin-access", label: "Achieves", type: "leads_to" }
      ] as Edge[]
    },
    high: {
      nodes: [
        { id: "user", label: "Authenticated User", type: "asset", x: 50, y: 300 },
        { id: "app", label: "Web Application", type: "asset", x: 200, y: 300 },
        { id: "sqli", label: "SQL Injection\nCVE-2024-5678", type: "vulnerability", severity: "high", cvss: 7.5, x: 350, y: 250 },
        { id: "data-access", label: "Database Access", type: "exploit", x: 500, y: 250 },
        { id: "sensitive-data", label: "Sensitive Data", type: "target", x: 650, y: 300 }
      ] as Node[],
      edges: [
        { from: "user", to: "app", label: "Login", type: "leads_to" },
        { from: "app", to: "sqli", label: "Malicious Input", type: "exploits" },
        { from: "sqli", to: "data-access", label: "Bypasses Auth", type: "leads_to" },
        { from: "data-access", to: "sensitive-data", label: "Extracts", type: "leads_to" }
      ] as Edge[]
    }
  };

  const currentPath = attackPaths[selectedPath as keyof typeof attackPaths];

  const getNodeColor = (node: Node) => {
    switch (node.type) {
      case 'asset': return '#3b82f6'; // blue
      case 'vulnerability': 
        return node.severity === 'critical' ? '#dc2626' : '#ea580c'; // red/orange
      case 'exploit': return '#f59e0b'; // yellow
      case 'target': return '#10b981'; // green
      default: return '#6b7280'; // gray
    }
  };

  const getNodeIcon = (type: string) => {
    switch (type) {
      case 'asset': return <Server className="h-4 w-4" />;
      case 'vulnerability': return <AlertTriangle className="h-4 w-4" />;
      case 'exploit': return <Zap className="h-4 w-4" />;
      case 'target': return <Target className="h-4 w-4" />;
      default: return <Network className="h-4 w-4" />;
    }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw edges
    currentPath.edges.forEach(edge => {
      const fromNode = currentPath.nodes.find(n => n.id === edge.from);
      const toNode = currentPath.nodes.find(n => n.id === edge.to);
      
      if (fromNode && toNode) {
        ctx.beginPath();
        ctx.moveTo(fromNode.x! + 50, fromNode.y! + 25);
        ctx.lineTo(toNode.x! + 50, toNode.y! + 25);
        ctx.strokeStyle = edge.type === 'exploits' ? '#dc2626' : '#6b7280';
        ctx.lineWidth = edge.type === 'exploits' ? 3 : 2;
        ctx.stroke();

        // Draw arrow
        const angle = Math.atan2(toNode.y! - fromNode.y!, toNode.x! - fromNode.x!);
        const arrowLength = 15;
        ctx.beginPath();
        ctx.moveTo(toNode.x! + 50 - arrowLength * Math.cos(angle - Math.PI / 6), 
                   toNode.y! + 25 - arrowLength * Math.sin(angle - Math.PI / 6));
        ctx.lineTo(toNode.x! + 50, toNode.y! + 25);
        ctx.lineTo(toNode.x! + 50 - arrowLength * Math.cos(angle + Math.PI / 6), 
                   toNode.y! + 25 - arrowLength * Math.sin(angle + Math.PI / 6));
        ctx.stroke();
      }
    });
  }, [currentPath, selectedPath]);

  const pathComplexity = currentPath.nodes.length;
  const exploitSteps = currentPath.edges.filter(e => e.type === 'exploits').length;

  return (
    <div className="space-y-6">
      <Card className="glass-effect border-primary/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Route className="h-5 w-5" />
              Attack Path Visualization
            </CardTitle>
            <Select value={selectedPath} onValueChange={setSelectedPath}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="critical">Critical Path</SelectItem>
                <SelectItem value="high">High Risk Path</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-6">
            <div className="flex items-center gap-2">
              <Network className="h-4 w-4 text-blue-500" />
              <span className="text-sm">Path Complexity: {pathComplexity}</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="h-4 w-4 text-yellow-500" />
              <span className="text-sm">Exploit Steps: {exploitSteps}</span>
            </div>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-red-500" />
              <span className="text-sm">Risk Level: {selectedPath.toUpperCase()}</span>
            </div>
            <div className="flex items-center gap-2">
              <Target className="h-4 w-4 text-green-500" />
              <span className="text-sm">Targets: {currentPath.nodes.filter(n => n.type === 'target').length}</span>
            </div>
          </div>

          <div className="relative border rounded-lg bg-card/50 overflow-hidden">
            <canvas 
              ref={canvasRef}
              width={900}
              height={500}
              className="absolute inset-0"
            />
            
            {/* Node overlays */}
            <div className="relative" style={{ width: '900px', height: '500px' }}>
              {currentPath.nodes.map((node) => (
                <div
                  key={node.id}
                  className={`absolute w-24 h-12 rounded-lg border-2 flex items-center justify-center cursor-pointer transition-all hover:scale-110 ${
                    hoveredNode === node.id ? 'z-10 scale-110' : ''
                  }`}
                  style={{
                    left: node.x,
                    top: node.y,
                    backgroundColor: getNodeColor(node),
                    borderColor: getNodeColor(node),
                  }}
                  onMouseEnter={() => setHoveredNode(node.id)}
                  onMouseLeave={() => setHoveredNode(null)}
                >
                  <div className="text-center">
                    <div className="text-white text-xs font-medium leading-tight">
                      {node.label.split('\n').map((line, i) => (
                        <div key={i}>{line}</div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Attack Path Steps */}
      <Card className="glass-effect">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Attack Steps & Mitigations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {currentPath.edges.map((edge, index) => {
              const fromNode = currentPath.nodes.find(n => n.id === edge.from);
              const toNode = currentPath.nodes.find(n => n.id === edge.to);
              
              return (
                <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded-full bg-primary text-primary-foreground text-xs flex items-center justify-center">
                        {index + 1}
                      </span>
                      <span className="text-sm font-medium">
                        {fromNode?.label} → {toNode?.label}
                      </span>
                    </div>
                    <Badge variant={edge.type === 'exploits' ? 'destructive' : 'outline'}>
                      {edge.type.replace('_', ' ')}
                    </Badge>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      View Details
                    </Button>
                    <Button size="sm" variant="outline">
                      Mitigation
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Risk Assessment */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="glass-effect border-red-500/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-500">
              <AlertTriangle className="h-5 w-5" />
              Critical Risks
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm">Immediate Threat</span>
              <Badge variant="destructive">HIGH</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Data Exposure Risk</span>
              <Badge variant="destructive">CRITICAL</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">System Compromise</span>
              <Badge variant="destructive">HIGH</Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-effect border-green-500/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-500">
              <Shield className="h-5 w-5" />
              Recommended Actions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="text-sm">
              • Patch Apache HTTP Server immediately
            </div>
            <div className="text-sm">
              • Implement input validation for SQL injection
            </div>
            <div className="text-sm">
              • Deploy network segmentation
            </div>
            <div className="text-sm">
              • Enable enhanced monitoring
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};