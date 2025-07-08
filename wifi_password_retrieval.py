#!/usr/bin/env python3
"""
WiFi Password Retrieval Tool
ETHICAL USE ONLY - Only use on networks you own or have permission to test
"""

import subprocess
import platform
import re
import os
import argparse
from pathlib import Path

class WiFiPasswordRetriever:
    def __init__(self):
        self.system = platform.system().lower()
        
    def get_saved_passwords_windows(self):
        """Retrieve saved WiFi passwords on Windows"""
        try:
            # Get list of saved WiFi profiles
            profiles_result = subprocess.run(
                ['netsh', 'wlan', 'show', 'profiles'], 
                capture_output=True, text=True, check=True
            )
            
            # Extract profile names
            profiles = re.findall(r'All User Profile\s*:\s*(.*)', profiles_result.stdout)
            
            wifi_passwords = {}
            for profile in profiles:
                profile = profile.strip()
                try:
                    # Get password for each profile
                    password_result = subprocess.run(
                        ['netsh', 'wlan', 'show', 'profile', f'name={profile}', 'key=clear'],
                        capture_output=True, text=True, check=True
                    )
                    
                    # Extract password
                    password_match = re.search(r'Key Content\s*:\s*(.*)', password_result.stdout)
                    if password_match:
                        wifi_passwords[profile] = password_match.group(1).strip()
                    else:
                        wifi_passwords[profile] = "No password or not accessible"
                        
                except subprocess.CalledProcessError:
                    wifi_passwords[profile] = "Error retrieving password"
                    
            return wifi_passwords
            
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return {}
    
    def get_saved_passwords_linux(self):
        """Retrieve saved WiFi passwords on Linux"""
        wifi_passwords = {}
        
        # Common NetworkManager connection paths
        nm_paths = [
            "/etc/NetworkManager/system-connections/",
            "/etc/NetworkManager/system-connections/",
        ]
        
        for nm_path in nm_paths:
            if os.path.exists(nm_path):
                try:
                    # Requires sudo privileges
                    for file_path in Path(nm_path).glob("*"):
                        if file_path.is_file():
                            try:
                                with open(file_path, 'r') as f:
                                    content = f.read()
                                    
                                # Extract SSID and password
                                ssid_match = re.search(r'ssid=(.*)', content)
                                psk_match = re.search(r'psk=(.*)', content)
                                
                                if ssid_match and psk_match:
                                    ssid = ssid_match.group(1).strip()
                                    password = psk_match.group(1).strip()
                                    wifi_passwords[ssid] = password
                                    
                            except PermissionError:
                                print(f"Permission denied: {file_path} (try running with sudo)")
                            except Exception as e:
                                print(f"Error reading {file_path}: {e}")
                                
                except Exception as e:
                    print(f"Error accessing {nm_path}: {e}")
                    
        return wifi_passwords
    
    def get_saved_passwords_macos(self):
        """Retrieve saved WiFi passwords on macOS"""
        wifi_passwords = {}
        
        try:
            # Get list of WiFi networks
            airport_result = subprocess.run(
                ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'],
                capture_output=True, text=True, check=True
            )
            
            # Extract SSIDs
            networks = re.findall(r'^\s*([^\s]+)', airport_result.stdout, re.MULTILINE)
            
            for ssid in networks[:10]:  # Limit to first 10 networks
                try:
                    # Get password from keychain
                    password_result = subprocess.run(
                        ['security', 'find-generic-password', '-wa', ssid],
                        capture_output=True, text=True, check=True
                    )
                    
                    password = password_result.stdout.strip()
                    if password:
                        wifi_passwords[ssid] = password
                        
                except subprocess.CalledProcessError:
                    wifi_passwords[ssid] = "Password not accessible or doesn't exist"
                    
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            
        return wifi_passwords
    
    def scan_networks(self):
        """Scan for available WiFi networks"""
        print("Scanning for available networks...")
        
        try:
            if self.system == "linux":
                # Using iwlist to scan
                result = subprocess.run(
                    ['sudo', 'iwlist', 'scan'], 
                    capture_output=True, text=True, check=True
                )
                
                # Extract SSIDs
                networks = re.findall(r'ESSID:"([^"]*)"', result.stdout)
                return list(set(networks))  # Remove duplicates
                
            elif self.system == "windows":
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'profiles'],
                    capture_output=True, text=True, check=True
                )
                
                networks = re.findall(r'All User Profile\s*:\s*(.*)', result.stdout)
                return [network.strip() for network in networks]
                
            elif self.system == "darwin":  # macOS
                result = subprocess.run(
                    ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'],
                    capture_output=True, text=True, check=True
                )
                
                networks = re.findall(r'^\s*([^\s]+)', result.stdout, re.MULTILINE)
                return networks
                
        except subprocess.CalledProcessError as e:
            print(f"Error scanning networks: {e}")
            return []
    
    def retrieve_saved_passwords(self):
        """Main method to retrieve saved passwords based on OS"""
        print(f"Retrieving saved WiFi passwords for {self.system}...")
        print("=" * 50)
        
        if self.system == "windows":
            return self.get_saved_passwords_windows()
        elif self.system == "linux":
            return self.get_saved_passwords_linux()
        elif self.system == "darwin":
            return self.get_saved_passwords_macos()
        else:
            print(f"Unsupported operating system: {self.system}")
            return {}

