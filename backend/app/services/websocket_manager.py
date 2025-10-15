"""
WebSocket Manager for Real-Time Updates
Provides live scan progress, vulnerability alerts, and system notifications
"""
import asyncio
import logging
from typing import Dict, List, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and broadcasts"""
    
    def __init__(self):
        # Active connections by scan ID
        self.scan_connections: Dict[int, Set[WebSocket]] = {}
        # Global connections (dashboard, etc.)
        self.global_connections: Set[WebSocket] = set()
        
    async def connect(self, websocket: WebSocket, scan_id: Optional[int] = None):
        """Accept new WebSocket connection"""
        await websocket.accept()
        
        if scan_id is not None:
            if scan_id not in self.scan_connections:
                self.scan_connections[scan_id] = set()
            self.scan_connections[scan_id].add(websocket)
            logger.info(f"Client connected to scan {scan_id}. Total: {len(self.scan_connections[scan_id])}")
        else:
            self.global_connections.add(websocket)
            logger.info(f"Client connected globally. Total: {len(self.global_connections)}")
    
    def disconnect(self, websocket: WebSocket, scan_id: Optional[int] = None):
        """Remove WebSocket connection"""
        if scan_id is not None and scan_id in self.scan_connections:
            self.scan_connections[scan_id].discard(websocket)
            if not self.scan_connections[scan_id]:
                del self.scan_connections[scan_id]
            logger.info(f"Client disconnected from scan {scan_id}")
        else:
            self.global_connections.discard(websocket)
            logger.info("Client disconnected from global")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Failed to send personal message: {e}")
    
    async def broadcast_to_scan(self, scan_id: int, message: dict):
        """Broadcast message to all clients watching a specific scan"""
        if scan_id not in self.scan_connections:
            return
        
        disconnected = set()
        for connection in self.scan_connections[scan_id]:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception as e:
                logger.error(f"Failed to broadcast to scan {scan_id}: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.scan_connections[scan_id].discard(conn)
    
    async def broadcast_globally(self, message: dict):
        """Broadcast message to all global clients"""
        disconnected = set()
        for connection in self.global_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception as e:
                logger.error(f"Failed to broadcast globally: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.global_connections.discard(conn)
    
    async def notify_scan_started(self, scan_id: int, target: str, tools: List[str]):
        """Notify clients that a scan has started"""
        message = {
            "type": "scan_started",
            "scan_id": scan_id,
            "target": target,
            "tools": tools,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_scan(scan_id, message)
        await self.broadcast_globally(message)
    
    async def notify_scan_progress(self, scan_id: int, progress: int, current_tool: str = None, message_text: str = None):
        """Notify clients of scan progress"""
        message = {
            "type": "scan_progress",
            "scan_id": scan_id,
            "progress": progress,
            "current_tool": current_tool,
            "message": message_text,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_scan(scan_id, message)
    
    async def notify_scan_completed(self, scan_id: int, vulnerabilities_found: int):
        """Notify clients that scan is complete"""
        message = {
            "type": "scan_completed",
            "scan_id": scan_id,
            "vulnerabilities_found": vulnerabilities_found,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_scan(scan_id, message)
        await self.broadcast_globally(message)
    
    async def notify_scan_failed(self, scan_id: int, error: str):
        """Notify clients that scan failed"""
        message = {
            "type": "scan_failed",
            "scan_id": scan_id,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_scan(scan_id, message)
        await self.broadcast_globally(message)
    
    async def notify_vulnerability_found(self, scan_id: int, vulnerability: dict):
        """Notify clients when a critical vulnerability is found"""
        if vulnerability.get('severity') in ['critical', 'high']:
            message = {
                "type": "vulnerability_found",
                "scan_id": scan_id,
                "vulnerability": {
                    "cve_id": vulnerability.get('cve_id'),
                    "title": vulnerability.get('title'),
                    "severity": vulnerability.get('severity'),
                    "cvss_score": vulnerability.get('cvss_score')
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.broadcast_to_scan(scan_id, message)
            await self.broadcast_globally(message)
    
    async def notify_system_alert(self, alert_type: str, message_text: str, severity: str = "info"):
        """Broadcast system-wide alert"""
        message = {
            "type": "system_alert",
            "alert_type": alert_type,
            "message": message_text,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_globally(message)


# Global WebSocket manager instance
manager = ConnectionManager()
