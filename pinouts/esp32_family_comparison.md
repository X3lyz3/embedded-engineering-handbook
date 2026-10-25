# ESP32 SoC Family Hardware Comparison

*Source Reference: Official Espressif Technical Reference Manuals & Datasheets (ESP32, ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6).*

| Feature | ESP32 (Original) | ESP32-S2 | ESP32-S3 | ESP32-C3 | ESP32-C6 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CPU Architecture** | Xtensa LX6 (Dual-Core) | Xtensa LX7 (Single-Core) | Xtensa LX7 (Dual-Core + AI Vector) | 32-bit RISC-V (Single-Core) | 32-bit RISC-V (HP Core + LP Core) |
| **Max CPU Clock** | 240 MHz | 240 MHz | 240 MHz | 160 MHz | 160 MHz (HP) / 20 MHz (LP) |
| **Internal SRAM** | 520 KB | 320 KB | 512 KB | 400 KB | 512 KB (HP) + 16 KB (LP) |
| **Wi-Fi Standard** | 802.11 b/g/n (2.4 GHz) | 802.11 b/g/n (2.4 GHz) | 802.11 b/g/n (2.4 GHz) | 802.11 b/g/n (2.4 GHz) | **Wi-Fi 6 (802.11ax, 2.4 GHz)** |
| **Bluetooth / 802.15.4** | BT 4.2 BR/EDR + BLE | **None** | BLE 5.0 (Long Range + 2 Mbps) | BLE 5.0 | BLE 5.3 + **Zigbee 3.0 / Thread (802.15.4)** |
| **Native USB Controller** | No (Requires external UART bridge) | **Yes** (USB OTG 1.1) | **Yes** (USB OTG 1.1 + Serial/JTAG) | USB Serial/JTAG Controller | USB Serial/JTAG Controller |
| **Total SoC GPIO Pads** | 34 pads | 43 pads | 45 pads | 22 pads | 30 pads (QFN40) / 22 pads (QFN32) |
| **Usable GPIOs (Std Module)** | **~22 I/O + 4 Input-Only** *(GPIO 6–11 used by Flash)* | **Up to 36** *(GPIO 46 is Input-Only; 26–32 used by Flash)* | **Up to 36** *(GPIO 26–32 used by Flash/PSRAM)* | **Up to 16** *(GPIO 12–17 used by Flash)* | **Up to 23** *(GPIO 24–30 used by Flash)* |

---

## Hardware Native USB D- / D+ Pins (Direct Flashing & JTAG Without CH340/CP2102)

When routing a custom PCB with native USB support, connect the USB Type-C `D-` and `D+` differential pair directly to these pins (add 22 Ω series damping resistors only if required by specific hardware design guidelines, though S3/C3/C6 integrate internal series termination):

* **ESP32-S2 / ESP32-S3:** `GPIO 19` (`USB_D-`), `GPIO 20` (`USB_D+`)
* **ESP32-C3:** `GPIO 18` (`USB_D-`), `GPIO 19` (`USB_D+`)
* **ESP32-C6:** `GPIO 12` (`USB_D-`), `GPIO 13` (`USB_D+`)

> **⚠️ Hardware Design Note for Native USB:** On ESP32-S3, C3, and C6, the internal USB Serial/JTAG controller enumerates automatically as a CDC-ACM serial port and a JTAG debug probe—allowing step-by-step OpenOCD/GDB debugging over a single USB cable without an external FT2232H or ESP-Prog adapter. Avoid reconfiguring the USB `D-`/`D+` pins as general-purpose GPIOs in firmware if you rely on USB DFU/Serial re-flashing!
