---
name: raspberry-pi-maintenance
description: Workflow for managing Raspberry Pi hardware, specifically EEPROM recovery, firmware updates, and bootloader troubleshooting.
---

# Raspberry Pi Maintenance & EEPROM Recovery

This skill covers the critical process of recovering a "bricked" or unstable Raspberry Pi via EEPROM (bootloader) reset and updating firmware to stable versions.

## Trigger Conditions
- User reports a Pi that won't boot (no HDMI output, specific LED blink patterns).
- Request to "reset EEPROM", "restore bootloader", or "fix Pi boot issue".
- Need to update the EEPROM to a specific version or the latest stable release.

## Hardware-Specific Variants
⚠️ **Crucial**: Recovery images are NOT cross-compatible between chip families.

| Model Family | Chip / Family | Recovery Image / Firmware |
|--------------|----------------|----------------------------|
| **Pi 4 / 400 / CM4** | BCM2711 | `firmware-2711` |
| **Pi 5 / 500 / CM5** | BCM2712 | `firmware-2712` |

## Recovery Workflow (The "Bricked Pi" Path)

### 1. Create Recovery Media
**Method A: Raspberry Pi Imager (Recommended)**
1. Open Imager $\rightarrow$ **CHOOSE OS** $\rightarrow$ **Misc utility images** $\rightarrow$ **Bootloader**.
2. Select the correct model (e.g., **Pi 5 / Pi 500 / CM5**).
3. Select the desired recovery type (usually "SD Card Boot" or "Reset to factory defaults").
4. Write to a FAT32 SD card (small partitions, $<32\text{GB}$ preferred).

**Method B: Manual binary placement**
1. Download `pieeprom.bin` from [rpi-eeprom releases](https://github.com/raspberrypi/rpi-eeprom/releases).
2. Rename the binary to `recovery.bin` and place it in the root of a FAT32 formatted SD card.

### 2. Execution (Minimalist Setup)
To maximize success and avoid interference:
- **Minimal Hardware**: Only Pi + Power Supply + Recovery SD Card.
- **Peripherals**: Disconnect keyboards, mice, and other USB devices.
- **Power**: Use official power supplies (especially for Pi 5: 5V/5A) to prevent write failures.
- **Process**: Insert card $\rightarrow$ Power on $\rightarrow$ Wait $\ge 10$ seconds.

### 3. Verification (The LED/Screen Signal)
| Indicator | Success | Failure |
|-----------|---------|----------|
| **Pi 4 LED** | Rapid, continuous green blinking | Error blink pattern |
| **Pi 5 LED** | **Solid Green** (stays on) | No light or error blink pattern |
| **HDMI** | Screen turns **Green** | Screen turns **Red** |

**Pi 5 Error Blink Patterns:**
- 4 blinks: EEPROM recognition error.
- 7 blinks: SD card read error (try different card/format).
- 8 blinks: SDRAM initialization error.
- 5 blinks: Memory test failure.

### 4. Post-Recovery Validation
1. Remove recovery card.
2. Insert an SD card with a minimal OS (e.g., Raspberry Pi OS Lite).
3. Confirm boot to login prompt via HDMI or Serial.

## Firmware Update Workflow (The "Healthy Pi" Path)

Once the Pi is bootable, keep the EEPROM updated:

```bash
# Check current vs available version
sudo rpi-eeprom-update

# Update to latest stable (applied on next reboot)
sudo rpi-eeprom-update -a
sudo reboot
```

## Pitfalls & Advanced Fixes
- **MFG_VER Constraint**: Newer boards (like Pi 5 16GB) may have a minimum version requirement. If a recovery fails, ensure the Imager is updated to the latest version.
- **FAT32 Requirement**: Recovery media MUST be FAT32. ExFAT or NTFS will not be read by the bootloader.
- **Immediate Update Risk**: Avoid `RPI_EEPROM_IMMEDIATE_UPDATE=1` unless absolutely necessary; a power loss during immediate flash can permanently brick the board. Use the default staging method.
- **Deep Bricks**: If the recovery SD card isn't recognized, use the [usbboot tool](https://github.com/raspberrypi/usbboot) to flash via USB from another PC.