class WiFiSecurityTester:
    """Ethical WiFi security testing tools"""
    
    def __init__(self):
        self.common_passwords = [
            "password", "123456", "12345678", "admin", "password123",
            "qwerty", "letmein", "welcome", "monkey", "1234567890"
        ]
    
    def check_wps_vulnerability(self, interface="wlan0"):
        """Check for WPS vulnerabilities (requires appropriate tools)"""
        print("Checking for WPS vulnerabilities...")
        print("Note: This requires wash/reaver tools and monitor mode")
        
        try:
            # Put interface in monitor mode first
            subprocess.run(['sudo', 'airmon-ng', 'start', interface], check=True)
            
            # Scan for WPS-enabled networks
            result = subprocess.run(
                ['sudo', 'wash', '-i', f'{interface}mon'],
                capture_output=True, text=True, timeout=30
            )
            
            print("WPS-enabled networks found:")
            print(result.stdout)
            
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print("Make sure aircrack-ng suite is installed")
        except subprocess.TimeoutExpired:
            print("Scan completed (timeout reached)")
    
    def test_weak_passwords(self, ssid, password_list=None):
        """Test for weak passwords (educational purposes)"""
        if password_list is None:
            password_list = self.common_passwords
            
        print(f"Testing weak passwords for network: {ssid}")
        print("This is for educational purposes only!")
        
        for password in password_list:
            print(f"Testing password: {password}")
            # In a real implementation, you would test the connection here
            # This is just a demonstration
            
        print("Weak password testing completed")

def main():
    parser = argparse.ArgumentParser(description="WiFi Password Retrieval Tool (Ethical Use Only)")
    parser.add_argument("--scan", action="store_true", help="Scan for available networks")
    parser.add_argument("--retrieve", action="store_true", help="Retrieve saved passwords")
    parser.add_argument("--test-wps", help="Test for WPS vulnerabilities on interface")
    parser.add_argument("--test-weak", help="Test weak passwords for SSID")
    
    args = parser.parse_args()
    
    # Display warning
    print("WARNING: This tool is for educational and ethical purposes only!")
    print("Only use on networks you own or have explicit permission to test.")
    print("Unauthorized access to networks is illegal.")
    print("=" * 60)
    
    retriever = WiFiPasswordRetriever()
    tester = WiFiSecurityTester()
    
    if args.scan:
        networks = retriever.scan_networks()
        print("Available networks:")
        for i, network in enumerate(networks, 1):
            print(f"{i}. {network}")
    
    if args.retrieve:
        passwords = retriever.retrieve_saved_passwords()
        if passwords:
            print("\nSaved WiFi passwords:")
            for ssid, password in passwords.items():
                print(f"SSID: {ssid}")
                print(f"Password: {password}")
                print("-" * 30)
        else:
            print("No saved passwords found or permission denied")
    
    if args.test_wps:
        tester.check_wps_vulnerability(args.test_wps)
    
    if args.test_weak:
        tester.test_weak_passwords(args.test_weak)

if __name__ == "__main__":
    main()