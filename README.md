# WiFi Password Retrieval and Security Testing Tools

⚠️ **IMPORTANT: ETHICAL USE ONLY** ⚠️

These tools are designed for **educational purposes** and **ethical security testing only**. Only use these tools on:
- Networks you own
- Networks you have explicit written permission to test
- Your own systems for retrieving forgotten passwords

**Unauthorized access to computer networks is illegal and may result in criminal charges.**

## Features

### Basic WiFi Password Retrieval (`wifi_password_retrieval.py`)
- Retrieve saved WiFi passwords from your own system (Windows/Linux/macOS)
- Scan for available WiFi networks
- Test for WPS vulnerabilities
- Educational weak password testing

### Advanced WiFi Security Testing (`advanced_wifi_security.py`)
- Monitor mode and packet injection testing
- Network scanning and information gathering
- WPA/WPA2 handshake capture
- Deauthentication attacks for handshake capture
- Handshake cracking with wordlists
- Fake access point creation
- Security vulnerability assessment

## Installation

### Prerequisites

1. **Python 3.6+** installed
2. **Linux system** (recommended for advanced features)
3. **WiFi adapter** that supports monitor mode and packet injection

### System Dependencies

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install aircrack-ng reaver wireless-tools python3-pip
sudo apt-get install hostapd dnsmasq
```

#### Fedora/CentOS:
```bash
sudo dnf install aircrack-ng reaver wireless-tools python3-pip
sudo dnf install hostapd dnsmasq
```

#### macOS:
```bash
brew install aircrack-ng python3
```

### Python Dependencies

```bash
pip3 install -r requirements.txt
```

or manually:

```bash
pip3 install scapy pywifi wifi
```

## Usage Examples

### Basic Password Retrieval

#### Retrieve saved passwords from your system:
```bash
python3 wifi_password_retrieval.py --retrieve
```

#### Scan for available networks:
```bash
python3 wifi_password_retrieval.py --scan
```

#### Test for WPS vulnerabilities:
```bash
python3 wifi_password_retrieval.py --test-wps wlan0
```

### Advanced Security Testing

⚠️ **Requires sudo privileges and monitor mode capable adapter**

#### Enable monitor mode:
```bash
sudo python3 advanced_wifi_security.py --monitor -i wlan0
```

#### Scan for networks (30 seconds):
```bash
sudo python3 advanced_wifi_security.py --scan -i wlan0 --duration 30
```

#### Test packet injection capability:
```bash
sudo python3 advanced_wifi_security.py --test-injection -i wlan0
```

#### Capture handshake (replace with actual BSSID):
```bash
sudo python3 advanced_wifi_security.py --capture AA:BB:CC:DD:EE:FF -i wlan0 --duration 60
```

#### Crack captured handshake:
```bash
python3 advanced_wifi_security.py --crack handshake_AABBCCDDEEFF.cap wordlist.txt
```

#### Create fake access point for testing:
```bash
sudo python3 advanced_wifi_security.py --fake-ap "TestAP" -i wlan0
```

## WiFi Adapters for Security Testing

For advanced features, you need a WiFi adapter that supports monitor mode and packet injection:

### Recommended Adapters:
- **ALFA AWUS036NHA** (Atheros AR9271) - Best for packet injection
- **ALFA AWUS036NH** (Ralink RT3070) - Good performance
- **TP-LINK TL-WN722N v1** (Atheros AR9271) - Budget option
- **Panda PAU09** (Ralink RT5372) - Compact option

### Chipsets that support monitor mode/injection:
- Atheros AR9271
- Ralink RT3070
- Ralink RT3572
- Ralink RT5370N
- Realtek RTL8812AU

## Legal and Ethical Guidelines

### ✅ Legal Uses:
- Testing your own networks
- Penetration testing with written authorization
- Educational purposes in controlled environments
- Recovering your own forgotten passwords
- Security research on your own equipment

### ❌ Illegal Uses:
- Accessing networks without permission
- Stealing passwords from others
- Disrupting public WiFi networks
- Any unauthorized network access
- Using these tools for malicious purposes

### Best Practices:
1. Always get written permission before testing
2. Only test on isolated networks when possible
3. Document your testing procedures
4. Report vulnerabilities responsibly
5. Use strong passwords on your own networks

## Command Reference

### Basic Tool Commands:
```bash
# Show help
python3 wifi_password_retrieval.py --help

# Retrieve all saved passwords
python3 wifi_password_retrieval.py --retrieve

# Scan for networks
python3 wifi_password_retrieval.py --scan
```

### Advanced Tool Commands:
```bash
# Show help
python3 advanced_wifi_security.py --help

# Enable monitor mode
sudo python3 advanced_wifi_security.py --monitor -i wlan0

# Scan networks for 60 seconds
sudo python3 advanced_wifi_security.py --scan --duration 60

# Capture handshake
sudo python3 advanced_wifi_security.py --capture [BSSID] --duration 120

# Crack handshake
python3 advanced_wifi_security.py --crack handshake.cap wordlist.txt
```

## Troubleshooting

### Common Issues:

#### "Permission denied" errors:
- Run with `sudo` for monitor mode operations
- Check file permissions

#### "Interface not found":
- Verify interface name with `iwconfig`
- Try `wlan0`, `wlp2s0`, or check `ip link show`

#### Monitor mode fails:
- Kill interfering processes: `sudo airmon-ng check kill`
- Check if adapter supports monitor mode
- Try different USB port

#### No handshakes captured:
- Make sure clients are connected to target network
- Increase capture duration
- Try deauth attack to force reconnection

#### Scapy import errors:
```bash
pip3 install scapy
# or
sudo pip3 install scapy
```

### Checking Adapter Capabilities:

```bash
# Check if adapter supports monitor mode
sudo iwconfig

# List USB devices
lsusb

# Check wireless interfaces
iwconfig

# Test monitor mode
sudo airmon-ng start wlan0
iwconfig
```

## Educational Resources

### Learning More:
- [Aircrack-ng Documentation](https://www.aircrack-ng.org/)
- [Scapy Documentation](https://scapy.readthedocs.io/)
- [WiFi Security Fundamentals](https://en.wikipedia.org/wiki/Wi-Fi_security)
- [802.11 Protocol Basics](https://en.wikipedia.org/wiki/IEEE_802.11)

### Practice Environments:
- Set up isolated test networks
- Use virtual machines
- Practice on your own equipment only
- Consider WiFi security courses

## Contributing

Contributions are welcome! Please:
1. Ensure all code follows ethical guidelines
2. Add appropriate warnings and disclaimers
3. Test thoroughly before submitting
4. Document new features clearly

## Disclaimer

This software is provided for educational and ethical testing purposes only. The authors are not responsible for any misuse of these tools. Users are solely responsible for ensuring their actions comply with applicable laws and regulations.

**Remember: With great power comes great responsibility. Use these tools wisely and ethically.**

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Always remember to use these tools responsibly and only on networks you own or have permission to test!**