#!/usr/bin/env python3
"""
Agent Browser Wrapper for OpenClaw Agents
Provides easy-to-use browser automation for all agents.
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
import time

@dataclass
class BrowserElement:
    """Represents a browser element with ref"""
    ref: str
    role: str
    name: str
    attributes: Dict[str, str]
    
    def __str__(self):
        return f"{self.ref}: {self.role} '{self.name}'"

@dataclass
class BrowserSnapshot:
    """Snapshot of page state"""
    url: str
    title: str
    elements: List[BrowserElement]
    timestamp: float
    
    def find_by_role(self, role: str, name: Optional[str] = None) -> List[BrowserElement]:
        """Find elements by role and optional name"""
        results = [e for e in self.elements if e.role == role]
        if name:
            results = [e for e in results if name.lower() in e.name.lower()]
        return results
    
    def find_by_text(self, text: str) -> List[BrowserElement]:
        """Find elements containing text"""
        return [e for e in self.elements if text.lower() in e.name.lower()]
    
    def get_ref(self, role: str, name: Optional[str] = None) -> Optional[str]:
        """Get ref for first matching element"""
        elements = self.find_by_role(role, name)
        return elements[0].ref if elements else None

class AgentBrowser:
    """
    Wrapper for Vercel Agent Browser CLI.
    Provides Pythonic interface for browser automation.
    """
    
    def __init__(self, 
                 session: Optional[str] = None,
                 profile: Optional[str] = None,
                 timeout: int = 30000,
                 headless: bool = True,
                 verbose: bool = False):
        """
        Initialize Agent Browser wrapper.
        
        Args:
            session: Session name for isolation
            profile: Persistent profile directory
            timeout: Default timeout in milliseconds
            headless: Run in headless mode
            verbose: Print commands and output
        """
        self.session = session
        self.profile = profile
        self.timeout = timeout
        self.headless = headless
        self.verbose = verbose
        
        # Set environment variables
        self.env = os.environ.copy()
        if timeout:
            self.env["AGENT_BROWSER_DEFAULT_TIMEOUT"] = str(timeout)
        if not headless:
            self.env["AGENT_BROWSER_HEADED"] = "1"
        
        # Current state
        self.current_url = None
        self.current_snapshot = None
        self.session_active = False
        
        # Test installation
        self._test_installation()
    
    def _test_installation(self):
        """Test if agent-browser is installed"""
        try:
            result = subprocess.run(
                ["agent-browser", "--version"],
                capture_output=True,
                text=True,
                env=self.env
            )
            if result.returncode != 0:
                raise RuntimeError("agent-browser not installed or not working")
            if self.verbose:
                print(f"✅ Agent Browser: {result.stdout.strip()}")
        except FileNotFoundError:
            raise RuntimeError(
                "agent-browser not installed. Run: npm install -g agent-browser && agent-browser install"
            )
    
    def _run_command(self, command: str, args: List[str] = None) -> Dict[str, Any]:
        """
        Run agent-browser command.
        
        Args:
            command: Command to run
            args: Additional arguments
            
        Returns:
            Dictionary with success, output, error
        """
        cmd = ["agent-browser"]
        
        # Add session if specified
        if self.session:
            cmd.extend(["--session", self.session])
        
        # Add profile if specified
        if self.profile:
            cmd.extend(["--profile", self.profile])
        
        # Add command
        cmd.append(command)
        
        # Add arguments
        if args:
            cmd.extend(args)
        
        if self.verbose:
            print(f"🔧 Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=self.env,
                timeout=(self.timeout / 1000) + 10  # Add 10 seconds buffer
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "error": result.stderr.strip(),
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": f"Command timed out after {self.timeout}ms",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }
    
    def _run_chain(self, commands: List[str]) -> Dict[str, Any]:
        """Run multiple commands chained with &&"""
        chain = " && ".join(commands)
        return self._run_command(chain, [])
    
    def open(self, url: str, wait_for_load: bool = True) -> bool:
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
            wait_for_load: Wait for network idle
            
        Returns:
            True if successful
        """
        commands = [f"open {url}"]
        if wait_for_load:
            commands.append("wait --load networkidle")
        
        result = self._run_chain(commands)
        
        if result["success"]:
            self.current_url = url
            self.session_active = True
            if self.verbose:
                print(f"✅ Navigated to: {url}")
        
        return result["success"]
    
    def snapshot(self, interactive: bool = True, compact: bool = True) -> Optional[BrowserSnapshot]:
        """
        Get page snapshot.
        
        Args:
            interactive: Only interactive elements
            compact: Compact output
            
        Returns:
            BrowserSnapshot object or None
        """
        args = ["--json"]
        if interactive:
            args.append("-i")
        if compact:
            args.append("-c")
        
        result = self._run_command("snapshot", args)
        
        if not result["success"]:
            if self.verbose:
                print(f"❌ Snapshot failed: {result['error']}")
            return None
        
        try:
            data = json.loads(result["output"])
            
            # Parse elements
            elements = []
            refs = data.get("refs", {})
            
            for ref_id, element_data in refs.items():
                element = BrowserElement(
                    ref=f"@{ref_id}",
                    role=element_data.get("role", ""),
                    name=element_data.get("name", ""),
                    attributes=element_data.get("attributes", {})
                )
                elements.append(element)
            
            # Get current URL and title
            url_result = self._run_command("get", ["url"])
            title_result = self._run_command("get", ["title"])
            
            snapshot = BrowserSnapshot(
                url=url_result["output"] if url_result["success"] else self.current_url or "",
                title=title_result["output"] if title_result["success"] else "",
                elements=elements,
                timestamp=time.time()
            )
            
            self.current_snapshot = snapshot
            
            if self.verbose:
                print(f"✅ Snapshot: {len(elements)} elements, URL: {snapshot.url}")
            
            return snapshot
            
        except json.JSONDecodeError as e:
            if self.verbose:
                print(f"❌ Failed to parse snapshot JSON: {e}")
            return None
    
    def click(self, selector: str) -> bool:
        """
        Click element.
        
        Args:
            selector: CSS selector, text selector, or ref
            
        Returns:
            True if successful
        """
        result = self._run_command("click", [selector])
        
        if self.verbose:
            if result["success"]:
                print(f"✅ Clicked: {selector}")
            else:
                print(f"❌ Click failed: {result['error']}")
        
        return result["success"]
    
    def fill(self, selector: str, text: str) -> bool:
        """
        Fill input field.
        
        Args:
            selector: CSS selector, text selector, or ref
            text: Text to fill
            
        Returns:
            True if successful
        """
        result = self._run_command("fill", [selector, text])
        
        if self.verbose:
            if result["success"]:
                print(f"✅ Filled {selector}: {text[:50]}...")
            else:
                print(f"❌ Fill failed: {result['error']}")
        
        return result["success"]
    
    def get_text(self, selector: str) -> Optional[str]:
        """
        Get text content of element.
        
        Args:
            selector: CSS selector, text selector, or ref
            
        Returns:
            Text content or None
        """
        result = self._run_command("get", ["text", selector])
        
        if result["success"]:
            return result["output"]
        
        if self.verbose:
            print(f"❌ Get text failed: {result['error']}")
        
        return None
    
    def screenshot(self, path: Optional[str] = None, annotate: bool = False) -> Optional[str]:
        """
        Take screenshot.
        
        Args:
            path: Path to save screenshot (None for temp file)
            annotate: Add element annotations
            
        Returns:
            Path to screenshot or None
        """
        if path is None:
            # Create temp file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                path = f.name
        
        args = [path]
        if annotate:
            args.append("--annotate")
        
        result = self._run_command("screenshot", args)
        
        if result["success"]:
            if self.verbose:
                print(f"✅ Screenshot saved: {path}")
            return path
        
        if self.verbose:
            print(f"❌ Screenshot failed: {result['error']}")
        
        return None
    
    def wait(self, selector: Optional[str] = None, timeout: Optional[int] = None) -> bool:
        """
        Wait for element or time.
        
        Args:
            selector: Element to wait for (None for time wait)
            timeout: Timeout in milliseconds
            
        Returns:
            True if successful
        """
        if selector:
            args = [selector]
        else:
            args = [str(timeout or 5000)]
        
        result = self._run_command("wait", args)
        return result["success"]
    
    def close(self) -> bool:
        """Close browser session."""
        result = self._run_command("close", [])
        
        if result["success"]:
            self.session_active = False
            self.current_url = None
            self.current_snapshot = None
            if self.verbose:
                print("✅ Browser closed")
        
        return result["success"]
    
    def find_and_click(self, role: str, name: Optional[str] = None) -> bool:
        """
        Find element by role and click it.
        
        Args:
            role: ARIA role (button, link, textbox, etc.)
            name: Element name (optional)
            
        Returns:
            True if successful
        """
        if not self.current_snapshot:
            if self.verbose:
                print("❌ No snapshot available. Call snapshot() first.")
            return False
        
        element = self.current_snapshot.get_ref(role, name)
        if not element:
            if self.verbose:
                print(f"❌ No {role} found" + (f" with name '{name}'" if name else ""))
            return False
        
        return self.click(element)
    
    def find_and_fill(self, role: str, text: str, name: Optional[str] = None) -> bool:
        """
        Find input by role and fill it.
        
        Args:
            role: ARIA role (textbox, searchbox, etc.)
            text: Text to fill
            name: Element name (optional)
            
        Returns:
            True if successful
        """
        if not self.current_snapshot:
            if self.verbose:
                print("❌ No snapshot available. Call snapshot() first.")
            return False
        
        element = self.current_snapshot.get_ref(role, name)
        if not element:
            if self.verbose:
                print(f"❌ No {role} found" + (f" with name '{name}'" if name else ""))
            return False
        
        return self.fill(element, text)
    
    def interactive_workflow(self, url: str) -> bool:
        """
        Complete interactive workflow:
        1. Navigate to URL
        2. Get snapshot
        3. Return success
        
        Args:
            url: URL to navigate to
            
        Returns:
            True if successful
        """
        if not self.open(url):
            return False
        
        snapshot = self.snapshot()
        if not snapshot:
            return False
        
        return True
    
    def login_workflow(self, url: str, username: str, password: str, 
                      username_field: str = "textbox", 
                      password_field: str = "textbox",
                      submit_button: str = "button") -> bool:
        """
        Complete login workflow.
        
        Args:
            url: Login page URL
            username: Username
            password: Password
            username_field: Role for username field
            password_field: Role for password field
            submit_button: Role for submit button
            
        Returns:
            True if successful
        """
        # Navigate to login page
        if not self.open(url):
            return False
        
        # Get snapshot
        snapshot = self.snapshot()
        if not snapshot:
            return False
        
        # Find and fill username
        username_ref = snapshot.get_ref(username_field, "username") or \
                      snapshot.get_ref(username_field, "email") or \
                      snapshot.get_ref(username_field, "user")
        
        if username_ref:
            if not self.fill(username_ref, username):
                return False
        else:
            # Try to find any textbox
            textboxes = snapshot.find_by_role("textbox")
            if textboxes and len(textboxes) >= 1:
                if not self.fill(textboxes[0].ref, username):
                    return False
        
        # Find and fill password
        password_ref = snapshot.get_ref(password_field, "password")
        if password_ref:
            if not self.fill(password_ref, password):
                return False
        else:
            # Try to find second textbox
            textboxes = snapshot.find_by_role("textbox")
            if textboxes and len(textboxes) >= 2:
                if not self.fill(textboxes[1].ref, password):
                    return False
        
        # Find and click submit
        submit_ref = snapshot.get_ref(submit_button, "sign in") or \
                    snapshot.get_ref(submit_button, "login") or \
                    snapshot.get_ref(submit_button, "submit")
        
        if submit_ref:
            if not self.click(submit_ref):
                return False
        else:
            # Try to find any button
            buttons = snapshot.find_by_role("button")
            if buttons:
                if not self.click(buttons[0].ref):
                    return False
        
        # Wait for login to complete
        time.sleep(2)
        
        return True
    
    def search_workflow(self, url: str, query: str, 
                       search_field: str = "searchbox",
                       search_button: str = "button") -> bool:
        """
        Complete search workflow.
        
        Args:
            url: Search page URL
            query: Search query
            search_field: Role for search field
            search_button: Role for search button
            
        Returns:
            True if successful
        """
        # Navigate to search page
        if not self.open(url):
            return False
        
        # Get snapshot
        snapshot = self.snapshot()
        if not snapshot:
            return False
        
        # Find and fill search
        search_ref = snapshot.get_ref(search_field, "search") or \
                    snapshot.get_ref("textbox", "search") or \
                    snapshot.get_ref("searchbox")
        
        if search_ref:
            if not self.fill(search_ref, query):
                return False
        else:
            # Try to find any textbox or searchbox
            inputs = snapshot.find_by_role("textbox") + snapshot.find_by_role("searchbox")
            if inputs:
                if not self.fill(inputs[0].ref, query):
                    return False
        
        # Find and click search button
        search_btn_ref = snapshot.get_ref(search_button, "search") or \
                        snapshot.get_ref(search_button, "go") or \
                        snapshot.get_ref("button", "search")
        
        if search_btn_ref:
            if not self.click(search_btn_ref):
                return False
        else:
            # Try pressing Enter
            if not self._run_command("press", ["Enter"])["success"]:
                return False
        
        # Wait for results
        time.sleep(2)
        
        return True

# Example usage
def example_usage():
    """Example of using AgentBrowser"""
    
    # Create browser instance
    browser = AgentBrowser(
        session="example-session",
        verbose=True
    )
    
    try:
        # Example 1: Simple navigation and snapshot
        print("\n📄 Example 1: Simple navigation")
        if browser.open("https://example.com"):
            snapshot = browser.snapshot()
            if snapshot:
                print(f"Page title: {snapshot.title}")
                print(f"Found {len(snapshot.elements)} elements")
                
                # Find all buttons
                buttons = snapshot.find_by_role("button")
                print(f"Found {len(buttons)} buttons")
        
        # Example 2: Search workflow
        print("\n🔍 Example 2: Search workflow")
        if browser.search_workflow("https://google.com", "OpenClaw AI"):
            snapshot = browser.snapshot()
            if snapshot:
                # Take screenshot
                screenshot = browser.screenshot(annotate=True)
                if screenshot:
                    print(f"Screenshot saved: {screenshot}")
        
        #