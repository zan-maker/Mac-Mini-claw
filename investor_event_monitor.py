#!/usr/bin/env python3
"""
Investor Event Monitor using OpenUtter
Attends online investor events, Zoom/Google Meet calls, and reports back
"""

import os
import sys
import json
import time
import subprocess
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from pathlib import Path

# OpenClaw workspace paths
WORKSPACE_DIR = "/Users/cubiczan/.openclaw/workspace"
OPENUTTER_DIR = os.path.join(WORKSPACE_DIR, "openutter")
TRANSCRIPTS_DIR = os.path.join(OPENUTTER_DIR, "transcripts")
EVENTS_DB = os.path.join(OPENUTTER_DIR, "investor_events.json")

class EventType(Enum):
    """Types of investor events"""
    EARNINGS_CALL = "earnings_call"
    VC_PITCH = "vc_pitch"
    INDUSTRY_WEBINAR = "industry_webinar"
    DEAL_SOURCING = "deal_sourcing"
    NETWORKING = "networking"
    CONFERENCE = "conference"
    ROADSHOW = "roadshow"

@dataclass
class InvestorEvent:
    """Investor event to monitor"""
    id: str
    name: str
    event_type: EventType
    meet_url: str
    scheduled_time: datetime
    duration_minutes: int = 60
    keywords: List[str] = None
    priority: int = 5  # 1-10, higher = more important
    auto_join: bool = True
    report_channel: str = "discord"  # discord, telegram, etc.
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "event_type": self.event_type.value,
            "meet_url": self.meet_url,
            "scheduled_time": self.scheduled_time.isoformat(),
            "duration_minutes": self.duration_minutes,
            "keywords": self.keywords,
            "priority": self.priority,
            "auto_join": self.auto_join,
            "report_channel": self.report_channel
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'InvestorEvent':
        """Create from dictionary"""
        return cls(
            id=data["id"],
            name=data["name"],
            event_type=EventType(data["event_type"]),
            meet_url=data["meet_url"],
            scheduled_time=datetime.fromisoformat(data["scheduled_time"]),
            duration_minutes=data.get("duration_minutes", 60),
            keywords=data.get("keywords", []),
            priority=data.get("priority", 5),
            auto_join=data.get("auto_join", True),
            report_channel=data.get("report_channel", "discord")
        )
    
    def is_upcoming(self, minutes_ahead: int = 15) -> bool:
        """Check if event is upcoming within X minutes"""
        now = datetime.now()
        time_until = (self.scheduled_time - now).total_seconds() / 60
        return 0 <= time_until <= minutes_ahead
    
    def is_ongoing(self) -> bool:
        """Check if event is currently happening"""
        now = datetime.now()
        end_time = self.scheduled_time + timedelta(minutes=self.duration_minutes)
        return self.scheduled_time <= now <= end_time

