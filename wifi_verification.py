#!/usr/bin/env python3
"""
WiFi Verification System for Deerfields Mall Gamification System
Provides actual network detection and validation for mall WiFi access
"""

import subprocess
import platform
import re
import time
import logging
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta

from app.services.presence_service import PresenceService
from database import MallDatabase

class WiFiVerification:
    """Enhanced WiFi/GPS verification system integrated with presence tracking."""

    def __init__(self, presence_service: Optional[PresenceService] = None):
        self.mall_ssids = [
            "Deerfields_Free_WiFi",
            "Deerfields_Mall_WiFi",
            "Deerfields_Guest",
            "Deerfields_Staff"
        ]
        self.allowed_networks = [
            "Deerfields_Free_WiFi",
            "Deerfields_Mall_WiFi",
            "Deerfields_Guest"
        ]
        self.staff_networks = [
            "Deerfields_Staff"
        ]
        self.setup_logging()
        self.cache_duration = 30  # seconds
        self.network_cache = {}
        self.last_scan = None
        self.presence_service = presence_service
    
    def setup_logging(self):
        """Setup logging for WiFi verification"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('WiFiVerification')
    
    def get_current_network(self) -> Optional[Dict[str, str]]:
        """Get current WiFi network information"""
        try:
            system = platform.system()
            
            if system == "Windows":
                return self._get_windows_network()
            elif system == "Darwin":  # macOS
                return self._get_macos_network()
            elif system == "Linux":
                return self._get_linux_network()
            else:
                self.logger.warning(f"Unsupported operating system: {system}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting current network: {e}")
            return None
    
    def _get_windows_network(self) -> Optional[Dict[str, str]]:
        """Get current network on Windows"""
        try:
            # Get current network profile
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
            output = result.stdout
            
            # Extract SSID
            ssid_match = re.search(r'SSID\s+:\s+(.+)', output)
            if not ssid_match:
                return None
            
            ssid = ssid_match.group(1).strip()
            
            # Extract signal strength
            signal_match = re.search(r'Signal\s+:\s+(\d+)%', output)
            signal = int(signal_match.group(1)) if signal_match else 0
            
            # Extract authentication
            auth_match = re.search(r'Authentication\s+:\s+(.+)', output)
            auth = auth_match.group(1).strip() if auth_match else "Unknown"
            
            return {
                "ssid": ssid,
                "signal_strength": signal,
                "authentication": auth,
                "platform": "Windows"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting Windows network: {e}")
            return None
    
    def _get_macos_network(self) -> Optional[Dict[str, str]]:
        """Get current network on macOS"""
        try:
            # Get current network
            result = subprocess.run(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
            output = result.stdout
            
            # Extract SSID
            ssid_match = re.search(r' SSID: (.+)', output)
            if not ssid_match:
                return None
            
            ssid = ssid_match.group(1).strip()
            
            # Extract signal strength
            signal_match = re.search(r' agrCtlRSSI: (-?\d+)', output)
            signal = int(signal_match.group(1)) if signal_match else 0
            
            # Extract security
            security_match = re.search(r' security: (.+)', output)
            security = security_match.group(1).strip() if security_match else "Unknown"
            
            return {
                "ssid": ssid,
                "signal_strength": signal,
                "authentication": security,
                "platform": "macOS"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting macOS network: {e}")
            return None
    
    def _get_linux_network(self) -> Optional[Dict[str, str]]:
        """Get current network on Linux"""
        try:
            # Try iwgetid first
            result = subprocess.run(
                ["iwgetid", "-r"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                ssid = result.stdout.strip()
                
                # Get signal strength
                signal_result = subprocess.run(
                    ["iwconfig"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                signal = 0
                if signal_result.returncode == 0:
                    signal_match = re.search(r'Link Quality=(\d+)/(\d+)', signal_result.stdout)
                    if signal_match:
                        quality = int(signal_match.group(1))
                        max_quality = int(signal_match.group(2))
                        signal = int((quality / max_quality) * 100)
                
                return {
                    "ssid": ssid,
                    "signal_strength": signal,
                    "authentication": "Unknown",
                    "platform": "Linux"
                }
            
            # Fallback to nmcli
            result = subprocess.run(
                ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "device", "wifi", "list", "--rescan", "no"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line and not line.startswith('*'):
                        parts = line.split(':')
                        if len(parts) >= 3:
                            ssid = parts[0]
                            signal = int(parts[1]) if parts[1].isdigit() else 0
                            security = parts[2] if len(parts) > 2 else "Unknown"
                            
                            return {
                                "ssid": ssid,
                                "signal_strength": signal,
                                "authentication": security,
                                "platform": "Linux"
                            }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting Linux network: {e}")
            return None
    
    def scan_available_networks(self) -> List[Dict[str, str]]:
        """Scan for available WiFi networks"""
        try:
            # Check cache first
            if self.last_scan and (datetime.now() - self.last_scan).seconds < self.cache_duration:
                return self.network_cache.get('networks', [])
            
            system = platform.system()
            networks = []
            
            if system == "Windows":
                networks = self._scan_windows_networks()
            elif system == "Darwin":
                networks = self._scan_macos_networks()
            elif system == "Linux":
                networks = self._scan_linux_networks()
            
            # Update cache
            self.network_cache['networks'] = networks
            self.last_scan = datetime.now()
            
            return networks
            
        except Exception as e:
            self.logger.error(f"Error scanning networks: {e}")
            return []
    
    def _scan_windows_networks(self) -> List[Dict[str, str]]:
        """Scan networks on Windows"""
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "networks"],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode != 0:
                return []
            
            networks = []
            output = result.stdout
            
            # Parse network information
            network_blocks = output.split('SSID')
            
            for block in network_blocks[1:]:  # Skip first empty block
                lines = block.strip().split('\n')
                
                if not lines:
                    continue
                
                # Extract SSID
                ssid_line = lines[0]
                ssid_match = re.search(r'\s+(\d+)\s+:\s+(.+)', ssid_line)
                if not ssid_match:
                    continue
                
                ssid = ssid_match.group(2).strip()
                
                # Extract signal strength
                signal = 0
                for line in lines:
                    signal_match = re.search(r'Signal\s+:\s+(\d+)%', line)
                    if signal_match:
                        signal = int(signal_match.group(1))
                        break
                
                # Extract security
                security = "Unknown"
                for line in lines:
                    security_match = re.search(r'Authentication\s+:\s+(.+)', line)
                    if security_match:
                        security = security_match.group(1).strip()
                        break
                
                networks.append({
                    "ssid": ssid,
                    "signal_strength": signal,
                    "security": security
                })
            
            return networks
            
        except Exception as e:
            self.logger.error(f"Error scanning Windows networks: {e}")
            return []
    
    def _scan_macos_networks(self) -> List[Dict[str, str]]:
        """Scan networks on macOS"""
        try:
            result = subprocess.run(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode != 0:
                return []
            
            networks = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 4:
                    ssid = parts[0]
                    signal = int(parts[1]) if parts[1].isdigit() else 0
                    security = parts[2] if len(parts) > 2 else "Unknown"
                    
                    networks.append({
                        "ssid": ssid,
                        "signal_strength": signal,
                        "security": security
                    })
            
            return networks
            
        except Exception as e:
            self.logger.error(f"Error scanning macOS networks: {e}")
            return []
    
    def _scan_linux_networks(self) -> List[Dict[str, str]]:
        """Scan networks on Linux"""
        try:
            # Try nmcli first
            result = subprocess.run(
                ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "device", "wifi", "list", "--rescan", "yes"],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                networks = []
                lines = result.stdout.strip().split('\n')
                
                for line in lines:
                    if line and not line.startswith('*'):
                        parts = line.split(':')
                        if len(parts) >= 3:
                            ssid = parts[0]
                            signal = int(parts[1]) if parts[1].isdigit() else 0
                            security = parts[2] if len(parts) > 2 else "Unknown"
                            
                            networks.append({
                                "ssid": ssid,
                                "signal_strength": signal,
                                "security": security
                            })
                
                return networks
            
            # Fallback to iwlist
            result = subprocess.run(
                ["iwlist", "scan"],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                networks = []
                output = result.stdout
                
                # Parse iwlist output
                cell_blocks = output.split('Cell')
                
                for block in cell_blocks[1:]:
                    ssid_match = re.search(r'ESSID:"([^"]*)"', block)
                    if ssid_match:
                        ssid = ssid_match.group(1)
                        
                        # Extract signal strength
                        signal_match = re.search(r'Quality=(\d+)/(\d+)', block)
                        signal = 0
                        if signal_match:
                            quality = int(signal_match.group(1))
                            max_quality = int(signal_match.group(2))
                            signal = int((quality / max_quality) * 100)
                        
                        # Extract security
                        security = "Unknown"
                        if "WPA" in block:
                            security = "WPA"
                        elif "WEP" in block:
                            security = "WEP"
                        elif "open" in block.lower():
                            security = "Open"
                        
                        networks.append({
                            "ssid": ssid,
                            "signal_strength": signal,
                            "security": security
                        })
                
                return networks
            
            return []
            
        except Exception as e:
            self.logger.error(f"Error scanning Linux networks: {e}")
            return []
    
    def is_inside_mall(
        self,
        ssid: str = None,
        user_id: Optional[str] = None,
        device_info: Optional[Dict[str, Any]] = None,
        coords: Optional[Dict[str, float]] = None,
    ) -> bool:
        """Check if user is connected to mall WiFi.

        When ``user_id`` is supplied and the user is connected to a mall network
        a presence event is recorded.
        """
        try:
            current_network = self.get_current_network()

            if not current_network:
                return False

            current_ssid = current_network.get('ssid', '')

            # Check if current SSID is a mall network
            if current_ssid in self.allowed_networks:
                if user_id and self.presence_service:
                    self.presence_service.capture_wifi_event(
                        user_id,
                        current_ssid,
                        device_info or {},
                        coords or {},
                    )
                self.logger.info(f"Connected to mall network: {current_ssid}")
                return True

            # Check if specified SSID matches
            if ssid and current_ssid == ssid:
                if user_id and self.presence_service:
                    self.presence_service.capture_wifi_event(
                        user_id,
                        current_ssid,
                        device_info or {},
                        coords or {},
                    )
                return True

            self.logger.info(f"Not connected to mall network. Current: {current_ssid}")
            return False

        except Exception as e:
            self.logger.error(f"Error checking mall connection: {e}")
            return False
    
    def is_staff_member(self) -> bool:
        """Check if user is connected to staff network"""
        try:
            current_network = self.get_current_network()
            
            if not current_network:
                return False
            
            current_ssid = current_network.get('ssid', '')
            
            if current_ssid in self.staff_networks:
                self.logger.info(f"Connected to staff network: {current_ssid}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking staff connection: {e}")
            return False

    def record_gps_event(
        self,
        user_id: str,
        coords: Dict[str, float],
        device_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Record a GPS-based mall presence event.

        This is a light wrapper around ``PresenceService.capture_gps_event`` and
        expects coordinates already verified by the caller.
        """
        if not self.presence_service:
            return False
        try:
            return self.presence_service.capture_gps_event(
                user_id,
                coords,
                device_info or {},
            )
        except Exception as exc:  # pragma: no cover - safety
            self.logger.error(f"Error recording GPS event: {exc}")
            return False
    
    def get_network_quality(self) -> Dict[str, any]:
        """Get current network quality metrics"""
        try:
            current_network = self.get_current_network()
            
            if not current_network:
                return {
                    "connected": False,
                    "quality": "disconnected",
                    "signal_strength": 0,
                    "recommendation": "Connect to WiFi"
                }
            
            signal_strength = current_network.get('signal_strength', 0)
            
            # Determine quality level
            if signal_strength >= 80:
                quality = "excellent"
                recommendation = "Great connection!"
            elif signal_strength >= 60:
                quality = "good"
                recommendation = "Good connection"
            elif signal_strength >= 40:
                quality = "fair"
                recommendation = "Connection could be better"
            elif signal_strength >= 20:
                quality = "poor"
                recommendation = "Consider moving closer to WiFi source"
            else:
                quality = "very_poor"
                recommendation = "Connection is very weak"
            
            return {
                "connected": True,
                "ssid": current_network.get('ssid', ''),
                "quality": quality,
                "signal_strength": signal_strength,
                "authentication": current_network.get('authentication', 'Unknown'),
                "platform": current_network.get('platform', 'Unknown'),
                "recommendation": recommendation,
                "is_mall_network": current_network.get('ssid', '') in self.allowed_networks,
                "is_staff_network": current_network.get('ssid', '') in self.staff_networks
            }
            
        except Exception as e:
            self.logger.error(f"Error getting network quality: {e}")
            return {
                "connected": False,
                "quality": "error",
                "signal_strength": 0,
                "recommendation": "Error checking network"
            }
    
    def get_mall_networks(self) -> List[Dict[str, str]]:
        """Get available mall networks"""
        try:
            all_networks = self.scan_available_networks()
            mall_networks = []
            
            for network in all_networks:
                ssid = network.get('ssid', '')
                if ssid in self.mall_ssids:
                    mall_networks.append({
                        **network,
                        "type": "staff" if ssid in self.staff_networks else "public"
                    })
            
            return mall_networks
            
        except Exception as e:
            self.logger.error(f"Error getting mall networks: {e}")
            return []
    
    def validate_network_access(
        self,
        required_network: str = None,
        user_id: Optional[str] = None,
        device_info: Optional[Dict[str, Any]] = None,
        coords: Optional[Dict[str, float]] = None,
    ) -> Dict[str, any]:
        """Comprehensive network access validation.

        If ``user_id`` is provided and access is granted, a presence event is
        recorded using ``PresenceService``.
        """
        try:
            current_network = self.get_current_network()
            network_quality = self.get_network_quality()
            mall_networks = self.get_mall_networks()
            
            # Check if connected to any network
            if not current_network:
                return {
                    "access_granted": False,
                    "reason": "no_network",
                    "message": "No WiFi connection detected",
                    "current_network": None,
                    "network_quality": network_quality,
                    "available_mall_networks": mall_networks
                }
            
            current_ssid = current_network.get('ssid', '')
            
            # Check if connected to mall network
            if current_ssid in self.allowed_networks:
                if user_id and self.presence_service:
                    self.presence_service.capture_wifi_event(
                        user_id,
                        current_ssid,
                        device_info or {},
                        coords or {},
                    )
                return {
                    "access_granted": True,
                    "reason": "mall_network",
                    "message": f"Connected to mall network: {current_ssid}",
                    "current_network": current_network,
                    "network_quality": network_quality,
                    "available_mall_networks": mall_networks
                }
            
            # Check if connected to staff network
            if current_ssid in self.staff_networks:
                if user_id and self.presence_service:
                    self.presence_service.capture_wifi_event(
                        user_id,
                        current_ssid,
                        device_info or {},
                        coords or {},
                    )
                return {
                    "access_granted": True,
                    "reason": "staff_network",
                    "message": f"Connected to staff network: {current_ssid}",
                    "current_network": current_network,
                    "network_quality": network_quality,
                    "available_mall_networks": mall_networks
                }
            
            # Check if specific network is required
            if required_network and current_ssid == required_network:
                if user_id and self.presence_service:
                    self.presence_service.capture_wifi_event(
                        user_id,
                        current_ssid,
                        device_info or {},
                        coords or {},
                    )
                return {
                    "access_granted": True,
                    "reason": "specific_network",
                    "message": f"Connected to required network: {current_ssid}",
                    "current_network": current_network,
                    "network_quality": network_quality,
                    "available_mall_networks": mall_networks
                }
            
            # Check if mall networks are available
            if mall_networks:
                return {
                    "access_granted": False,
                    "reason": "wrong_network",
                    "message": f"Please connect to a mall network. Available: {[n['ssid'] for n in mall_networks]}",
                    "current_network": current_network,
                    "network_quality": network_quality,
                    "available_mall_networks": mall_networks
                }
            else:
                return {
                    "access_granted": False,
                    "reason": "no_mall_networks",
                    "message": "No mall networks detected. Please ensure you are inside the mall.",
                    "current_network": current_network,
                    "network_quality": network_quality,
                    "available_mall_networks": mall_networks
                }
            
        except Exception as e:
            self.logger.error(f"Error validating network access: {e}")
            return {
                "access_granted": False,
                "reason": "error",
                "message": f"Error checking network access: {str(e)}",
                "current_network": None,
                "network_quality": None,
                "available_mall_networks": []
            }

# Global WiFi verification instance hooked to presence tracking
_db = MallDatabase()
_presence_service = PresenceService(_db)
wifi_verification = WiFiVerification(_presence_service)
