import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { 
  Shield, 
  AlertTriangle, 
  TrendingUp, 
  Clock, 
  Eye,
  Download,
  Filter,
  RefreshCw,
  Loader2
} from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { api } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

interface DashboardProps {
  scanData: any;
  refreshTrigger?: number;
}

export const Dashboard = ({ scanData, refreshTrigger }: DashboardProps) => {
  const { toast } = useToast();
  const [loading, setLoading] = useState(true);
  const [dashboardStats, setDashboardStats] = useState<any>(null);
  const [recentScans, setRecentScans] = useState<any[]>([]);

  useEffect(() => {
    fetchDashboardData();
  }, [refreshTrigger]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch dashboard statistics from API
      const stats = await api.getDashboardStats();
      setDashboardStats(stats);

      // Fetch recent scans
      const scansResponse = await api.listScans(1, 5);
      setRecentScans(scansResponse.items || []);
      
    } catch (error: any) {
      console.error("Failed to fetch dashboard data:", error);
      toast({
        title: "Failed to Load Dashboard",
        description: error.message || "Could not connect to backend API. Using fallback data.",
        variant: "destructive",
      });
      
      // Fallback to mock data if API fails
      setDashboardStats({
        total_scans: 0,
        active_scans: 0,
        completed_scans: 0,
        failed_scans: 0,
        total_vulnerabilities: 0,
        critical_count: 0,
        high_count: 0,
        medium_count: 0,
        low_count: 0,
        risk_score: 0
      });
    } finally {
      setLoading(false);
    }
  };

  // Use real data from API or scanData
  const totalVulns = dashboardStats?.total_vulnerabilities || scanData?.vulnerabilities?.length || 0;
  const criticalCount = dashboardStats?.critical_count || scanData?.vulnerabilities?.filter((v: any) => v.severity === "critical").length || 0;
  const highCount = dashboardStats?.high_count || scanData?.vulnerabilities?.filter((v: any) => v.severity === "high").length || 0;
  const mediumCount = dashboardStats?.medium_count || scanData?.vulnerabilities?.filter((v: any) => v.severity === "medium").length || 0;
  const lowCount = dashboardStats?.low_count || scanData?.vulnerabilities?.filter((v: any) => v.severity === "low").length || 0;
  const riskScore = dashboardStats?.risk_score || 0;

  // Use sample data for visualization if no real data exists
  const hasRealData = totalVulns > 0;
  const severityData = hasRealData ? [
    { name: "Critical", value: criticalCount, color: "#dc2626" },
    { name: "High", value: highCount, color: "#ea580c" },
    { name: "Medium", value: mediumCount, color: "#ca8a04" },
    { name: "Low", value: lowCount, color: "#16a34a" }
  ] : [
    { name: "Critical", value: 8, color: "#dc2626" },
    { name: "High", value: 15, color: "#ea580c" },
    { name: "Medium", value: 22, color: "#ca8a04" },
    { name: "Low", value: 35, color: "#16a34a" }
  ];

  const threatIntelligence = {
    activeCampaigns: 3,
    exploitsAvailable: 7,
    threatActors: ["APT29", "Lazarus Group"],
    riskScore
  };

  const mockTrendData = [
    { month: "Oct", vulnerabilities: 28 },
    { month: "Nov", vulnerabilities: 23 },
    { month: "Dec", vulnerabilities: 31 },
    { month: "Jan", vulnerabilities: 19 },
    { month: "Feb", vulnerabilities: 25 },
    { month: "Mar", vulnerabilities: 22 }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Key Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="glass-effect border-primary/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Vulnerabilities</CardTitle>
            <Shield className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalVulns}</div>
            <p className="text-xs text-muted-foreground">
              +12% from last scan
            </p>
          </CardContent>
        </Card>

        <Card className="glass-effect border-red-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Issues</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">{criticalCount}</div>
            <p className="text-xs text-muted-foreground">
              Requires immediate attention
            </p>
          </CardContent>
        </Card>

        <Card className="glass-effect border-orange-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">High Risk</CardTitle>
            <TrendingUp className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-500">{highCount}</div>
            <p className="text-xs text-muted-foreground">
              Patch within 72 hours
            </p>
          </CardContent>
        </Card>

        <Card className="glass-effect border-blue-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Risk Score</CardTitle>
            <Eye className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-500">{threatIntelligence.riskScore}/10</div>
            <p className="text-xs text-muted-foreground">
              Based on threat intelligence
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Severity Distribution */}
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Vulnerability Distribution
            </CardTitle>
            {!hasRealData && (
              <p className="text-xs text-muted-foreground mt-1">
                Showing sample data - run a scan to see actual results
              </p>
            )}
          </CardHeader>
          <CardContent>
            {totalVulns === 0 && (
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="text-center space-y-2 mt-16">
                  <AlertTriangle className="h-12 w-12 mx-auto text-yellow-500 opacity-50" />
                  <p className="text-sm text-muted-foreground">No vulnerabilities detected yet</p>
                  <p className="text-xs text-muted-foreground">Run a scan to populate this chart</p>
                </div>
              </div>
            )}
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={severityData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={120}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                  opacity={hasRealData ? 1 : 0.4}
                >
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            {!hasRealData && (
              <div className="mt-4 flex items-center justify-center gap-4">
                {severityData.map((item) => (
                  <div key={item.name} className="flex items-center gap-2">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: item.color, opacity: 0.4 }}
                    />
                    <span className="text-xs text-muted-foreground">
                      {item.name}: {item.value}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Vulnerability Trends */}
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              6-Month Vulnerability Trend
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mockTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="vulnerabilities" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Threat Intelligence & Recent Scans */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Threat Intelligence */}
        <Card className="glass-effect border-yellow-500/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Eye className="h-5 w-5 text-yellow-500" />
              Threat Intelligence
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm">Active Campaigns</span>
              <Badge variant="destructive">{threatIntelligence.activeCampaigns}</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Available Exploits</span>
              <Badge variant="outline">{threatIntelligence.exploitsAvailable}</Badge>
            </div>
            <div className="space-y-2">
              <span className="text-sm font-medium">Known Threat Actors:</span>
              <div className="flex flex-wrap gap-2">
                {threatIntelligence.threatActors.map((actor) => (
                  <Badge key={actor} variant="secondary" className="text-xs">
                    {actor}
                  </Badge>
                ))}
              </div>
            </div>
            <div className="pt-2">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm">Overall Risk Score</span>
                <span className="text-sm font-bold">{threatIntelligence.riskScore}/10</span>
              </div>
              <Progress value={threatIntelligence.riskScore * 10} className="h-2" />
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Quick Actions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button className="w-full justify-start" variant="outline">
              <RefreshCw className="mr-2 h-4 w-4" />
              Run New Comprehensive Scan
            </Button>
            <Button className="w-full justify-start" variant="outline">
              <Download className="mr-2 h-4 w-4" />
              Export Vulnerability Report
            </Button>
            <Button className="w-full justify-start" variant="outline">
              <Filter className="mr-2 h-4 w-4" />
              Configure Scan Parameters
            </Button>
            <Button className="w-full justify-start" variant="outline">
              <Eye className="mr-2 h-4 w-4" />
              View Attack Path Analysis
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Recent Vulnerabilities Table */}
      {scanData?.vulnerabilities && (
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle>Recent Vulnerabilities</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {scanData.vulnerabilities.slice(0, 5).map((vuln: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <Badge variant={vuln.severity === "critical" ? "destructive" : "outline"}>
                        {vuln.severity.toUpperCase()}
                      </Badge>
                      <span className="font-medium">{vuln.id}</span>
                    </div>
                    <p className="text-sm text-muted-foreground">{vuln.title}</p>
                    <p className="text-xs text-muted-foreground">CVSS: {vuln.cvss}</p>
                  </div>
                  <Button size="sm" variant="outline">
                    View Details
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};