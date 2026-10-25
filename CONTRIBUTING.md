# Contributing to Embedded Engineering Handbook

Thank you for helping make this handbook a reliable, zero-fluff reference for hardware and firmware engineers!

## 1. Types of Welcome Contributions

* **Technical Corrections (Highest Priority):** Fixing formula sign conventions, boundary conditions, unit errors, or MCU family overgeneralizations.
* **Hardware Traps & Errata:** Documenting real-world microcontroller strapping pin traps, peripheral clock anomalies, or PCB layout pitfalls backed by manufacturer documentation.
* **Calculation Scripts:** Small, dependency-free Python 3 CLI utilities in `scripts/` (e.g., CRC calculators, I2C pull-up resistance calculators, ADC voltage divider solvers).
* **SPICE Simulation Netlists:** Portable SPICE-3f5 `.cir` files in `simulations/` that run cleanly in `ngspice`, `LTspice`, and `Micro-Cap`.

## 2. Technical Citation & Formatting Requirements

1. **Authoritative Sources Only:** Any microcontroller-specific claim (STM32, ESP32, RP2040, AVR, etc.) must specify the exact chip family and cite the official datasheet, reference manual (e.g., *ST RM0008*, *ST AN2834*), or silicon errata sheet.
2. **Native Math & Diagrams Only:**
   * Do **not** commit raster screenshots (`.png`, `.jpg`) of equations or block diagrams.
   * Use `$inline$` or `$$display$$` LaTeX for mathematical equations.
   * **LaTeX Compatibility Rule:** Never place raw underscores `_` inside `\text{...}` blocks (use subscripts like `\text{ADC}_{\text{raw}}`), and leave a blank line before and after every `$$` block and every Markdown list (`*`).
   * Use `mermaid` code blocks for state machines and flowcharts.
   * Use plain Markdown text and standard Unicode symbols (`kΩ`, `μF`, `°C`) for simple numbers and units inside tables. 

## 3. Local Validation Before Submitting a Pull Request

Run these commands locally to verify that your changes compile cleanly:

```bash
# 1. Verify Python script syntax and CLI execution
python3 -m py_compile scripts/*.py
python3 scripts/stm32_timer_calc.py --clk 72000000 --freq 50 --bits 16

# 2. Verify MkDocs site build in strict mode
pip install mkdocs-material
mkdir -p docs/javascripts
cp README.md docs/index.md
cp -r pinouts scripts simulations docs/
mkdocs build --strict
```

## 4. Licensing

By submitting a Pull Request or Issue to this repository, you agree to dedicate your contribution to the public domain under the **[CC0 1.0 Universal](./LICENSE)** license. Do not submit copyrighted tables, proprietary datasheet screenshots, or NDA-restricted material.
