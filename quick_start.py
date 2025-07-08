#!/usr/bin/env python3
"""
Quick Start WiFi Password Retrieval
Simple examples for accessing WiFi passwords using Python in terminal
ETHICAL USE ONLY
"""

import subprocess
import platform
import sys

def check_system():
    """Check what operating system we're running on"""
    system = platform.system().lower()
    print(f"Detected OS: {system}")
    return system

def get_windows_passwords():
    """Quick method to get WiFi passwords on Windows"""
    print("Retrieving saved WiFi passwords on Windows...")
    
    try:
        # Get profiles
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                              capture_output=True, text=True, check=True)
        
        print("Available WiFi profiles:")
        profiles = []
        for line in result.stdout.split('\n'):
            if 'All User Profile' in line:
                profile = line.split(':')[1].strip()
                profiles.append(profile)
                print(f"  - {profile}")
        
        # Get password for first profile as example
        if profiles:
            first_profile = profiles[0]
            print(f"\nGetting password for: {first_profile}")
            
            pwd_result = subprocess.run([
                'netsh', 'wlan', 'show', 'profile', 
                f'name={first_profile}', 'key=clear'
            ], capture_output=True, text=True, check=True)
            
            for line in pwd_result.stdout.split('\n'):
                if 'Key Content' in line:
                    password = line.split(':')[1].strip()
                    print(f"Password: {password}")
                    break
                    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def get_linux_passwords():
    """Quick method to get WiFi passwords on Linux"""
    print("Retrieving saved WiFi passwords on Linux...")
    print("Note: This requires sudo privileges")
    
    try:
        # Check NetworkManager connections
        nm_path = "/etc/NetworkManager/system-connections/"
        
        print(f"Checking {nm_path} for saved connections...")
        result = subprocess.run(['sudo', 'ls', nm_path], 
                              capture_output=True, text=True, check=True)
        
        connections = result.stdout.strip().split('\n')
        if connections and connections[0]:
            print("Found connections:")
            for conn in connections[:3]:  # Show first 3
                print(f"  - {conn}")
                
                # Try to read first connection file
                if conn:
                    try:
                        cat_result = subprocess.run([
                            'sudo', 'cat', f"{nm_path}{conn}"
                        ], capture_output=True, text=True, check=True)
                        
                        lines = cat_result.stdout.split('\n')
                        ssid = None
                        psk = None
                        
                        for line in lines:
                            if line.startswith('ssid='):
                                ssid = line.split('=')[1]
                            elif line.startswith('psk='):
                                psk = line.split('=')[1]
                                
                        if ssid and psk:
                            print(f"SSID: {ssid}, Password: {psk}")
                            break
                            
                    except subprocess.CalledProcessError:
                        print(f"  Could not read {conn} (permission denied)")
                        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Make sure to run with sudo privileges")

def scan_networks():
    """Simple network scanner"""
    system = platform.system().lower()
    print("Scanning for available networks...")
    
    try:
        if system == "windows":
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                  capture_output=True, text=True, check=True)
            print("Saved networks:")
            for line in result.stdout.split('\n'):
                if 'All User Profile' in line:
                    profile = line.split(':')[1].strip()
                    print(f"  - {profile}")
                    
        elif system == "linux":
            # Try iwlist scan
            result = subprocess.run(['sudo', 'iwlist', 'scan'], 
                                  capture_output=True, text=True, check=True)
            
            networks = set()
            for line in result.stdout.split('\n'):
                if 'ESSID:' in line and '""' not in line:
                    ssid = line.split('ESSID:')[1].strip().strip('"')
                    if ssid:
                        networks.add(ssid)
            
            print("Available networks:")
            for network in sorted(networks):
                print(f"  - {network}")
                
        elif system == "darwin":  # macOS
            result = subprocess.run([
                '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', 
                '-s'
            ], capture_output=True, text=True, check=True)
            
            print("Available networks:")
            for line in result.stdout.split('\n')[1:6]:  # First 5 networks
                if line.strip():
                    network = line.split()[0]
                    print(f"  - {network}")
                    
    except subprocess.CalledProcessError as e:
        print(f"Error scanning: {e}")
    except FileNotFoundError:
        print("Required tools not found. Please install wireless-tools or equivalent")

def interactive_demo():
    """Interactive demonstration"""
    print("=" * 50)
    print("WiFi Password Retrieval - Quick Start Demo")
    print("ETHICAL USE ONLY - Your own networks only!")
    print("=" * 50)
    
    system = check_system()
    
    while True:
        print("\nOptions:")
        print("1. Scan for networks")
        print("2. Get saved passwords")
        print("3. Check system info")
        print("4. Exit")
        
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                scan_networks()
            elif choice == "2":
                if system == "windows":
                    get_windows_passwords()
                elif system == "linux":
                    get_linux_passwords()
                else:
                    print(f"Password retrieval not implemented for {system}")
            elif choice == "3":
                print(f"Operating System: {platform.system()}")
                print(f"Platform: {platform.platform()}")
                print(f"Python Version: {sys.version}")
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    interactive_demo()