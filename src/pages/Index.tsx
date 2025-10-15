import { useState } from "react";
import { Scanner } from "@/components/Scanner";
import { Analyzer } from "@/components/Analyzer";
import { AIAssistant } from "@/components/AIAssistant";
import { ScanOutput } from "@/components/ScanOutput";
import { Dashboard } from "@/components/Dashboard";
import { AttackPath } from "@/components/AttackPath";
import { ThreatIntelligence } from "@/components/ThreatIntelligence";
import { Shield, Activity, BarChart3, Route, Globe, Zap } from "lucide-react";

const Index = () => {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [scanData, setScanData] = useState<any>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleScanComplete = (data: any) => {
    setScanData(data);
    setRefreshTrigger(prev => prev + 1); // Trigger dashboard refresh
    setActiveTab("analyzer"); // Switch to analyzer to show results
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-gradient-to-r from-card/80 via-card/50 to-card/80 backdrop-blur-xl sticky top-0 z-50 shadow-lg">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg gradient-primary glow-primary animate-pulse-glow">
                <Shield className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary via-accent to-primary bg-[length:200%_auto] animate-[gradient_3s_linear_infinite]">
                  PatchScout
                </h1>
                <p className="text-xs text-muted-foreground">Centralized Vulnerability Detection & AI-Powered Analysis</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Activity className="h-4 w-4 text-success animate-pulse" />
                <span className="text-sm text-muted-foreground">System Active</span>
              </div>
              <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20">
                <Zap className="h-3 w-3 text-primary" />
                <span className="text-xs text-primary font-medium">RAG Enabled</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="border-b border-border/30 bg-gradient-to-r from-card/20 via-card/40 to-card/20 backdrop-blur-md">
        <div className="container mx-auto px-6">
          <div className="flex gap-1 overflow-x-auto">
            {[
              { id: "dashboard", label: "Dashboard", icon: BarChart3 },
              { id: "scanner", label: "Scanner", icon: Shield },
              { id: "analyzer", label: "Analyzer", icon: Activity },
              { id: "attack-path", label: "Attack Paths", icon: Route },
              { id: "threat-intel", label: "Threat Intel", icon: Globe },
              { id: "assist", label: "AI Assistant", icon: Zap },
              { id: "output", label: "Reports", icon: Shield },
            ].map((tab) => {
              const IconComponent = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-6 py-3 text-sm font-medium transition-all duration-300 relative whitespace-nowrap ${
                    activeTab === tab.id
                      ? "text-primary scale-105"
                      : "text-muted-foreground hover:text-foreground hover:scale-102"
                  }`}
                >
                  <IconComponent className="h-4 w-4" />
                  {tab.label}
                  {activeTab === tab.id && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 gradient-primary glow-primary animate-pulse" />
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {activeTab === "dashboard" && <Dashboard scanData={scanData} refreshTrigger={refreshTrigger} />}
        {activeTab === "scanner" && <Scanner onScanComplete={handleScanComplete} />}
        {activeTab === "analyzer" && <Analyzer scanData={scanData} />}
        {activeTab === "attack-path" && <AttackPath scanData={scanData} />}
        {activeTab === "threat-intel" && <ThreatIntelligence scanData={scanData} />}
        {activeTab === "assist" && <AIAssistant />}
        {activeTab === "output" && <ScanOutput scanData={scanData} />}
      </main>
    </div>
  );
};

export default Index;
