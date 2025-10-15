"""
Email Notification Service
Sends email alerts for critical vulnerabilities, scan completions, and system events
"""
import asyncio
import logging
from typing import List, Dict, Optional
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

logger = logging.getLogger(__name__)

# Try to import aiosmtplib for async email
try:
    import aiosmtplib
    from jinja2 import Template
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    logger.warning("Email dependencies not installed. Email notifications disabled.")


class EmailService:
    """Email notification service with templating support"""
    
    def __init__(self):
        self.enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_username)
        self.from_name = os.getenv("FROM_NAME", "PatchScout Security")
        
        # Alert recipients
        self.alert_emails = os.getenv("ALERT_EMAILS", "").split(",")
        self.alert_emails = [email.strip() for email in self.alert_emails if email.strip()]
        
        # Minimum severity for email alerts
        self.min_severity = os.getenv("EMAIL_MIN_SEVERITY", "high")  # info, low, medium, high, critical
    
    def _is_configured(self) -> bool:
        """Check if email is properly configured"""
        return (
            self.enabled and
            EMAIL_AVAILABLE and
            bool(self.smtp_host and self.smtp_username and self.smtp_password and self.alert_emails)
        )
    
    async def send_critical_vulnerability_alert(
        self,
        scan_id: int,
        target: str,
        vulnerability: Dict
    ):
        """Send alert for critical vulnerability discovery"""
        if not self._is_configured():
            logger.info("Email not configured, skipping critical vulnerability alert")
            return
        
        severity = vulnerability.get('severity', 'unknown')
        if not self._should_alert(severity):
            return
        
        subject = f"🚨 {severity.upper()} Vulnerability Found - {target}"
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #dc2626; color: white; padding: 20px; text-align: center; }
                .content { background: #f9fafb; padding: 20px; margin-top: 20px; }
                .vulnerability { background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #dc2626; }
                .footer { margin-top: 20px; padding: 20px; text-align: center; font-size: 12px; color: #666; }
                .severity-critical { color: #dc2626; font-weight: bold; }
                .severity-high { color: #ea580c; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛡️ PatchScout Security Alert</h1>
                    <p>Critical Vulnerability Detected</p>
                </div>
                <div class="content">
                    <h2>Vulnerability Details</h2>
                    <div class="vulnerability">
                        <p><strong>Target:</strong> {{ target }}</p>
                        <p><strong>CVE ID:</strong> {{ cve_id }}</p>
                        <p><strong>Title:</strong> {{ title }}</p>
                        <p><strong>Severity:</strong> <span class="severity-{{ severity }}">{{ severity | upper }}</span></p>
                        <p><strong>CVSS Score:</strong> {{ cvss_score }}</p>
                        <p><strong>Description:</strong> {{ description }}</p>
                        <p><strong>Affected Component:</strong> {{ component }}</p>
                        <p><strong>Port/Service:</strong> {{ port }}/{{ service }}</p>
                    </div>
                    <h3>Recommended Actions</h3>
                    <p>{{ solution }}</p>
                    <h3>Scan Information</h3>
                    <p><strong>Scan ID:</strong> {{ scan_id }}</p>
                    <p><strong>Detected At:</strong> {{ timestamp }}</p>
                </div>
                <div class="footer">
                    <p>This is an automated alert from PatchScout Vulnerability Scanner</p>
                    <p>Please review and remediate this vulnerability as soon as possible</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_body = template.render(
            target=target,
            scan_id=scan_id,
            cve_id=vulnerability.get('cve_id', 'N/A'),
            title=vulnerability.get('title', 'Unknown'),
            severity=severity,
            cvss_score=vulnerability.get('cvss_score', 0),
            description=vulnerability.get('description', 'No description'),
            component=vulnerability.get('affected_component', 'Unknown'),
            port=vulnerability.get('port', 'N/A'),
            service=vulnerability.get('service', 'N/A'),
            solution=vulnerability.get('solution', 'Contact security team'),
            timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        )
        
        await self._send_email(
            subject=subject,
            html_body=html_body,
            recipients=self.alert_emails
        )
    
    async def send_scan_completion_report(
        self,
        scan_id: int,
        target: str,
        vulnerabilities_count: int,
        critical_count: int,
        high_count: int,
        medium_count: int,
        low_count: int,
        duration: str
    ):
        """Send scan completion summary"""
        if not self._is_configured():
            logger.info("Email not configured, skipping scan completion report")
            return
        
        # Only send if there are vulnerabilities
        if vulnerabilities_count == 0:
            return
        
        subject = f"📊 Scan Complete - {vulnerabilities_count} Vulnerabilities Found on {target}"
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #2563eb; color: white; padding: 20px; text-align: center; }
                .content { background: #f9fafb; padding: 20px; margin-top: 20px; }
                .stats { display: flex; justify-content: space-around; margin: 20px 0; }
                .stat-box { background: white; padding: 15px; text-align: center; border-radius: 8px; }
                .stat-number { font-size: 32px; font-weight: bold; }
                .critical { color: #dc2626; }
                .high { color: #ea580c; }
                .medium { color: #ca8a04; }
                .low { color: #16a34a; }
                .footer { margin-top: 20px; padding: 20px; text-align: center; font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛡️ PatchScout Scan Report</h1>
                    <p>Vulnerability Scan Completed</p>
                </div>
                <div class="content">
                    <h2>Scan Summary</h2>
                    <p><strong>Target:</strong> {{ target }}</p>
                    <p><strong>Scan ID:</strong> {{ scan_id }}</p>
                    <p><strong>Duration:</strong> {{ duration }}</p>
                    <p><strong>Total Vulnerabilities:</strong> {{ total }}</p>
                    
                    <div class="stats">
                        <div class="stat-box">
                            <div class="stat-number critical">{{ critical }}</div>
                            <div>Critical</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number high">{{ high }}</div>
                            <div>High</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number medium">{{ medium }}</div>
                            <div>Medium</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number low">{{ low }}</div>
                            <div>Low</div>
                        </div>
                    </div>
                    
                    <h3>Recommended Actions</h3>
                    <ul>
                        {% if critical > 0 %}
                        <li><strong>Immediate:</strong> Address {{ critical }} critical vulnerabilities</li>
                        {% endif %}
                        {% if high > 0 %}
                        <li><strong>Urgent:</strong> Remediate {{ high }} high-severity issues within 72 hours</li>
                        {% endif %}
                        <li>Review detailed scan results in PatchScout dashboard</li>
                        <li>Generate comprehensive report for stakeholders</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>This is an automated report from PatchScout Vulnerability Scanner</p>
                    <p>Visit your PatchScout dashboard for detailed analysis and remediation guidance</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_body = template.render(
            target=target,
            scan_id=scan_id,
            duration=duration,
            total=vulnerabilities_count,
            critical=critical_count,
            high=high_count,
            medium=medium_count,
            low=low_count
        )
        
        await self._send_email(
            subject=subject,
            html_body=html_body,
            recipients=self.alert_emails
        )
    
    async def send_scheduled_scan_report(
        self,
        report_type: str,
        data: Dict
    ):
        """Send scheduled reports (daily/weekly summary)"""
        if not self._is_configured():
            return
        
        subject = f"📈 {report_type} Security Report - PatchScout"
        
        # Simple template for now
        html_body = f"""
        <html>
        <body>
            <h1>{report_type} Security Report</h1>
            <p>Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <pre>{data}</pre>
        </body>
        </html>
        """
        
        await self._send_email(
            subject=subject,
            html_body=html_body,
            recipients=self.alert_emails
        )
    
    async def _send_email(
        self,
        subject: str,
        html_body: str,
        recipients: List[str],
        plain_body: Optional[str] = None
    ):
        """Send email using aiosmtplib"""
        try:
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{self.from_name} <{self.from_email}>"
            message['To'] = ", ".join(recipients)
            
            # Add plain text version
            if plain_body:
                part1 = MIMEText(plain_body, 'plain')
                message.attach(part1)
            
            # Add HTML version
            part2 = MIMEText(html_body, 'html')
            message.attach(part2)
            
            # Send email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_username,
                password=self.smtp_password,
                use_tls=self.smtp_use_tls
            )
            
            logger.info(f"Email sent successfully to {recipients}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    
    def _should_alert(self, severity: str) -> bool:
        """Check if severity meets minimum threshold for alerts"""
        severity_levels = ['info', 'low', 'medium', 'high', 'critical']
        try:
            min_index = severity_levels.index(self.min_severity)
            current_index = severity_levels.index(severity.lower())
            return current_index >= min_index
        except ValueError:
            return False


# Global email service instance
email_service = EmailService()
