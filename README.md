# ⚡ Systems & Hardware Engineering Handbook

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/X3lyz3/embedded-engineering-handbook)

> A high-density, zero-fluff reference guide for Embedded Systems, Analog/Digital Electronics, PCB Design, Engineering Math, and Linux System Administration. Rendered natively with GitHub LaTeX and Mermaid diagrams.

🌐 **Live Searchable Documentation:** [x3lyz3.github.io/embedded-engineering-handbook](https://x3lyz3.github.io/embedded-engineering-handbook/)

---

## 📂 Repository Structure
* 📄 **`README.md`** — Core engineering formulas, tables, and quick-reference diagrams.
* 🐍 **[`/scripts`](./scripts)** — Standalone calculation utilities (e.g., exact STM32 `PSC`/`ARR` timer register solver).
* 📌 **[`/pinouts`](./pinouts)** — Hardware architecture comparisons and native USB/GPIO pinout tables.
* 📈 **[`/simulations`](./simulations)** — Ready-to-run SPICE netlists (`.cir`) for Micro-Cap, LTspice, and ngspice.

---

## 🧭 Table of Contents
1. [Analog Electronics & Op-Amps](#-1-analog-electronics--op-amps)
2. [Embedded Systems & Microcontrollers](#-2-embedded-systems--microcontrollers)
3. [MCU Boot Traps & PCB Design Checklist](#-3-mcu-boot-traps--pcb-design-checklist)
4. [Engineering Mathematics](#-4-engineering-mathematics)
5. [Linux CLI & Hardware Debugging](#-5-linux-cli--hardware-debugging)
6. [SQL & Time-Series Telemetry](#-6-sql--time-series-telemetry)
7. [Bonus: Bytebeat & Algorithmic Audio](#-7-bonus-bytebeat--algorithmic-audio)

---

## 🔌 1. Analog Electronics & Op-Amps

### Passive RC / RL Filters
* **Capacitive Reactance:** $X_C = \frac{1}{2\pi f C}$
* **Inductive Reactance:** $X_L = 2\pi f L$
* **Cutoff Frequency ($-3\text{ dB}$ half-power point):**

$$f_c = \frac{1}{2\pi R C} = \frac{R}{2\pi L}$$

* **Time Constant ($\tau$):** $\tau = R \cdot C$ (Reaches $\approx 63.2\%$ of final value in $1\tau$, and $\approx 99.3\%$ in $5\tau$).

### Operational Amplifiers (Ideal Model: $Z_{in} = \infty$, $Z_{out} = 0$, $A_{OL} = \infty$)

| Configuration | Transfer Function | Input Impedance ($Z_{in}$) | Key Application |
| :--- | :--- | :--- | :--- |
| **Voltage Follower** | $V_{out} = V_{in}$ | $\infty$ (Ideal) | Buffering high-impedance sensors |
| **Inverting** | $V_{out} = -V_{in} \left(\frac{R_f}{R_{in}}\right)$ | $R_{in}$ | Phase inversion, current-to-voltage |
| **Non-Inverting** | $V_{out} = V_{in} \left(1 + \frac{R_f}{R_g}\right)$ | $\infty$ (Ideal) | High-impedance signal amplification |
| **Differential** | $V_{out} = \frac{R_f}{R_{in}}(V_2 - V_1)$ | $R_{in}$ | Shunt current sensing, noise rejection |
| **Integrator** | $V_{out}(t) = -\frac{1}{RC} \int_0^t V_{in}(\tau) \, d\tau$ | $R$ | Wave shaping (Square $\to$ Triangle), PID |

### BJT Transistor Operating Regions (NPN)
```mermaid
flowchart LR
    A[Base-Emitter Junction] --> B{V_BE > 0.7V?}
    B -->|No| C[Cutoff Region: Fully OFF]
    B -->|Yes| D{Base-Collector Junction}
    D -->|Reverse Biased: V_CE > V_BE| E[Active Region: Linear Amplifier]
    D -->|Forward Biased: V_CE ≈ 0.2V| F[Saturation: Fully ON Switch]
```
* **Collector Current (Active Region):** $I_C = \beta I_B = I_S \left( e^{\frac{V_{BE}}{V_T}} - 1 \right)$, where thermal voltage $V_T = \frac{kT}{q} \approx 25.85\text{ mV}$ at $300\text{ K}$.

---

## 🎛️ 2. Embedded Systems & Microcontrollers

### Bitwise Manipulation Macros (C / C++)
Essential register operations without corrupting adjacent bits:

```c
#define BIT_SET(REG, BIT)     ((REG) |= (1ULL << (BIT)))
#define BIT_CLEAR(REG, BIT)   ((REG) &= ~(1ULL << (BIT)))
#define BIT_TOGGLE(REG, BIT)  ((REG) ^= (1ULL << (BIT)))
#define BIT_READ(REG, BIT)    (((REG) >> (BIT)) & 1ULL)
```

### Hardware Communication Protocols
| Protocol | Wires | Duplex | Max Speed (Typical) | Topology | Pull-up Resistors? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **UART** | 2 (`TX`, `RX`) | Full | $\le 5\text{ Mbps}$ | Peer-to-Peer | No |
| **I2C** | 2 (`SDA`, `SCL`) | Half | $100\text{ kHz} - 3.4\text{ MHz}$ | Multi-Master / Multi-Slave | **Yes** ($2.2\text{ k}\Omega - 10\text{ k}\Omega$) |
| **SPI** | 4 (`MOSI`, `MISO`, `SCK`, `CS`) | Full | $10 - 100+\text{ MHz}$ | 1 Master / Multi-Slave | No |
| **CAN** | 2 (`CAN_H`, `CAN_L`) | Half | $1\text{ Mbps}$ (CAN 2.0) | Differential Bus | $120\,\Omega$ termination at ends |

### PWM & Servo Control Math (ESP32 / STM32)
Standard hobby servos (e.g., SG90, MG996R) expect a $50\text{ Hz}$ PWM signal ($T = 20\text{ ms}$ period):
* **$0^\circ$ (Min):** $1.0\text{ ms}$ pulse width ($5\%$ duty cycle) — *Note: many clones use $0.5\text{ ms}$*.
* **$90^\circ$ (Center):** $1.5\text{ ms}$ pulse width ($7.5\%$ duty cycle).
* **$180^\circ$ (Max):** $2.0\text{ ms}$ pulse width ($10\%$ duty cycle) — *Note: many clones use $2.5\text{ ms}$*.

**Timer Prescaler & Period Formula (STM32):**

$$f_{PWM} = \frac{f_{\text{TIM}}}{(\text{PSC} + 1) \cdot (\text{ARR} + 1)}$$

### ADC Quantization & Resolution
For an $N$-bit ADC with reference voltage $V_{ref}$:

$$\text{LSB} = \frac{V_{ref}}{2^N - 1}, \quad V_{measured} = \text{ADC}_{\text{raw}} \times \frac{V_{ref}}{2^N - 1}$$

* **Signal-to-Noise Ratio (Ideal ADC):** $\text{SNR}_{\text{dB}} = 6.02 \cdot N + 1.76$

### RTOS Task State Machine
```mermaid
stateDiagram-v2
    [*] --> Ready: xTaskCreate()
    Ready --> Running: Scheduler Dispatch (Highest Priority)
    Running --> Ready: Preempted / Time Slice Expired
    Running --> Blocked: vTaskDelay() / Semaphore Wait / Queue Empty
    Blocked --> Ready: Timeout Expired / Event Occurred / Interrupt (ISR)
    Running --> Suspended: vTaskSuspend()
    Suspended --> Ready: vTaskResume()
```

---

## ⚠️ 3. MCU Boot Traps & PCB Design Checklist

### ESP32 (WROOM / WROVER) Strapping & Restricted Pins
| Pin | Default | Restriction / Hardware Trap |
| :--- | :--- | :--- |
| **GPIO 0** | Pull-up | Must be **HIGH** for normal boot. **LOW** enters UART Flashing mode. Avoid heavy capacitive loads. |
| **GPIO 2** | Pull-down | Must be **LOW** or floating during flashing. Often connected to onboard LED. |
| **GPIO 12 (MTDI)** | Pull-down | Sets internal flash voltage (`VDD_SDIO`). If pulled **HIGH** at boot, selects $1.8\text{ V}$ instead of $3.3\text{ V}$ $\to$ **bootloop / brownout!** |
| **GPIO 15 (MTDO)** | Pull-up | If pulled **LOW** at boot, silences all UART0 bootROM diagnostic log messages. |
| **GPIO 6–11** | — | **Connected to internal SPI Flash.** Never use for general I/O (triggers immediate crash). |
| **GPIO 34–39** | Floating | **Input-only pins!** No internal pull-ups/pull-downs, no PWM or output drive capability. |
| **ADC2 Pins** | — | **Cannot be used** when Wi-Fi or Bluetooth driver is active (hardware conflict). Always use **ADC1** (`GPIO 32–39`). |

### STM32 (F1 / F4 Series) Hardware Traps
* **`BOOT0` Pin:** Never leave floating! Pull to **GND** via a $10\text{ k}\Omega$ resistor for normal Flash execution. A floating `BOOT0` pin causes random hard-faults or failure to boot on power-up.
* **SWD Debugging (`PA13` / `SWDIO`, `PA14` / `SWCLK`):** Never repurpose these pins as general GPIO inside `main()` without a startup delay, otherwise you will brick SWD debugger access on the next flash attempt.

### 🛡️ Pre-Flight PCB & Schematic Design Checklist
* [ ] **Decoupling Capacitors:** $100\text{ nF}$ ceramic (X7R/X5R) placed within $< 2\text{ mm}$ of *every* `VDD` pin, plus $4.7\text{ }\mu\text{F} - 10\text{ }\mu\text{F}$ bulk capacitor per IC power rail.
* [ ] **I2C Pull-ups:** External $2.2\text{ k}\Omega - 4.7\text{ k}\Omega$ resistors placed on `SDA` and `SCL` lines (internal MCU pull-ups of $\approx 40\text{ k}\Omega$ are too weak and cause severe signal rise-time distortion).
* [ ] **Reverse Polarity Protection:** P-Channel MOSFET on the high side (ultra-low voltage drop compared to a series Schottky diode).
* [ ] **Inductive Loads (Relays / Motors / Solenoids):** Flyback diode (e.g., 1N4148 or 1N5819) placed in anti-parallel across the coil to clamp back-EMF voltage spikes ($V = -L \frac{dI}{dt}$).
* [ ] **Op-Amp Unused Channels:** Never ground inputs directly! Configure unused channels as a **Voltage Follower** (`Output` tied to `-IN`, and `+IN` tied to a mid-supply reference $\frac{V_{CC}}{2}$).

---

## 📐 4. Engineering Mathematics

### Infinite Series Convergence Tests
Given an infinite series $\sum_{n=1}^{\infty} a_n$:

```mermaid
flowchart TD
    Start["Check Limit: lim (n→∞) a_n = 0 ?"] -->|No| Div["Diverges (Divergence Test)"]
    Start -->|Yes| Type{"Form of a_n?"}
    Type -->|"1 / n^p"| PSeries["p-Series: Converges if p > 1"]
    Type -->|"a * r^n"| Geom["Geometric: Converges if |r| < 1"]
    Type -->|"(-1)^n b_n"| Alt["Alternating (Leibniz): Converges if b_(n+1) <= b_n"]
    Type -->|"Factorials / Powers"| Ratio["Ratio Test: L = lim |a_(n+1) / a_n|"]
    Ratio -->|"L < 1"| Conv["Converges Absolutely"]
    Ratio -->|"L > 1"| Div2["Diverges"]
    Ratio -->|"L = 1"| Inc["Inconclusive (Try Raabe's or Integral Test)"]
```

### Fourier & Laplace Transforms
* **Continuous Fourier Transform:**

$$F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-j\omega t} \, dt$$

* **Unilateral Laplace Transform (Control Systems):**

$$F(s) = \mathcal{L}\{f(t)\} = \int_{0}^{\infty} f(t) e^{-st} \, dt, \quad s = \sigma + j\omega$$

<details>
<summary><b>Click to expand: Common Laplace Transform Pairs</b></summary>

| Time Domain $f(t)$ ($t \ge 0$) | Laplace Domain $F(s)$ | Region of Convergence |
| :--- | :--- | :--- |
| Dirac Delta $\delta(t)$ | $1$ | All $s$ |
| Unit Step $u(t)$ | $\frac{1}{s}$ | $\text{Re}(s) > 0$ |
| Ramp $t$ | $\frac{1}{s^2}$ | $\text{Re}(s) > 0$ |
| Exponential Decay $e^{-at}$ | $\frac{1}{s + a}$ | $\text{Re}(s) > -a$ |
| Sine Wave $\sin(\omega t)$ | $\frac{\omega}{s^2 + \omega^2}$ | $\text{Re}(s) > 0$ |
| Cosine Wave $\cos(\omega t)$ | $\frac{s}{s^2 + \omega^2}$ | $\text{Re}(s) > 0$ |
| First Derivative $\frac{df(t)}{dt}$ | $sF(s) - f(0^-)$ | — |

</details>

---

## 🐧 5. Linux CLI & Hardware Debugging (Fedora / RHEL / Debian)

### Hardware & Serial Debugging
```bash
# List all USB devices and bus hierarchy tree
lsusb && lsusb -t

# Watch kernel ring buffer in real-time (catch USB/Serial plug events)
dmesg -wH

# Connect to UART serial port at 115200 baud (using picocom)
picocom -b 115200 /dev/ttyUSB0

# Grant current user access to serial ports without sudo (re-login required)
sudo usermod -aG dialout,uucp $USER

# Inspect ELF binary size (Flash vs RAM usage for embedded targets)
arm-none-eabi-size firmware.elf
```

### Systemd, Processes & Networking
```bash
# Find which process is holding a specific port (e.g., 8080)
sudo ss -tulpn | grep :8080

# Analyze system boot performance and slow services
systemd-analyze blame

# Follow live logs of a specific background service
journalctl -u nginx.service -f

# Check which process locked a serial port
lsof /dev/ttyUSB0
```

### DNF Package Management (Fedora / RHEL)
```bash
# Find which package provides a missing shared library or binary
dnf provides "*/libGL.so.1"

# View transaction history and rollback a broken update
sudo dnf history
sudo dnf history undo <ID>
```

---

## 🗄️ 6. SQL & Time-Series Telemetry

### Execution Order vs. Lexical Order
SQL queries are **not** executed in the order they are written:

```mermaid
flowchart LR
    A[1. FROM / JOIN] --> B[2. WHERE]
    B --> C[3. GROUP BY]
    C --> D[4. HAVING]
    D --> E[5. SELECT / Window]
    E --> F[6. DISTINCT]
    F --> G[7. ORDER BY]
    G --> H[8. LIMIT / OFFSET]
```

### Analytical Window Functions (Sensor Telemetry Example)
Calculate a 5-point moving average and delta from the previous reading without collapsing rows:

```sql
SELECT 
    device_id,
    recorded_at,
    voltage_mv,
    LAG(voltage_mv, 1) OVER (PARTITION BY device_id ORDER BY recorded_at) AS prev_voltage,
    AVG(voltage_mv) OVER (
        PARTITION BY device_id 
        ORDER BY recorded_at 
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS moving_avg_5pt
FROM sensor_telemetry
WHERE recorded_at >= NOW() - INTERVAL '24 hours';
```

---

## 🎵 7. Bonus: Bytebeat & Algorithmic Audio

1-line C expressions evaluated at sample rate $f_s = 8000\text{ Hz}$, where `t` is a monotonically increasing integer (`uint32_t t = 0, 1, 2...`), outputting an 8-bit unsigned PCM waveform (`0..255`).

* **Frequency Conversion:** To generate a tone of frequency $f_{\text{Hz}}$ at sample rate $f_s$:

$$\text{Step} = \frac{256 \cdot f_{\text{Hz}}}{f_s}$$

* **Classic 42 Melody:**
  ```c
  t * (42 & t >> 10)
  ```
* **Exponential Decay Kick / Bass Drum Envelope:**
  ```c
  (int)(sin(sqrt(t % 4096) * 20) * 127) + 128
  ```
* **Pseudo-Random Noise Hat (LFSR approximation):**
  ```c
  ((t * (t >> 8 | t >> 9) & 46 & t >> 8)) ^ (t & t >> 13 | t >> 6)
  ```

---

## 🤝 Contributing
Contributions, corrections, and new engineering formulas are welcome!
1. Fork the repository.
2. Ensure all math uses native `$inline$` or `$$block$$` LaTeX syntax (avoid underscores inside `\text{...}` blocks).
3. Ensure all diagrams use native `mermaid` code blocks.
4. Submit a Pull Request.

## 📄 License
To the extent possible under law, the authors have waived all copyright and related or neighboring rights to this work under the **CC0 1.0 Universal Public Domain Dedication**.
