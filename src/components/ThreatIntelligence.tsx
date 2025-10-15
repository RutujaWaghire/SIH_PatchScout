import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { 
  Globe, 
  AlertTriangle, 
  Eye, 
  TrendingUp, 
  Clock,
  MapPin,
  Users,
  Database,
  ExternalLink
} from "lucide-react";

interface ThreatIntelligenceProps {
  scanData?: any;
}

export const ThreatIntelligence = ({ scanData }: ThreatIntelligenceProps) => {
  // Mock threat intelligence data
  const threatData = {
    globalThreats: {
      activeCampaigns: 47,
      newCVEs: 23,
      exploitReleases: 12,
      malwareFamilies: 156
    },
    targetedThreats: [
      {
        name: "APT29 (Cozy Bear)",
        targeting: "Government, Healthcare",
        confidence: 0.85,
        lastActivity: "2 hours ago",
        ttps: ["T1190", "T1059", "T1083"],
        description: "Advanced persistent threat group linked to Russian intelligence, currently exploiting Apache vulnerabilities"
      },
      {
        name: "Lazarus Group",
        targeting: "Financial, Cryptocurrency",
        confidence: 0.78,
        lastActivity: "6 hours ago", 
        ttps: ["T1566", "T1055", "T1021"],
        description: "North Korean-linked group focusing on financial theft and espionage"
      },
      {
        name: "DarkHalo",
        targeting: "Technology, Government",
        confidence: 0.92,
        lastActivity: "1 day ago",
        ttps: ["T1078", "T1140", "T1027"],
        description: "Sophisticated group using supply chain attacks and living-off-the-land techniques"
      }
    ],
    cveIntelligence: [
      {
        cve: "CVE-2024-1234",
        exploitStatus: "Active exploitation",
        threatActors: ["APT29", "DarkHalo"],
        firstSeen: "2024-01-15",
        malwareFamilies: ["Cobalt Strike", "Metasploit"],
        urgency: "critical"
      },
      {
        cve: "CVE-2024-5678", 
        exploitStatus: "PoC available",
        threatActors: ["Script kiddies"],
        firstSeen: "2024-02-03",
        malwareFamilies: ["SQLMap"],
        urgency: "high"
      }
    ],
    geographicalIntel: [
      { country: "Russia", threatLevel: "High", activities: 89 },
      { country: "China", threatLevel: "High", activities: 76 },
      { country: "North Korea", threatLevel: "Medium", activities: 45 },
      { country: "Iran", threatLevel: "Medium", activities: 34 }
    ],
    industryTargeting: [
      { sector: "Government", attacks: 234, trend: "up" },
      { sector: "Healthcare", attacks: 198, trend: "up" },
      { sector: "Financial", attacks: 156, trend: "stable" },
      { sector: "Technology", attacks: 143, trend: "down" }
    ]
  };

  const getThreatLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-red-500';
    if (confidence >= 0.6) return 'text-orange-500';
    return 'text-yellow-500';
  };

  return (
    <div className="space-y-6">
      {/* Global Threat Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="glass-effect border-red-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Campaigns</CardTitle>
            <Globe className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">{threatData.globalThreats.activeCampaigns}</div>
            <p className="text-xs text-muted-foreground">
              +12% from last week
            </p>
          </CardContent>
        </Card>

        <Card className="glass-effect border-orange-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">New CVEs</CardTitle>
            <AlertTriangle className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-500">{threatData.globalThreats.newCVEs}</div>
            <p className="text-xs text-muted-foreground">
              Published this week
            </p>
          </CardContent>
        </Card>

        <Card className="glass-effect border-yellow-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Exploit Releases</CardTitle>
            <Eye className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-500">{threatData.globalThreats.exploitReleases}</div>
            <p className="text-xs text-muted-foreground">
              New exploit codes
            </p>
          </CardContent>
        </Card>

        <Card className="glass-effect border-purple-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Malware Families</CardTitle>
            <Database className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-500">{threatData.globalThreats.malwareFamilies}</div>
            <p className="text-xs text-muted-foreground">
              Active variants tracked
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Threat Actor Intelligence */}
      <Card className="glass-effect">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            Threat Actor Intelligence
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {threatData.targetedThreats.map((threat, index) => (
              <div key={index} className="border rounded-lg p-4 space-y-3">
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-lg">{threat.name}</h3>
                      <span className={`text-sm font-medium ${getConfidenceColor(threat.confidence)}`}>
                        {Math.round(threat.confidence * 100)}% confidence
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground">{threat.targeting}</p>
                    <p className="text-sm">{threat.description}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground">Last Activity</div>
                    <div className="text-sm font-medium">{threat.lastActivity}</div>
                  </div>
                </div>
                
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium">TTPs:</span>
                    <div className="flex gap-1">
                      {threat.ttps.map((ttp, i) => (
                        <span key={i} className="text-xs px-2 py-1 rounded border bg-muted">
                          {ttp}
                        </span>
                      ))}
                    </div>
                  </div>
                  <Button size="sm" variant="outline">
                    <ExternalLink className="h-3 w-3 mr-1" />
                    View Profile
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* CVE Intelligence & Geographical Threats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* CVE Intelligence */}
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              CVE Intelligence
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {threatData.cveIntelligence.map((cve, index) => (
                <div key={index} className="border rounded-lg p-3 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{cve.cve}</span>
                    <span className={`text-xs px-2 py-1 rounded ${
                      cve.urgency === 'critical' 
                        ? 'bg-red-500/20 text-red-500' 
                        : 'bg-orange-500/20 text-orange-500'
                    }`}>
                      {cve.urgency.toUpperCase()}
                    </span>
                  </div>
                  <div className="text-sm text-muted-foreground">
                    <div>Status: {cve.exploitStatus}</div>
                    <div>First seen: {cve.firstSeen}</div>
                    <div>Threat actors: {cve.threatActors.join(', ')}</div>
                    <div>Malware: {cve.malwareFamilies.join(', ')}</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Geographical Intelligence */}
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="h-5 w-5" />
              Geographical Threats
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {threatData.geographicalIntel.map((geo, index) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${getThreatLevelColor(geo.threatLevel)}`} />
                    <div>
                      <div className="font-medium">{geo.country}</div>
                      <div className="text-sm text-muted-foreground">{geo.threatLevel} threat level</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">{geo.activities}</div>
                    <div className="text-xs text-muted-foreground">activities</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Industry Targeting Trends */}
      <Card className="glass-effect">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Industry Targeting Trends
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {threatData.industryTargeting.map((industry, index) => (
              <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="font-medium">{industry.sector}</div>
                  <div className={`flex items-center gap-1 text-xs ${
                    industry.trend === 'up' ? 'text-red-500' :
                    industry.trend === 'down' ? 'text-green-500' : 'text-gray-500'
                  }`}>
                    <TrendingUp className={`h-3 w-3 ${
                      industry.trend === 'down' ? 'rotate-180' : ''
                    }`} />
                    {industry.trend}
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-medium">{industry.attacks}</div>
                  <div className="text-xs text-muted-foreground">attacks</div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card className="glass-effect border-blue-500/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5 text-blue-500" />
            Threat Intelligence Actions
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            <Button variant="outline" className="h-auto p-3 flex flex-col items-start">
              <Globe className="h-4 w-4 mb-2" />
              <div className="text-left">
                <div className="font-medium">IOC Feed</div>
                <div className="text-xs text-muted-foreground">Latest indicators</div>
              </div>
            </Button>
            <Button variant="outline" className="h-auto p-3 flex flex-col items-start">
              <AlertTriangle className="h-4 w-4 mb-2" />
              <div className="text-left">
                <div className="font-medium">YARA Rules</div>
                <div className="text-xs text-muted-foreground">Detection rules</div>
              </div>
            </Button>
            <Button variant="outline" className="h-auto p-3 flex flex-col items-start">
              <Eye className="h-4 w-4 mb-2" />
              <div className="text-left">
                <div className="font-medium">TTP Analysis</div>
                <div className="text-xs text-muted-foreground">Behavior patterns</div>
              </div>
            </Button>
            <Button variant="outline" className="h-auto p-3 flex flex-col items-start">
              <Database className="h-4 w-4 mb-2" />
              <div className="text-left">
                <div className="font-medium">Export Intel</div>
                <div className="text-xs text-muted-foreground">STIX/TAXII format</div>
              </div>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};