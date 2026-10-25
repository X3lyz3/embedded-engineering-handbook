# ESP32 SoC Family Hardware Comparison

| Feature | ESP32 (Original) | ESP32-S2 | ESP32-S3 | ESP32-C3 | ESP32-C6 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Architecture** | Xtensa LX6 (Dual) | Xtensa LX7 (Single) | Xtensa LX7 (Dual) | RISC-V (Single) | RISC-V (Single + LP) |
| **Max Clock** | $240\text{ MHz}$ | $240\text{ MHz}$ | $240\text{ MHz}$ | $160\text{ MHz}$ | $160\text{ MHz}$ |
| **SRAM** | $520\text{ KB}$ | $320\text{ KB}$ | $512\text{ KB}$ | $400\text{ KB}$ | $512\text{ KB}$ |
| **Wi-Fi** | 802.11 b/g/n | 802.11 b/g/n | 802.11 b/g/n | 802.11 b/g/n | **Wi-Fi 6 (802.11ax)** |
| **Bluetooth** | BT 4.2 + BLE | **None** | BLE 5.0 | BLE 5.0 | BLE 5.3 + **Zigbee/Thread** |
| **Native USB OTG** | No (UART bridge) | **Yes** | **Yes** | USB Serial/JTAG only | USB Serial/JTAG only |
| **Total GPIOs** | 34 (6 input-only) | 43 (GPIO 46 in-only) | 45 | 22 | 30 |

## Hardware Native USB Pins (No CP2102/CH340 Required)
* **ESP32-S2 / ESP32-S3:** `GPIO 19` (`USB_D-`), `GPIO 20` (`USB_D+`)
* **ESP32-C3:** `GPIO 18` (`USB_D-`), `GPIO 19` (`USB_D+`)
* **ESP32-C6:** `GPIO 12` (`USB_D-`), `GPIO 13` (`USB_D+`)
