/**
 * API Client for PatchScout Backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface ScanConfig {
  selected_tools: string[];
  scan_type: string;
  aggressiveness: string;
  port_range: string;
  exclude_ports?: string;
  include_nse: boolean;
  compliance: string[];
}

interface CreateScanRequest {
  target: string;
  scan_config: ScanConfig;
}

export const api = {
  // Scans
  async createScan(data: CreateScanRequest) {
    const response = await fetch(`${API_BASE_URL}/scans/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create scan');
    return response.json();
  },

  async listScans(page = 1, pageSize = 20, status?: string) {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString(),
      ...(status && { status }),
    });
    const response = await fetch(`${API_BASE_URL}/scans/?${params}`);
    if (!response.ok) throw new Error('Failed to fetch scans');
    return response.json();
  },

  async getScan(scanId: number) {
    const response = await fetch(`${API_BASE_URL}/scans/${scanId}`);
    if (!response.ok) throw new Error('Failed to fetch scan');
    return response.json();
  },

  async getScanVulnerabilities(scanId: number) {
    const response = await fetch(`${API_BASE_URL}/scans/${scanId}/vulnerabilities`);
    if (!response.ok) throw new Error('Failed to fetch vulnerabilities');
    return response.json();
  },

  async cancelScan(scanId: number) {
    const response = await fetch(`${API_BASE_URL}/scans/${scanId}/cancel`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to cancel scan');
    return response.json();
  },

  // Vulnerabilities
  async listVulnerabilities(filters: {
    page?: number;
    page_size?: number;
    severity?: string;
    scan_id?: number;
    cve_id?: string;
  } = {}) {
    const params = new URLSearchParams(
      Object.entries(filters).reduce((acc, [key, value]) => {
        if (value !== undefined) acc[key] = String(value);
        return acc;
      }, {} as Record<string, string>)
    );
    const response = await fetch(`${API_BASE_URL}/vulnerabilities/?${params}`);
    if (!response.ok) throw new Error('Failed to fetch vulnerabilities');
    return response.json();
  },

  async getVulnerability(vulnId: number) {
    const response = await fetch(`${API_BASE_URL}/vulnerabilities/${vulnId}`);
    if (!response.ok) throw new Error('Failed to fetch vulnerability');
    return response.json();
  },

  async markFalsePositive(vulnId: number, isFalsePositive: boolean) {
    const response = await fetch(
      `${API_BASE_URL}/vulnerabilities/${vulnId}/false-positive?is_false_positive=${isFalsePositive}`,
      { method: 'PATCH' }
    );
    if (!response.ok) throw new Error('Failed to update vulnerability');
    return response.json();
  },

  async getVulnerabilityStats() {
    const response = await fetch(`${API_BASE_URL}/vulnerabilities/stats/summary`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  },

  // AI Chat
  async sendChatMessage(message: string, ragMode = true, scanId?: number) {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        rag_mode: ragMode,
        scan_id: scanId,
      }),
    });
    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
  },

  // Attack Paths
  async getAttackPaths(scanId: number) {
    const response = await fetch(`${API_BASE_URL}/attack-paths/${scanId}`);
    if (!response.ok) throw new Error('Failed to fetch attack paths');
    return response.json();
  },

  async getAttackGraph(scanId: number) {
    const response = await fetch(`${API_BASE_URL}/attack-paths/${scanId}/graph`);
    if (!response.ok) throw new Error('Failed to fetch attack graph');
    return response.json();
  },

  // Reports
  async generateJsonReport(scanId: number) {
    const response = await fetch(`${API_BASE_URL}/reports/${scanId}/json`);
    if (!response.ok) throw new Error('Failed to generate report');
    return response.json();
  },

  async generateSummaryReport(scanId: number) {
    const response = await fetch(`${API_BASE_URL}/reports/${scanId}/summary`);
    if (!response.ok) throw new Error('Failed to generate summary');
    return response.json();
  },

  async downloadCsvReport(scanId: number) {
    const response = await fetch(`${API_BASE_URL}/reports/${scanId}/csv`);
    if (!response.ok) throw new Error('Failed to download CSV');
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `scan_${scanId}_report.csv`;
    a.click();
  },

  async getDashboardStats() {
    const response = await fetch(`${API_BASE_URL}/reports/dashboard/stats`);
    if (!response.ok) throw new Error('Failed to fetch dashboard stats');
    return response.json();
  },

  // Health Check
  async healthCheck() {
    const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`);
    if (!response.ok) throw new Error('Backend is not healthy');
    return response.json();
  },
};

export default api;
