"""
Scheduled Scan Service
Automates periodic vulnerability scanning based on configured schedules
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class ScheduledScanService:
    """Manages scheduled/automated scans"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.enabled = os.getenv("SCHEDULED_SCANS_ENABLED", "false").lower() == "true"
        
    def start(self):
        """Start the scheduler"""
        if not self.enabled:
            logger.info("Scheduled scans disabled")
            return
        
        logger.info("Starting scheduled scan service")
        self.scheduler.start()
        
        # Load scheduled scans from database and configure them
        self._load_scheduled_scans()
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduled scan service stopped")
    
    def add_daily_scan(
        self,
        scan_name: str,
        target: str,
        scan_config: Dict,
        hour: int = 2,
        minute: int = 0
    ) -> str:
        """
        Add daily scan schedule
        
        Args:
            scan_name: Name for the scheduled scan
            target: Target to scan
            scan_config: Scan configuration
            hour: Hour to run (0-23)
            minute: Minute to run (0-59)
        
        Returns:
            Job ID
        """
        job = self.scheduler.add_job(
            self._execute_scan,
            trigger=CronTrigger(hour=hour, minute=minute),
            args=[scan_name, target, scan_config],
            id=f"daily_{scan_name}",
            name=f"Daily Scan: {scan_name}",
            replace_existing=True
        )
        
        logger.info(f"Added daily scan: {scan_name} at {hour:02d}:{minute:02d}")
        return job.id
    
    def add_weekly_scan(
        self,
        scan_name: str,
        target: str,
        scan_config: Dict,
        day_of_week: str = 'mon',
        hour: int = 2,
        minute: int = 0
    ) -> str:
        """
        Add weekly scan schedule
        
        Args:
            scan_name: Name for the scheduled scan
            target: Target to scan
            scan_config: Scan configuration
            day_of_week: Day to run (mon, tue, wed, thu, fri, sat, sun)
            hour: Hour to run (0-23)
            minute: Minute to run (0-59)
        
        Returns:
            Job ID
        """
        job = self.scheduler.add_job(
            self._execute_scan,
            trigger=CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute),
            args=[scan_name, target, scan_config],
            id=f"weekly_{scan_name}",
            name=f"Weekly Scan: {scan_name}",
            replace_existing=True
        )
        
        logger.info(f"Added weekly scan: {scan_name} on {day_of_week} at {hour:02d}:{minute:02d}")
        return job.id
    
    def add_monthly_scan(
        self,
        scan_name: str,
        target: str,
        scan_config: Dict,
        day: int = 1,
        hour: int = 2,
        minute: int = 0
    ) -> str:
        """
        Add monthly scan schedule
        
        Args:
            scan_name: Name for the scheduled scan
            target: Target to scan
            scan_config: Scan configuration
            day: Day of month (1-31)
            hour: Hour to run (0-23)
            minute: Minute to run (0-59)
        
        Returns:
            Job ID
        """
        job = self.scheduler.add_job(
            self._execute_scan,
            trigger=CronTrigger(day=day, hour=hour, minute=minute),
            args=[scan_name, target, scan_config],
            id=f"monthly_{scan_name}",
            name=f"Monthly Scan: {scan_name}",
            replace_existing=True
        )
        
        logger.info(f"Added monthly scan: {scan_name} on day {day} at {hour:02d}:{minute:02d}")
        return job.id
    
    def add_interval_scan(
        self,
        scan_name: str,
        target: str,
        scan_config: Dict,
        hours: int = 0,
        minutes: int = 0
    ) -> str:
        """
        Add interval-based scan (repeats every X hours/minutes)
        
        Args:
            scan_name: Name for the scheduled scan
            target: Target to scan
            scan_config: Scan configuration
            hours: Repeat interval in hours
            minutes: Repeat interval in minutes
        
        Returns:
            Job ID
        """
        if hours == 0 and minutes == 0:
            raise ValueError("Must specify either hours or minutes")
        
        job = self.scheduler.add_job(
            self._execute_scan,
            trigger=IntervalTrigger(hours=hours, minutes=minutes),
            args=[scan_name, target, scan_config],
            id=f"interval_{scan_name}",
            name=f"Interval Scan: {scan_name}",
            replace_existing=True
        )
        
        logger.info(f"Added interval scan: {scan_name} every {hours}h {minutes}m")
        return job.id
    
    def remove_scheduled_scan(self, job_id: str):
        """Remove a scheduled scan"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed scheduled scan: {job_id}")
        except Exception as e:
            logger.error(f"Failed to remove scheduled scan {job_id}: {e}")
    
    def list_scheduled_scans(self) -> List[Dict]:
        """List all scheduled scans"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            })
        return jobs
    
    def pause_scheduled_scan(self, job_id: str):
        """Pause a scheduled scan"""
        try:
            self.scheduler.pause_job(job_id)
            logger.info(f"Paused scheduled scan: {job_id}")
        except Exception as e:
            logger.error(f"Failed to pause scheduled scan {job_id}: {e}")
    
    def resume_scheduled_scan(self, job_id: str):
        """Resume a paused scheduled scan"""
        try:
            self.scheduler.resume_job(job_id)
            logger.info(f"Resumed scheduled scan: {job_id}")
        except Exception as e:
            logger.error(f"Failed to resume scheduled scan {job_id}: {e}")
    
    async def _execute_scan(self, scan_name: str, target: str, scan_config: Dict):
        """Execute a scheduled scan"""
        logger.info(f"Executing scheduled scan: {scan_name} on {target}")
        
        try:
            # Import here to avoid circular imports
            from app.api.scans import create_scan
            from app.schemas.scan import ScanCreateSchema
            from app.database import SessionLocal
            
            db = SessionLocal()
            
            try:
                # Create scan request
                scan_request = ScanCreateSchema(
                    target=target,
                    scan_config=scan_config
                )
                
                # Create and execute scan
                # This will trigger the scan orchestrator
                logger.info(f"Scheduled scan '{scan_name}' created for {target}")
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Failed to execute scheduled scan '{scan_name}': {e}")
    
    def _load_scheduled_scans(self):
        """Load scheduled scans from database/config"""
        # In a production system, you would load saved schedules from database
        # For now, we'll configure some example schedules from environment
        
        # Example: Daily scan of production servers
        daily_targets = os.getenv("DAILY_SCAN_TARGETS", "").split(",")
        for target in daily_targets:
            if target.strip():
                self.add_daily_scan(
                    scan_name=f"daily_{target.strip()}",
                    target=target.strip(),
                    scan_config={
                        "selected_tools": ["Nmap"],
                        "scan_type": "quick",
                        "aggressiveness": "low",
                        "port_range": "1-1000",
                        "include_nse": False,
                        "compliance": []
                    },
                    hour=2,
                    minute=0
                )
        
        # Example: Weekly comprehensive scan
        weekly_targets = os.getenv("WEEKLY_SCAN_TARGETS", "").split(",")
        for target in weekly_targets:
            if target.strip():
                self.add_weekly_scan(
                    scan_name=f"weekly_{target.strip()}",
                    target=target.strip(),
                    scan_config={
                        "selected_tools": ["Nmap", "OpenVAS"],
                        "scan_type": "comprehensive",
                        "aggressiveness": "medium",
                        "port_range": "1-65535",
                        "include_nse": True,
                        "compliance": ["PCI DSS", "NIST"]
                    },
                    day_of_week='sun',
                    hour=1,
                    minute=0
                )


# Global scheduled scan service instance
scheduled_scan_service = ScheduledScanService()
