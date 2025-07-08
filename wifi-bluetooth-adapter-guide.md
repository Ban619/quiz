# WiFi and Bluetooth Adapter Configuration Guide

## Understanding WiFi and Bluetooth Adapters

### Key Concepts

**Important:** You cannot literally "add bluetooth to a wifi adapter" - these are separate hardware components. However, many modern adapters are **combo devices** that include both WiFi and Bluetooth functionality in a single chip.

### Types of Adapters

1. **WiFi-only adapters** - Only provide wireless networking
2. **Bluetooth-only adapters** - Only provide Bluetooth connectivity  
3. **Combo adapters** - Single device with both WiFi and Bluetooth (most common today)

## Current System Status

Your current system shows:
- **Network interfaces:** `eth0` (ethernet), `lo` (loopback)
- **No wireless interfaces detected**
- **No bluetooth interfaces detected**
- **Missing network tools:** `ip`, `rfkill`, `lsusb` commands not available

## Setting Up WiFi and Bluetooth on Linux

### 1. Installing Required Tools

```bash
# On Ubuntu/Debian systems:
sudo apt update
sudo apt install wireless-tools wpasupplicant bluetooth bluez bluez-tools rfkill iw

# On RHEL/CentOS/Fedora:
sudo yum install wireless-tools wpa_supplicant bluez bluez-tools rfkill iw
# or
sudo dnf install wireless-tools wpa_supplicant bluez bluez-tools rfkill iw
```

### 2. Detecting WiFi and Bluetooth Adapters

```bash
# Check for USB devices (including adapters)
lsusb | grep -i -E "(wifi|wireless|bluetooth|802\.11)"

# List network interfaces
ip link show

# Check radio devices (WiFi and Bluetooth)
rfkill list

# List wireless interfaces specifically
iw dev

# Check bluetooth status
systemctl status bluetooth
hciconfig -a
```

### 3. Configuring a Combo WiFi/Bluetooth Adapter

#### WiFi Configuration

```bash
# Enable WiFi radio if blocked
sudo rfkill unblock wifi

# Scan for networks
sudo iw dev wlan0 scan | grep SSID

# Connect using wpa_supplicant
sudo wpa_passphrase "YourSSID" "YourPassword" >> /etc/wpa_supplicant/wpa_supplicant.conf
sudo wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
sudo dhclient wlan0
```

#### Bluetooth Configuration

```bash
# Enable Bluetooth radio if blocked
sudo rfkill unblock bluetooth

# Start Bluetooth service
sudo systemctl start bluetooth
sudo systemctl enable bluetooth

# Use bluetoothctl for device management
bluetoothctl
# In bluetoothctl:
# power on
# agent on
# discoverable on
# scan on
# pair <device_mac>
# connect <device_mac>
```

### 4. Common Combo Adapter Examples

#### Popular Combo Chipsets:
- **Intel AX200/AX201/AX210** - WiFi 6 + Bluetooth 5.x
- **Realtek RTL8822CE** - WiFi 5 + Bluetooth 5.0
- **Broadcom BCM43142** - WiFi + Bluetooth 4.0
- **Qualcomm Atheros QCA9377** - WiFi + Bluetooth

#### Checking Your Adapter Type:

```bash
# Check PCI devices
lspci | grep -i -E "(wifi|wireless|bluetooth|network)"

# Check USB devices  
lsusb | grep -i -E "(wifi|wireless|bluetooth)"

# Check loaded kernel modules
lsmod | grep -E "(wifi|bluetooth|wireless)"
```

### 5. Driver Installation

#### For Intel Adapters:
```bash
# Intel WiFi drivers usually included in kernel
# May need firmware package:
sudo apt install firmware-iwlwifi
```

#### For Realtek Adapters:
```bash
# May need additional drivers
sudo apt install rtl8821ce-dkms  # example for RTL8821CE
```

#### For Broadcom Adapters:
```bash
sudo apt install broadcom-sta-dkms
```

### 6. NetworkManager Configuration

```bash
# Install NetworkManager for easier management
sudo apt install network-manager

# Enable and start
sudo systemctl enable NetworkManager
sudo systemctl start NetworkManager

# Connect to WiFi via GUI or CLI
nmcli dev wifi connect "YourSSID" password "YourPassword"

# List available networks
nmcli dev wifi list
```

### 7. Troubleshooting

#### Common Issues:

1. **Adapter not detected:**
   ```bash
   # Check if hardware is recognized
   dmesg | grep -i -E "(wifi|bluetooth|wireless)"
   
   # Check USB connection (for USB adapters)
   lsusb
   
   # Check PCI connection (for internal adapters)
   lspci
   ```

2. **Driver issues:**
   ```bash
   # Check loaded modules
   lsmod | grep -E "(wifi|bluetooth)"
   
   # Check for firmware errors
   dmesg | grep firmware
   ```

3. **Radio blocked:**
   ```bash
   # Check and unblock radios
   rfkill list
   sudo rfkill unblock all
   ```

### 8. Modern System Configuration

#### Using systemd-networkd and systemd-resolved:

```bash
# WiFi configuration file: /etc/systemd/network/25-wireless.network
[Match]
Name=wlan0

[Network]
DHCP=yes
DNS=8.8.8.8

# WPA supplicant configuration: /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
network={
    ssid="YourSSID"
    psk="YourPassword"
}
```

## Next Steps

To proceed with your specific setup:

1. **Identify your adapter:** Run hardware detection commands
2. **Install appropriate drivers:** Based on your chipset
3. **Configure both services:** WiFi and Bluetooth independently
4. **Test functionality:** Ensure both work simultaneously

Would you like me to help you with any specific aspect of this configuration?