class OpenUtterManager:
    """Manager for OpenUtter Google Meet bot"""
    
    def __init__(self, auth_mode: str = "auth"):
        """
        Initialize OpenUtter manager
        
        Args:
            auth_mode: "auth" (authenticated) or "anon" (anonymous)
        """
        self.auth_mode = auth_mode
        self.bot_name = "Investor Intelligence Bot"
        self.running_sessions = {}  # event_id -> process
        
        # Create directories
        os.makedirs(OPENUTTER_DIR, exist_ok=True)
        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
    
    def check_openutter_installed(self) -> bool:
        """Check if OpenUtter is installed"""
        try:
            result = subprocess.run(["npx", "openutter", "--help"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def install_openutter(self) -> bool:
        """Install OpenUtter"""
        print("📦 Installing OpenUtter...")
        try:
            # Install to workspace
            cmd = ["npx", "openutter", "--target-dir", 
                  os.path.join(WORKSPACE_DIR, "skills", "openutter")]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ OpenUtter installed successfully")
                return True
            else:
                print(f"❌ OpenUtter installation failed: {result.stderr[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False
    
    def authenticate(self) -> bool:
        """Authenticate with Google for reliable joins"""
        print("🔑 Authenticating OpenUtter with Google...")
        print("   A browser will open. Sign in to Google, then press Enter in terminal.")
        
        try:
            result = subprocess.run(["npx", "openutter", "auth"], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Google authentication successful")
                return True
            else:
                print(f"⚠️  Authentication may need manual intervention: {result.stderr[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def join_meeting(self, event: InvestorEvent, headed: bool = False) -> Optional[subprocess.Popen]:
        """
        Join a Google Meet meeting
        
        Args:
            event: Investor event to join
            headed: Run with browser visible (for debugging)
            
        Returns:
            Process object if successful, None otherwise
        """
        print(f"🎯 Joining investor event: {event.name}")
        print(f"   URL: {event.meet_url}")
        print(f"   Time: {event.scheduled_time}")
        
        # Build OpenUtter command
        cmd = ["npx", "openutter", "join", event.meet_url]
        
        if self.auth_mode == "auth":
            cmd.append("--auth")
        else:
            cmd.extend(["--anon", "--bot-name", self.bot_name])
        
        if headed:
            cmd.append("--headed")
        
        # Add duration if specified
        if event.duration_minutes:
            cmd.extend(["--duration", f"{event.duration_minutes}m"])
        
        # Add channel for updates
        cmd.extend(["--channel", event.report_channel])
        
        # Add target if we have a specific channel ID
        # cmd.extend(["--target", "your-channel-id"])
        
        cmd.append("--verbose")
        
        try:
            # Start OpenUtter process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Store process
            self.running_sessions[event.id] = process
            
            # Start monitoring thread
            monitor_thread = threading.Thread(
                target=self._monitor_meeting,
                args=(event, process)
            )
            monitor_thread.daemon = True
            monitor_thread.start()
            
            print(f"✅ Joined meeting for event: {event.name}")
            return process
            
        except Exception as e:
            print(f"❌ Failed to join meeting: {e}")
            return None
    
    def _monitor_meeting(self, event: InvestorEvent, process: subprocess.Popen):
        """Monitor meeting process and capture output"""
        print(f"📊 Monitoring meeting: {event.name}")
        
        transcript_lines = []
        screenshot_count = 0
        
        try:
            # Read output line by line
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line:
                    print(f"[OpenUtter] {line}")
                    
                    # Capture transcript lines
                    if ":" in line and "[" in line and "]" in line:
                        transcript_lines.append(line)
                    
                    # Take periodic screenshots for important events
                    if self._should_take_screenshot(line, event):
                        self.take_screenshot(event)
                        screenshot_count += 1
            
            # Process completed
            process.wait()
            
            # Generate report
            self._generate_event_report(event, transcript_lines, screenshot_count)
            
            # Clean up
            if event.id in self.running_sessions:
                del self.running_sessions[event.id]
                
        except Exception as e:
            print(f"❌ Monitoring error for {event.name}: {e}")
    
    def _should_take_screenshot(self, line: str, event: InvestorEvent) -> bool:
        """Determine if we should take a screenshot based on content"""
        # Check for keywords
        keywords = event.keywords + [
            "funding", "investment", "valuation", "round",
            "acquisition", "exit", "IPO", "merger",
            "deal", "term sheet", "due diligence",
            "Q&A", "question", "answer", "feedback"
        ]
        
        line_lower = line.lower()
        for keyword in keywords:
            if keyword.lower() in line_lower:
                return True
        
        return False
    
    def take_screenshot(self, event: InvestorEvent) -> bool:
        """Take on-demand screenshot"""
        try:
            # Use OpenUtter screenshot command
            result = subprocess.run(
                ["npx", "openutter", "screenshot"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Move screenshot to event-specific location
                screenshot_src = os.path.join(WORKSPACE_DIR, "openutter", "on-demand-screenshot.png")
                screenshot_dst = os.path.join(
                    OPENUTTER_DIR, 
                    f"screenshot_{event.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
                
                if os.path.exists(screenshot_src):
                    os.rename(screenshot_src, screenshot_dst)
                    print(f"📸 Screenshot saved: {screenshot_dst}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return False
    
    def get_transcript(self, event: InvestorEvent, last_lines: int = None) -> List[str]:
        """Get transcript for an event"""
        transcript_path = os.path.join(TRANSCRIPTS_DIR, f"{event.id}.txt")
        
        if not os.path.exists(transcript_path):
            # Try to get from OpenUtter
            try:
                cmd = ["npx", "openutter", "transcript"]
                if last_lines:
                    cmd.extend(["--last", str(last_lines)])
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    # Save transcript
                    with open(transcript_path, 'w') as f:
                        f.write(result.stdout)
                    
                    return result.stdout.split('\n')
            except:
                pass
            
            return []
        
        # Read from file
        with open(transcript_path, 'r') as f:
            lines = f.readlines()
        
        if last_lines:
            lines = lines[-last_lines:]
        
        return [line.strip() for line in lines if line.strip()]
    
    def _generate_event_report(self, event: InvestorEvent, transcript: List[str], screenshot_count: int):
        """Generate report for an investor event"""
        print(f"📝 Generating report for: {event.name}")
        
        # Analyze transcript
        analysis = self._analyze_transcript(transcript, event)
        
        # Create report
        report = {
            "event_id": event.id,
            "event_name": event.name,
            "event_type": event.event_type.value,
            "date": datetime.now().isoformat(),
            "duration_minutes": event.duration_minutes,
            "transcript_line_count": len(transcript),
            "screenshot_count": screenshot_count,
            "key_insights": analysis.get("key_insights", []),
            "speakers": analysis.get("speakers", []),
            "keywords_found": analysis.get("keywords_found", []),
            "sentiment": analysis.get("sentiment", "neutral"),
            "recommended_actions": analysis.get("recommended_actions", [])
        }
        
        # Save report
        report_path = os.path.join(OPENUTTER_DIR, f"report_{event.id}.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report saved: {report_path}")
        
        # Send summary via OpenClaw
        self._send_event_summary(event, report)
        
        return report
    
    def _analyze_transcript(self, transcript: List[str], event: InvestorEvent) -> Dict:
        """Analyze transcript for key insights"""
        if not transcript:
            return {"key_insights": ["No transcript captured"], "sentiment": "unknown"}
        
        # Extract speakers
        speakers = set()
        for line in transcript:
            match = re.match(r'\[.*?\]\s*([^:]+):', line)
            if match:
                speakers.add(match.group(1).strip())
        
        # Find keywords
        keywords_found = []
        for line in transcript:
            for keyword in event.keywords:
                if keyword.lower() in line.lower():
                    keywords_found.append({
                        "keyword": keyword,
                        "context": line[:200]
                    })
        
        # Simple sentiment analysis
        positive_words = ["great", "excellent", "success", "growth", "profit", "opportunity"]
        negative_words = ["concern", "risk", "challenge", "loss", "decline", "problem"]
        
        positive_count = sum(1 for line in transcript for word in positive_words if word in line.lower())
        negative_count = sum(1 for line in transcript for word in negative_words if word in line.lower())
        
        if positive_count > negative_count * 2:
            sentiment = "positive"
        elif negative_count > positive_count * 2:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Extract key insights (simplified)
        key_insights = []
        for line in transcript[-20:]:  # Last 20 lines often contain Q&A and key points
            if any(word in line.lower() for word in ["conclusion", "summary", "key takeaway", "important"]):
                key_insights.append(line)
        
        # If no explicit insights, use lines with keywords
        if not key_insights and keywords_found:
            key_insights = [kf["context"] for kf in keywords_found[:3]]
        
        # Generate recommended actions
        recommended_actions = []
        if event.event_type == EventType.VC_PITCH:
            recommended_actions.extend([
                "Follow up with presenting companies",
                "Research mentioned competitors",
                "Check funding timelines discussed"
            ])
        elif event.event_type == EventType.EARNINGS_CALL:
            recommended_actions.extend([
                "Update financial models with new data",
                "Monitor stock price reaction",
                "Review guidance vs. actual results"
            ])
        
        return {
            "speakers": list(speakers),
            "keywords_found": keywords_found,
            "sentiment": sentiment,
            "key_insights": key_insights[:5],  # Top 5 insights
            "recommended_actions": recommended_actions
        }
    
    def _send_event_summary(self, event: InvestorEvent, report: Dict):
        """Send event summary via OpenClaw messaging"""
        try:
            # Create summary message
            summary = f"📊 **Investor Event Report: {event.name}**\n\n"
            summary += f"**Type:** {event.event_type.value.replace('_', ' ').title()}\n"
            summary += f"**Duration:** {report['duration_minutes']} minutes\n"
            summary += f"**Transcript:** {report['transcript_line_count']} lines\n"
            summary += f"**Screenshots:** {report['screenshot_count']}\n"
            summary += f"**Sentiment:** {report['sentiment'].title()}\n\n"
            
            if report['key_insights']:
                summary += "**Key Insights:**\n"
                for insight in report['key_insights'][:3]:
                    summary += f"• {insight[:100]}...\n"
                summary += "\n"
            
            if report['speakers']:
                summary += f"**Speakers:** {', '.join(report['speakers'][:5])}\n\n"
            
            if report['recommended_actions']:
                summary += "**Recommended Actions:**\n"
                for action in report['recommended_actions']:
                    summary += f"• {action}\n"
            
            # Send via OpenClaw message tool
            # Note: In production, you'd use the actual message tool
            print("\n" + "="*60)
            print("EVENT SUMMARY READY FOR OPENCLAW MESSAGING:")
            print("="*60)
            print(summary)
            print("="*60)
            print("\n(Would send to channel via OpenClaw message tool)")
            
            # Example of what would be sent:
            # message(action="send", channel="discord", message=summary)
            
        except Exception as e:
            print(f"❌ Failed to send summary: {e}")
    
    def leave_meeting(self, event_id: str):
        """Leave a meeting"""
        if event_id in self.running_sessions:
            process = self.running_sessions[event_id]
            process.terminate()
            try:
                process.wait(timeout=10)
            except:
                process.kill()
            
            del self.running_sessions[event_id]
            print(f"✅ Left meeting for event: {event_id}")
    
    def leave_all_meetings(self):
        """Leave all meetings"""
        for event_id in list(self.running_sessions.keys()):
            self.leave_meeting(event_id)

class InvestorEventScheduler:
    """Scheduler for investor events"""
    
    def __init__(self, db_path: str = EVENTS_DB):
        self.db_path = db_path
        self.events = self.load_events()
        self.openutter = OpenUtterManager()
    
    def load_events(self) -> Dict[str, InvestorEvent]:
        """Load events from database"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                
                events = {}
                for event_data in data.get("events", []):
                    event = InvestorEvent.from_dict(event_data)
                    events[event.id] = event
                
                print(f"✅ Loaded {len(events)} investor events")
                return events
            except Exception as e:
                print(f"❌ Failed to load events: {e}")
        
        return {}
    
    def save_events(self):
        """Save events to database"""
        try:
            data = {
                "events": [event.to_dict() for event in self.events.values()],
                "updated": datetime.now().isoformat()
            }
            
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Saved {len(self.events)} investor events")
        except Exception as e:
            print(f"❌ Failed to save events: {e}")
    
    def add_event(self, event: InvestorEvent):
        """Add a new investor event"""
        self.events[event.id] = event
        self.save_events()
        print(f"✅ Added event: {event.name}")
    
    def remove_event(self, event_id: str):
        """Remove an investor event"""
        if event_id in self.events:
            del self.events[event_id]
            self.save_events()
            print(f"✅ Removed event: {event_id}")
        else:
            print(f"❌ Event not found: {event_id}")
    
    def get_upcoming_events(self, minutes_ahead: int = 60) -> List[InvestorEvent]:
        """Get events scheduled within the next X minutes"""
        upcoming = []
        for event in self.events.values():
            if event.is_upcoming(minutes_ahead):
                upcoming.append(event)
        
        return sorted(upcoming, key=lambda e: e.scheduled_time)
    
    def get_ongoing_events(self) -> List[InvestorEvent]:
        """Get events currently happening"""
        ongoing = []
        for event in self.events.values():
            if event.is_ongoing():
                ongoing.append(event)
        
        return ongoing
    
    def monitor_and_join(self):
        """Monitor for upcoming events and join them"""
        print("🔍 Monitoring for upcoming investor events...")
        
        while True:
            try:
                # Check for upcoming events
                upcoming = self.get_upcoming_events(minutes_ahead=15)
                
                for event in upcoming:
                    if event.auto_join and event.id not in self.openutter.running_sessions:
                        print(f"⏰ Event starting soon: {event.name}")
                        self.openutter.join_meeting(event)
                
                # Check for ongoing events that need monitoring
                ongoing = self.get_ongoing_events()
                for event in ongoing:
                    if event.id not in self.openutter.running_sessions:
                        print(f"⚠️  Event ongoing but not joined: {event.name}")
                        # Could attempt late join here
                
                # Sleep before next check
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(60)

# Example events database
def create_example_events() -> List[InvestorEvent]:
    """Create example investor events for testing"""
    now = datetime.now()
    
    events = [
        InvestorEvent(
            id="vc_pitch_tech_2026",
            name="Tech Startup Pitch Day - Silicon Valley VC",
            event_type=EventType.VC_PITCH,
            meet_url="https://meet.google.com/abc-defg-hij",
            scheduled_time=now + timedelta(minutes=30),
            duration_minutes=120,
            keywords=["funding", "valuation", "SAAS", "AI", "seed round"],
            priority=8,
            auto_join=True,
            report_channel="discord"
        ),
        InvestorEvent(
            id="earnings_q4_2025",
            name="TechCorp Q4 2025 Earnings Call",
            event_type=EventType.EARNINGS_CALL,
            meet_url="https://meet.google.com/xyz-uvw-rst",
            scheduled_time=now + timedelta(hours=2),
            duration_minutes=90,
            keywords=["revenue", "guidance", "EPS", "growth", "outlook"],
            priority=7,
            auto_join=True,
            report_channel="discord"
        ),
        InvestorEvent(
            id="mining_investor_day",
            name="Mining & Resources Investor Day",
            event_type=EventType.INDUSTRY_WEBINAR,
            meet_url="https://meet.google.com/mno-pqr-stu",
            scheduled_time=now + timedelta(days=1),
            duration_minutes=180,
            keywords=["copper", "gold", "exploration", "resources", "commodities"],
            priority=6,
            auto_join=True,
            report_channel="discord"
        )
    ]
    
    return events

# Main function
def main():
    """Main function for investor event monitoring"""
    print("="*60)
    print("INVESTOR EVENT MONITOR - OpenUtter Integration")
    print("="*60)
    
    # Initialize
    scheduler = InvestorEventScheduler()
    
    # Check if we have events
    if not scheduler.events:
        print("No events found. Creating example events...")
        for event in create_example_events():
            scheduler.add_event(event)
    
    # Check OpenUtter installation
    if not scheduler.openutter.check_openutter_installed():
        print("OpenUtter not installed. Installing...")
        if not scheduler.openutter.install_openutter():
            print("❌ Failed to install OpenUtter. Exiting.")
            return
    
    # Authenticate (optional but recommended)
    print("\n🔑 Authentication (optional but recommended for reliable joins)")
    auth_choice = input("Authenticate with Google? (y/n): ").lower()
    if auth_choice == 'y':
        scheduler.openutter.authenticate()
    
    # Show upcoming events
    print("\n📅 Upcoming Investor Events:")
    upcoming = scheduler.get_upcoming_events(minutes_ahead=24*60)  # Next 24 hours
    if upcoming:
        for i, event in enumerate(upcoming, 1):
            time_str = event.scheduled_time.strftime("%Y-%m-%d %H:%M")
            print(f"{i}. {event.name}")
            print(f"   ⏰ {time_str} | 🎯 {event.event_type.value} | 🔑 {event.priority}/10")
            print(f"   🔗 {event.meet_url}")
            print()
    else:
        print("   No upcoming events in next 24 hours")
    
    # Start monitoring
    print("\n🚀 Starting event monitoring...")
    print("   Will auto-join events 15 minutes before start")
    print("   Press Ctrl+C to stop\n")
    
    try:
        scheduler.monitor_and_join()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")
    
    # Cleanup
    scheduler.openutter.leave_all_meetings()
    print("✅ Cleanup complete")

if __name__ == "__main__":
    main()
